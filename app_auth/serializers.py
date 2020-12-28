from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from core.models import User
from scheduling.models import Company, Employee
from scheduling.serializers import ServiceSerializer, ScheduleReadSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    schedule = ScheduleReadSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'private', 'name', 'instagram', 'schedule',
                  'email', 'phone', 'services', 'profile_img', 'bio')


class UserSerializer(serializers.ModelSerializer):
    owner = CompanySerializer()
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        source='get_all_permissions'
    )
    employee = EmployeeSerializer()

    class Meta:
        model = User
        fields = ('id', 'owner', 'email', 'first_name', 'last_name', 'name',
                  'groups', 'permissions', 'employee', 'verified')


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)

    def get_cleaned_data(self):
        cleaned_data = RegisterSerializer.get_cleaned_data(self)
        cleaned_data['first_name'] = self.validated_data.get('first_name', '')
        cleaned_data['last_name'] = self.validated_data.get('last_name', '')
        return cleaned_data
