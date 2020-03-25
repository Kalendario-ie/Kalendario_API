from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from scheduling.customException import ModelCreationFailedException
from scheduling.models import Service, Employee, Appointment, Company, Person


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'name', 'email', 'phone')


class EmployeeSerializer(PersonSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    owner = CompanyReadSerializer(read_only=True)

    class Meta(PersonSerializer.Meta):
        model = Employee
        fields = PersonSerializer.Meta.fields + ('services', 'profile_img', 'bio', 'owner')


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


class AppointmentReadSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    customer = PersonSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'status', 'customer_notes')


class AppointmentWriteSerializer(serializers.ModelSerializer):
    end = serializers.DateTimeField(required=False)

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'customer_notes', 'status')

    def create(self, validated_data):
        try:
            appoint = self.Meta.model.objects.create(**validated_data)
            return appoint
        except ModelCreationFailedException as e:
            raise PermissionDenied(str(e))

    def get_validation_exclusions(self):
        exclusions = super(AppointmentWriteSerializer, self).get_validation_exclusions()
        return exclusions + ['end']


class CustomerAppointmentWriteSerializer(AppointmentWriteSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'start', 'end', 'employee', 'service', 'customer', 'customer_notes', 'status')


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
