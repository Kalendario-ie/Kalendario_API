from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from core.models import User


@receiver(email_confirmed)
def after_email_confirmed(sender, email_address, **kwargs):
    user = User.objects.filter(email=email_address).first()
    user.link_to_customers()
    user.enable_create_company()
