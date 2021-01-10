from django.db import models
from billing.stripe import helpers


class RequestManager(models.Manager):

    def get_or_create(self, request_id):
        intent, created = super().get_or_create(request_id=request_id)
        request = intent.request
        stripe_intent = helpers.create_payment_intent(request) if created else helpers.update_payment_intent(request)
        intent.update_stripe_fields(stripe_intent)
        return intent, created
