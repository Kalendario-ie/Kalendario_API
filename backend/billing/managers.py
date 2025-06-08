from django.db import models
from billing.stripe import helpers


class PaymentIntentManager(models.Manager):

    def get_or_create(self, request_id):
        intent, created = super().get_or_create(request_id=request_id)
        intent.amount = int(intent.request.total * 100)
        no_stripe_intent = created or intent.stripe_id is None
        intent.update_stripe_fields(
            helpers.create_payment_intent(intent) if no_stripe_intent else helpers.update_payment_intent(intent)
        )
        return intent, created
