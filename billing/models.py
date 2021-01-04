from . import managers
from django.db import models
from core.models import User
from scheduling.models import Company
from datetime import datetime


class BillingCustomer(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)


class BillingCompanyCustomer(BillingCustomer):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    objects = managers.CompanyCustomerManager()


class BillingUserCustomer(BillingCustomer):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = managers.UserCustomerManager()


class Subscription(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)
    customer = models.ForeignKey(BillingCustomer, on_delete=models.CASCADE)
    is_trial = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    objects = managers.SubscriptionManager()

    @property
    def is_expired(self):
        return self.current_period_end > datetime.now()


class StripeConnectedAccount(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)
    owner = models.OneToOneField(Company, on_delete=models.CASCADE)
    details_submitted = models.BooleanField(default=False)
    charges_enabled = models.BooleanField(default=False)
    payouts_enabled = models.BooleanField(default=False)
    default_currency = models.CharField(max_length=20, null=True)

    objects = managers.ConnectedAccountManager()

    @property
    def is_stripe_enabled(self):
        return self.charges_enabled and self.details_submitted and self.payouts_enabled
    
    def update_stripe_fields(self, stripe_act):
        self.details_submitted = stripe_act.details_submitted
        self.charges_enabled = stripe_act.charges_enabled
        self.payouts_enabled = stripe_act.payouts_enabled
        self.default_currency = stripe_act.default_currency
        self.save()
