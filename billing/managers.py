from django.db import models
from billing.stripe import helpers


class PaymentIntentManager(models.Manager):

    def get_or_create(self, request_id):
        intent, created = super().get_or_create(request_id=request_id)
        intent.amount = intent.request.total * 100
        stripe_intent = helpers.create_payment_intent(intent) if created else helpers.update_payment_intent(intent)
        intent.update_stripe_fields(stripe_intent)
        return intent, created
