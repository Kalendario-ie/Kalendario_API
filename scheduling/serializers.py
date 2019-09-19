from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from scheduling.customException import ModelCreationFailedException
from scheduling.models import Service, Employee, Appointment, Customer, SelfAppointment


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'name', 'phone')


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
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'status', 'customer_notes')


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


class AppointmentWriteSerializer(serializers.ModelSerializer):
    end = serializers.DateTimeField(required=False)

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'customer_notes', 'status')

    def create(self, validated_data):
        try:
            appoint = Appointment.objects.create(**validated_data)
            return appoint
        except ModelCreationFailedException as e:
            raise PermissionDenied({"message": str(e)})

    def get_validation_exclusions(self):
        exclusions = super(AppointmentWriteSerializer, self).get_validation_exclusions()
        return exclusions + ['end']


class SelfAppointmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfAppointment
        fields = ('id', 'start', 'end', 'employee', 'reason')


class SelfAppointmentReadSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = SelfAppointment
        fields = ('id', 'start', 'end', 'employee', 'reason')


class CustomerAppointmentWriteSerializer(AppointmentWriteSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'customer_notes', 'status')


class EmployeeAppointmentWriteSerializer(AppointmentWriteSerializer):

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'status', 'customer_notes')


class AppointmentQuerySerlializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(required=False)
    customer = serializers.IntegerField(required=False)
    employee = serializers.IntegerField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
