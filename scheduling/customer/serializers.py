from scheduling.models import Appointment
from scheduling.serializers import AppointmentWriteSerializer


class CustomerAppointmentWriteSerializer(AppointmentWriteSerializer):

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'customer_notes')
