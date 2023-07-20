from django.contrib import admin
from .models import CPUDetail, DiskUsageDetail, NetworkUsage, OtherDetail, ProcessDetail, RAMDetail, SwapDetail, Server

# Register your models here.
admin.site.register(CPUDetail)
admin.site.register(DiskUsageDetail)
admin.site.register(NetworkUsage)
admin.site.register(OtherDetail)
admin.site.register(ProcessDetail)
admin.site.register(RAMDetail)
admin.site.register(Server)
admin.site.register(SwapDetail)
