from django.conf import settings

from django.http import HttpResponse
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from kalendario.common import stripe_helpers
from webhooks import models
from scheduling.models import Request, Appointment


def handle_payment_intent_succeeded(stripe_event):
    try:
        request = Request.objects.get_by_payment_intent_id(stripe_event.object_id)
        request.status = Appointment.ACCEPTED
        request.save()
    except Request.DoesNotExist as e:
        return False
    request.stripe_payment_intent_succeeded(stripe_event.event_obj.get('amount'))
    return True


def handle_account_application_authorized(stripe_event):
    pass


@csrf_exempt
@require_POST
def my_webhook_view(request):
    """
    Returns 200 if everything went ok
    400 if couldn't get the event or the secret is wrong
    422 if the event type has no handler
    404 if the event doesn't belong to a know entity
    """
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    payload = request.body
    event = None
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe_helpers.stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    handlers = {
        'payment_intent.succeeded': handle_payment_intent_succeeded,
        'account.external_account.updated': None,
        'account.external_account.deleted': None,
        'account.application.deauthorized': None,
        'account.application.authorized': handle_account_application_authorized,
        'account.external_account.created': None
    }
    stripe_event = models.StripeEvent.from_event(event)
    handler = handlers.get(event.type)

    if handler is None:
        return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    handled = handler(stripe_event)

    if not handled:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    stripe_event.is_handled = True
    stripe_event.save()

    return HttpResponse(status=status.HTTP_200_OK)

