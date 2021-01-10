from scheduling.models import Request, Appointment
from . import models


def payment_intent_succeeded(payment_intent):
    try:
        request = Request.objects.get_by_payment_intent_id(payment_intent.id)
        request.status = Appointment.ACCEPTED
        request.save()
    except Request.DoesNotExist as e:
        return False
    request.stripe_payment_intent_succeeded(payment_intent.get('amount'))
    return True


def account_updated(event):
    account = event.data.object
    stripe_account = models.StripeAccount.objects.get(stripe_id=account.id)
    stripe_account.update_stripe_fields(account)


handlers = {
    'payment_intent.succeeded': payment_intent_succeeded,
    'account.external_account.updated': None,
    'account.external_account.deleted': None,
    'account.application.deauthorized': None,
    'account.application.authorized': None,
    'account.external_account.created': None,
    'account.updated': account_updated
}
