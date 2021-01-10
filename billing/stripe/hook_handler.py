from billing import models


class StripeHookHandler:

    def __init__(self, event):
        self.event = event
        handlers = {
            'payment_intent.succeeded': self._payment_intent_succeeded,
            'account.updated': self._account_updated
        }
        self._handler_function = handlers.get(self.event.type)
        self.invalid_event = self._handler_function is None

    def handle(self):
        return self._handler_function() if not self.invalid_event else False

    def _payment_intent_succeeded(self):
        payment_intent = self.event.data.object
        try:
            intent = models.PaymentIntent.objects.get(stripe_id=payment_intent.id)
            intent.payment_succeeded(payment_intent)
            return True
        except models.PaymentIntent.DoesNotExist as e:
            return False

    def _account_updated(self):
        account = self.event.data.object
        try:
            stripe_account = models.Account.objects.get(stripe_id=account.id)
            stripe_account.update_stripe_fields(account)
            return True
        except models.Account.DoesNotExist:
            return False
