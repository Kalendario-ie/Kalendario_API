from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from core.models import User
from scheduling.serializers import PersonSerializer, CompanyReadSerializer


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    company = CompanyReadSerializer()
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        source='get_all_permissions'
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'person', 'is_employee', 'permissions', 'company')


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_cleaned_data(self):
        cleaned_data = super(CustomRegisterSerializer, self).get_cleaned_data()
        cleaned_data['first_name'] = self.validated_data.get('first_name', '')
        cleaned_data['last_name'] = self.validated_data.get('last_name', '')
        return cleaned_data

    def save(self, request):
        return super(CustomRegisterSerializer, self).save(request)
