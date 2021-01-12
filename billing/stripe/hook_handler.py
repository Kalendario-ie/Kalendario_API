from abc import ABC, abstractmethod

from billing import models


class BaseHandler(ABC):

    def __init__(self, event):
        self.event = event
        self._handler_function = self.get_handlers().get(self.event.type)
        self.invalid_event = self._handler_function is None

    @abstractmethod
    def get_handlers(self):
        """should return a dict where the key is the event type and the value is the function to handle the event"""
        pass

    def handle(self):
        return self._handler_function() if not self.invalid_event else False


class ConnectedAccountHookHandler(BaseHandler):

    def get_handlers(self):
        return {
            'account.updated': self._account_updated
        }

    def _account_updated(self):
        account = self.event.data.object
        try:
            stripe_account = models.Account.objects.get(stripe_id=account.id)
            stripe_account.update_stripe_fields(account)
            return True
        except models.Account.DoesNotExist:
            return False


class AccountHookHandler(BaseHandler):

    def get_handlers(self):
        return {
            'payment_intent.succeeded': self._payment_intent_succeeded,
        }

    def _payment_intent_succeeded(self):
        payment_intent = self.event.data.object
        try:
            intent = models.PaymentIntent.objects.get(stripe_id=payment_intent.id)
            intent.payment_succeeded(payment_intent)
            return True
        except models.PaymentIntent.DoesNotExist as e:
            return False
