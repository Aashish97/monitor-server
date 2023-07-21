from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .helpers import get_class_name_from_instance
from .models import RAMDetail, DiskUsageDetail, SwapDetail
from .send_mail import send_mail


@receiver(post_save, sender=RAMDetail)
@receiver(post_save, sender=DiskUsageDetail)
@receiver(post_save, sender=RAMDetail)
def send_warning_mail(sender, **kwargs):
    class_name = get_class_name_from_instance(sender)
    class_name_excluding_detail = class_name.replace("Detail", "")
    instance = kwargs["instance"]
    usage_percent = instance.percent
    if instance.percent > 90:
        send_mail(
            f"{class_name_excluding_detail} of {instance.server} almost full",
            f"{class_name_excluding_detail} for {instance.server} is {usage_percent} %. Please free up some space.",
            settings.DEFAULT_FROM_EMAIL,
            settings.EMAIL_RECIPIENT,
            fail_silently=False,
            html_message=None
        )