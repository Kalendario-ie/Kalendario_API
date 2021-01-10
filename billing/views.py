from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
import logging
from kalendario.common import viewsets, mixins
from . import serializers, models, stripe


logger = logging.getLogger(__name__)


class AccountViewSet(mixins.WithPermissionsMixin,
                     mixins.AuthOwnerFilterMixin,
                     viewsets.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()
    lookup_field = 'owner_id'

    @action(detail=True, methods=['post'])
    def connect(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            origin = self.request.headers.get('origin', '')
            return_url = origin + '/admin/home'
            refresh_url = origin + reverse('billing-account-detail', kwargs={self.lookup_field: instance.id})
            account_link_url = stripe.helpers.generate_account_link(instance.stripe_id, refresh_url, return_url)
            return Response({'url': account_link_url})
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


@csrf_exempt
@require_POST
def get_payment_intent(request):
    payload = request.body

    pi, created = models.PaymentIntent.objects.get_or_create(payload['request_id'])

    if request.user and request.user.id != pi.user.id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response({'clientSecret': pi.client_secret})


@csrf_exempt
@require_POST
def stripe_hook(request):
    """
    Returns 200 if everything went ok
    400 if couldn't get the event or the secret is wrong
    422 if the event type has no handler
    404 if the event doesn't belong to a know entity
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.helpers.construct_event(payload, sig_header)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.helpers.SignatureVerificationError as e:
        # Invalid signature
        logger.error('Invalid Stripe signature')
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    handler = stripe.hook_handler.StripeHookHandler(event)

    if handler.invalid_event:
        return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if not handler.handle():
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(status=status.HTTP_200_OK)
