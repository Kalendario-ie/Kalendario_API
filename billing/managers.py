from django.db import models
from kalendario.common import stripe_helpers
from datetime import datetime


class CustomerManager(models.Manager):

    def create(self, model, **kwargs):
        # Create Stripe Object
        metadata = {
            'class': model.__class__,
            'instance_id': model.id
        }
        stripe_customer = stripe_helpers.create_customer(model.name, model.email, metadata)
        # Update kwargs with stripe information
        kwargs.update({'stripe_id': stripe_customer.stripe_id})
        # Create model
        return models.Manager.create(self, **kwargs)


class CompanyCustomerManager(CustomerManager):
    def create(self, company, **kwargs):
        kwargs.update({'company': company})
        return CustomerManager.create(self, company, **kwargs)


class UserCustomerManager(CustomerManager):
    def create(self, user, **kwargs):
        kwargs.update({'user': user})
        return CustomerManager.create(self, user, **kwargs)


class SubscriptionManager(models.Manager):
    def create(self, billing_customer, **kwargs):
        stripe_subscription = stripe_helpers.create_subscription(billing_customer.stripe_id)
        kwargs.update({
            'customer': billing_customer,
            'stripe_id': stripe_subscription.stripe_id,
            'start_date': datetime.fromtimestamp(stripe_subscription.start_date),
            'current_period_start': datetime.fromtimestamp(stripe_subscription.current_period_start),
            'current_period_end': datetime.fromtimestamp(stripe_subscription.current_period_end),
            'is_active': stripe_subscription.status == 'active'
        })
        return models.Manager.create(self, **kwargs)


class ConnectedAccountManager(models.Manager):
    def create(self, owner, **kwargs):
        connected_account = stripe_helpers.create_account(metadata={'company': owner.id})
        kwargs.update({
            'owner': owner,
            'stripe_id': connected_account.stripe_id,
            'details_submitted': connected_account.details_submitted,
            'charges_enabled': connected_account.charges_enabled,
            'payouts_enabled': connected_account.payouts_enabled,
            'default_currency': connected_account.default_currency,
        })
        return models.Manager.create(self, **kwargs)
