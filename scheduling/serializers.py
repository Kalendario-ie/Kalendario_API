from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from scheduling.models import *
from scheduling.customException import ModelCreationFailedException


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = super(CustomerSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ('start', 'end', 'employee', 'service', 'customer')

    def create(self, validated_data):
        try:
            appoint = Appointment.objects.create(**validated_data)
            return appoint
        except ModelCreationFailedException as e:
            raise PermissionDenied({"message": str(e)})


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'instagram', 'email', 'phone', 'services')

