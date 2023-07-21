from django.db import models
from .constants import DEPLOYMENT_SERVER_CHOICES
from .helpers import pretty_display


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', '-modified_at')
        abstract = True
        
class Server(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=15)
    deployment_server = models.CharField(choices=DEPLOYMENT_SERVER_CHOICES, max_length=13)
    
    def __str__(self):
        return self.name
    
    
class BaseUsageDetail(BaseModel):
    server = models.ForeignKey(Server, related_name="+", on_delete=models.CASCADE)
    total = models.FloatField()
    used = models.FloatField()
    free = models.FloatField()
    percent = models.FloatField()
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.server} created at {self.created_at}"
    
    @property
    def display_total(self):
        return pretty_display(self.total)
    
    @property
    def display_used(self):
        return pretty_display(self.used)

    @property
    def display_free(self):
        return pretty_display(self.used)
    
    @property
    def display_percent(self):
        return pretty_display(self.free)
    

# Create your models here.
class CPUDetail(BaseModel):
    server = models.ForeignKey(Server, related_name="cpu_detail", on_delete=models.CASCADE)
    user_time = models.FloatField()
    system_time = models.FloatField()
    idle_time = models.FloatField()
    cpu_percentage = models.JSONField()
    cpu_count = models.IntegerField()
    
    def __str__(self):
        return f"{self.server} CPU detail for {self.created_at}"


class RAMDetail(BaseUsageDetail):
    available = models.FloatField()
    
    @property
    def display_available(self):
        return pretty_display(self.available)
    

class SwapDetail(BaseUsageDetail):
    pass
    

class DiskUsageDetail(BaseUsageDetail):
    location = models.CharField(max_length=255)
    

class OtherDetail(BaseModel):
    server = models.ForeignKey(Server, related_name="other_detail", on_delete=models.CASCADE)
    boot_time = models.DateTimeField()
    user = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user} logged in {self.boot_time}"
    

class NetworkUsage(BaseModel):
    server = models.ForeignKey(Server, related_name="network_detail", on_delete=models.CASCADE)
    byte_sent = models.BigIntegerField()
    bytes_received = models.BigIntegerField()
    packet_sent = models.BigIntegerField()
    packet_received = models.BigIntegerField()
    ip_address = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.server} network usage for {self.created_at}"
    
    
class ProcessDetail(BaseModel):
    server = models.ForeignKey(Server, related_name="process_detail", on_delete=models.CASCADE)
    process_info = models.JSONField()
    