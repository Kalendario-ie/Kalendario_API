from scheduling.models import Appointment
from scheduling.serializers import AppointmentWriteSerializer


class EmployeeAppointmentWriteSerializer(AppointmentWriteSerializer):

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'status', 'customer_notes')

