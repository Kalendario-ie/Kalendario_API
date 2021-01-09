from django.db.models.signals import post_save

from billing import models
from core.models import User
from scheduling.models import Company
from stripe.error import InvalidRequestError
import logging
from datetime import datetime
from kalendario.common import stripe_helpers


def create_subscription(billing_customer):
    stripe_subscription = stripe_helpers.create_subscription(billing_customer.stripe_id)
    subscription = models.Subscription.objects.create(customer=billing_customer,
                                                      stripe_id=stripe_subscription.stripe_id,
                                                      start_date=datetime.fromtimestamp(stripe_subscription.start_date),
                                                      current_period_start=datetime.fromtimestamp(
                                                          stripe_subscription.current_period_start),
                                                      current_period_end=datetime.fromtimestamp(
                                                          stripe_subscription.current_period_end),
                                                      is_active=stripe_subscription.status == 'active'
                                                      )
    return subscription


def create_company_customer(company):
    try:
        stripe_customer = stripe_helpers.create_customer(company)
        company_customer = models.BillingCompanyCustomer.objects.create(company=company,
                                                                        stripe_id=stripe_customer.stripe_id)
        subscription = create_subscription(company_customer)
    except InvalidRequestError as e:
        logging.error(
            f'Could not create stripe customer for Company id: {company.id} ({company.name}) with message {e}'
        )


def create_user_customer(user):
    stripe_customer = stripe_helpers.create_customer(user)
    return models.BillingUserCustomer.objects.create(user=user, stripe_id=stripe_customer.stripe_id)


def create_connected_account(company):
    connected_account = stripe_helpers.create_account(company)
    sca = models.StripeConnectedAccount.objects.create(owner=company, stripe_id=connected_account.stripe_id)
    sca.update_stripe_fields(connected_account)


def company_post_save(sender, instance: Company, **kwargs):
    try:
        models.BillingCompanyCustomer.objects.get(company=instance)
    except models.BillingCompanyCustomer.DoesNotExist:
        create_company_customer(instance)

    try:
        models.StripeConnectedAccount.objects.get(owner=instance)
    except models.StripeConnectedAccount.DoesNotExist:
        create_connected_account(instance)


def user_post_save(sender, instance: User, **kwargs):
    try:
        models.BillingUserCustomer.objects.get(user=instance)
    except models.BillingUserCustomer.DoesNotExist:
        create_user_customer(instance)


post_save.connect(company_post_save, sender=Company)
post_save.connect(user_post_save, sender=User)
