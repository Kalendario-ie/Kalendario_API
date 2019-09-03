from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from scheduling.models import Appointment, ModelCreationFailedException


class EmployeeAppointmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'status')

    def create(self, validated_data):
        try:
            appoint = Appointment.objects.create(**validated_data)
            return appoint
        except ModelCreationFailedException as e:
            raise PermissionDenied({"message": str(e)})
