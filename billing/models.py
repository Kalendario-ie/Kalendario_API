from django.db import models
from core.models import User
from scheduling.models import Company
from datetime import datetime

from . import managers


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
