from django.core.mail import send_mail as send_email


def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    html_message=None
):
    try:
        send_email(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
            html_message=html_message,
        )
    
    except Exception:
        # nothing as of now, create log later
        pass