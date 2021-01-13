from rest_framework import serializers
from scheduling import models


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'name', 'duration', 'description', 'price', 'category', 'cost')


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = ('id', 'name', 'color')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'last_name', 'name', 'email', 'phone')


class EmployeeSerializer(PersonSerializer):
    class Meta(PersonSerializer.Meta):
        model = models.Employee
        fields = PersonSerializer.Meta.fields + ('profile_img', 'bio', 'services')


class SlotQuerySerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    service = serializers.IntegerField()
    employee = serializers.IntegerField(required=False)
    customer = serializers.IntegerField(required=False)

    def validate_service(self, service):
        try:
            s = models.Service.objects.get(pk=service)
            return s
        except models.Service.DoesNotExist:
            raise serializers.ValidationError('Invalid service id')

    def validate_employee(self, employee):
        try:
            return models.Employee.objects.get(pk=employee) if employee is not None else None
        except models.Employee.DoesNotExist:
            raise serializers.ValidationError('Invalid employee id')

    def validate_customer(self, customer):
        try:
            return models.Person.objects.get(pk=customer) if customer is not None else None
        except models.Person.DoesNotExist:
            raise serializers.ValidationError('Invalid customer id')


class SlotSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Config
        fields = ('owner', 'pre_book_warn', 'post_book_message', 'post_book_email_message',
                  'appointment_reminder_message', 'appointment_accepted_message',
                  'appointment_rejected_message', 'can_receive_card_payments', 'can_receive_unpaid_request',
                  'show_services', 'show_employees')


class CompanySerializer(serializers.ModelSerializer):
    config = ConfigSerializer()

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'avatar', 'address', 'config')


class CompanyDetailsSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    employees = EmployeeSerializer(many=True, read_only=True)
    service_categories = ServiceCategorySerializer(many=True, read_only=True, source='servicecategory_set')
    config = ConfigSerializer()

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'address', 'about', 'avatar', 'employees', 'services', 'config',
                  'service_categories')


class AppointmentReadSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    customer = PersonSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    owner = CompanySerializer(read_only=True)

    class Meta:
        model = models.Appointment
        fields = ('id', 'owner', 'start', 'end', 'employee', 'service', 'customer', 'status')


class AddAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('id', 'start', 'employee', 'service')
        extra_kwargs = {'employee': {'required': False}}
        read_only_fields = ['owner_id']

    def save(self, **kwargs):
        validated_data = {
            **self.validated_data,
            'user': self.context.get('user'),
            'owner_id': self.validated_data.get('service').owner_id
        }
        self.instance = self.create(validated_data).request
        return self.instance

    def create(self, validated_data):
        request = models.Request.objects.get_current(validated_data.get('owner_id'),
                                                     validated_data.get('user').id)
        return request.add_appointment(**validated_data)


class AppointmentQuerySerializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    employees = serializers.ListField(required=False)
    services = serializers.ListField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RequestQueryBaseSerializer(serializers.Serializer):
    appointment = serializers.IntegerField(required=False)
    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RequestQueryRequiredOwnerSerializer(RequestQueryBaseSerializer):
    owner = serializers.IntegerField()


class RequestQuerySerializer(RequestQueryBaseSerializer):
    owner = serializers.IntegerField(required=False)


class RequestReadSerializer(serializers.ModelSerializer):
    appointments = AppointmentReadSerializer(read_only=True, many=True, source='appointment_set')
    owner = CompanySerializer(read_only=True)

    class Meta:
        model = models.Request
        fields = ('id', 'owner', 'appointments', 'total', 'fee', 'complete', 'status', 'customer_notes', 'scheduled_date')


class RequestWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Request
        fields = ('id', 'customer_notes')
