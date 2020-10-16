from django.core import mail
from django.conf import settings


def send_mail(subject, message, recipient_list, fail_silently=False):
    mail.send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=fail_silently,
    )
