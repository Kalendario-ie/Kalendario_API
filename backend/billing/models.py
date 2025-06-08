import json

from django.db import models
from core.models import User
from scheduling.models import Company, Request
from datetime import datetime
from . import managers


class BillingCustomer(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)


class BillingCompanyCustomer(BillingCustomer):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)


class BillingUserCustomer(BillingCustomer):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Subscription(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)
    customer = models.ForeignKey(BillingCustomer, on_delete=models.CASCADE)
    is_trial = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    @property
    def is_expired(self):
        return self.current_period_end > datetime.now()


class Account(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)
    owner = models.OneToOneField(Company, on_delete=models.CASCADE)
    details_submitted = models.BooleanField(default=False)
    charges_enabled = models.BooleanField(default=False)
    payouts_enabled = models.BooleanField(default=False)
    default_currency = models.CharField(max_length=20, null=True)
    requirements_disabled_reason = models.CharField(max_length=255, null=True)
    requirements_currently_due = models.TextField(null=True)

    json_decoder = json.decoder.JSONDecoder()

    @property
    def is_stripe_enabled(self):
        return self.charges_enabled and self.details_submitted and self.payouts_enabled

    @property
    def currently_due(self):
        if self.requirements_currently_due is None:
            return []
        return self.json_decoder.decode(self.requirements_currently_due)

    @property
    def require_connect(self):
        """
        Returns true if the user is required to connect to stripe to provide extra information.
        """
        return self.requirements_disabled_reason is not None

    def update_stripe_fields(self, stripe_act):
        self.details_submitted = stripe_act.details_submitted
        self.charges_enabled = stripe_act.charges_enabled
        self.payouts_enabled = stripe_act.payouts_enabled
        self.default_currency = stripe_act.default_currency
        self.requirements_currently_due = json.dumps(stripe_act.requirements.currently_due)
        self.requirements_disabled_reason = stripe_act.requirements.disabled_reason
        self.save()


class PaymentIntent(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True, null=True)
    request = models.OneToOneField(Request, on_delete=models.CASCADE)
    client_secret = models.CharField(max_length=255, null=True)
    paid = models.BooleanField(default=False)
    application_fee_amount = models.FloatField(default=0)
    amount = models.IntegerField(default=0)
    amount_received = models.IntegerField(default=0)

    objects = managers.PaymentIntentManager()

    @property
    def account(self):
        return self.request.owner.account

    @property
    def user(self):
        return self.request.user

    @property
    def customer(self):
        return self.user.billingusercustomer

    @property
    def fee(self):
        return int(self.amount * 0.01)

    def update_stripe_fields(self, stripe_intent):
        self.stripe_id = stripe_intent.id
        self.client_secret = stripe_intent.client_secret
        self.amount = stripe_intent.amount or 0
        self.application_fee_amount = stripe_intent.application_fee_amount or 0
        self.save()

    def payment_succeeded(self, stripe_intent):
        self.request.accept()
        self.paid = True
        self.amount_received = stripe_intent.amount_received
        self.save()

