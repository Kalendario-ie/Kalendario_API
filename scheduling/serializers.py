from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from scheduling.customException import ModelCreationFailedException
from scheduling.models import Service, Employee, Appointment, Customer


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'name')

    def create(self, validated_data):
        user = super(CustomerSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'instagram', 'email', 'phone', 'services', 'profile_img', 'bio')


class AppointmentReadSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'status')


class SlotSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    service = serializers.IntegerField()

    def validate_service(self, service):
        try:
            s = Service.objects.get(pk=service)
            return s
        except Service.DoesNotExist:
            raise serializers.ValidationError('Invalid service id')
