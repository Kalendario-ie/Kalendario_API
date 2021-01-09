from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from kalendario.common import viewsets, mixins, stripe_helpers
from . import serializers, models


class StripeViewSet(mixins.WithPermissionsMixin,
                    mixins.AuthOwnerFilterMixin,
                    viewsets.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.StripeConnectedAccountSerializer
    queryset = models.StripeAccount.objects.all()
    lookup_field = 'owner_id'

    @action(detail=True, methods=['post'])
    def url(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            origin = self.request.headers.get('origin', '')
            return_url = origin + '/admin/home'
            refresh_url = origin + reverse('company-stripe-detail', kwargs={self.lookup_field: instance.id})
            account_link_url = stripe_helpers.generate_account_link(instance.stripe_id, refresh_url, return_url)
            return Response({'url': account_link_url})
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
