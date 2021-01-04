from rest_framework import serializers
from . import models


class StripeConnectedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StripeConnectedAccount
        fields = ('id', 'details_submitted', 'charges_enabled', 'payouts_enabled',
                  'default_currency')
