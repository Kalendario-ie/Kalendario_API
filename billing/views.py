from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.reverse import reverse
from kalendario.common import viewsets, mixins
from billing import serializers, models
from billing.stripe import views, hook_handler, helpers
from django.conf import settings
import logging

ACCOUNT_WEBHOOK_SECRET = getattr(settings, 'ACCOUNT_WEBHOOK_SECRET', '')
CONNECTED_ACCOUNT_WEBHOOK_SECRET = getattr(settings, 'CONNECTED_ACCOUNT_WEBHOOK_SECRET', '')

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
            account_link_url = helpers.generate_account_link(instance.stripe_id, refresh_url, return_url)
            return Response({'url': account_link_url})
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class PaymentIntentView(viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Request.objects.all()
    serializer_class = serializers.PaymentIntentSecretSerializer

    def get_queryset(self, **kwargs):
        return models.Request.objects.filter(user_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        request = self.get_object()
        pi, created = models.PaymentIntent.objects.get_or_create(request.id)
        serializer = self.get_serializer(pi)
        return Response(serializer.data)


class ConnectedAccountHookView(views.StripeHookView):
    hook_handler_class = hook_handler.ConnectedAccountHookHandler
    hook_secret = CONNECTED_ACCOUNT_WEBHOOK_SECRET


class AccountHookView(views.StripeHookView):
    hook_handler_class = hook_handler.AccountHookHandler
    hook_secret = ACCOUNT_WEBHOOK_SECRET
