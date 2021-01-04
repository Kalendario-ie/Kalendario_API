from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from kalendario.common import viewsets, mixins, stripe_helpers
from . import serializers, models


class StripeViewSet(mixins.WithPermissionsMixin,
                    mixins.AuthOwnerFilterMixin,
                    viewsets.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.StripeConnectedAccountSerializer
    queryset = models.StripeConnectedAccount.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            origin = self.request.headers.get('origin', '')
            return_url = origin + '/admin/home'
            refresh_url = origin + reverse('company-stripe-detail', kwargs={'pk': instance.id})
            account_link_url = stripe_helpers.generate_account_link(instance.stripe_id, refresh_url, return_url)
            return Response({'url': account_link_url})
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
