from json import JSONEncoder
import json
import datetime

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from scheduling.models import Employee, Appointment, Service
from scheduling.customException import ModelCreationFailedException
from scheduling.utility import Slot


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


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

