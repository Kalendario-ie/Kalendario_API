from django.db.models.signals import post_save

from billing import models
from core.models import User
from scheduling.models import Company
from stripe.error import InvalidRequestError
import logging


def upsert_billing_company_account(sender, instance: Company, **kwargs):
    company_customer = models.BillingCompanyCustomer.objects.filter(company=instance).first()
    if company_customer is not None:
        pass
    else:
        try:
            company_customer = models.BillingCompanyCustomer.objects.create(instance)
            models.Subscription.objects.create(company_customer)
        except InvalidRequestError as e:
            logging.error(
                f'Could not create stripe customer for {sender} id: {instance.id} ({instance.name}) with message {e}'
            )


def upsert_billing_user_account(sender, instance: User, **kwargs):
    user_customer = models.BillingUserCustomer.objects.filter(user=instance).first()
    if user_customer is not None:
        pass
    else:
        models.BillingUserCustomer.objects.create(instance)


def upsert_stripe_connect_account(sender, instance: Company, **kwargs):
    connected_account = models.StripeConnectedAccount.objects.filter(owner=instance).first()
    if connected_account is None:
        models.StripeConnectedAccount.objects.create(instance)


post_save.connect(upsert_billing_company_account, sender=Company)
post_save.connect(upsert_stripe_connect_account, sender=Company)
post_save.connect(upsert_billing_user_account, sender=User)
