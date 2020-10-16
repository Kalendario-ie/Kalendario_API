from rest_framework import serializers
from scheduling import models
from core.models import User


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'last_name', 'name', 'email', 'phone')


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Config
        fields = ('owner_id', 'pre_book_warn', 'post_book_message', 'post_book_email_message',
                  'appointment_reminder_message', 'appointment_accepted_message', 'private',
                  'appointment_rejected_message', 'allow_card_payment', 'allow_unpaid_request')


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('id', 'name', )


class CompanySerializer(serializers.ModelSerializer):
    config = ConfigSerializer()

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'address', 'avatar', 'about',
                  'instagram', 'phone_number', 'whatsapp', 'facebook', 'config')
        read_only_fields = ['avatar']

    def update(self, instance, validated_data):
        self.save_config(instance, validated_data)
        return serializers.ModelSerializer.update(self, instance, validated_data)

    def save_config(self, instance, validated_data):
        config = validated_data.pop('config', {})
        cs = ConfigSerializer(instance=instance.config, data=config, partial=True)
        cs.is_valid(raise_exception=True), cs.save()


class StripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('id', 'stripe_details_submitted', 'stripe_charges_enabled', 'stripe_payouts_enabled',
                  'stripe_default_currency')


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = ('id', 'owner', 'name', 'color')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'owner', 'private', 'name', 'duration', 'color', 'description', 'cost', 'is_from', 'price', 'category')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = ('id', 'owner', 'private', 'name', 'first_name', 'last_name', 'instagram', 'schedule',
                  'email', 'phone', 'services', 'profile_img', 'bio')


class TimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeFrame
        fields = ('start', 'end')


class ShiftSerializer(serializers.ModelSerializer):
    frames = TimeFrameSerializer(many=True, read_only=False, source='timeframe_set')

    class Meta:
        model = models.Shift
        fields = ('frames', )


def updateShift(schedule, shift, validated_data):
    shift.schedule = schedule
    shift.save()

    frames, validatedFrames = list(shift.timeframe_set.all()), validated_data['timeframe_set']
    instanceLen, validatedLen, = len(frames), len(validatedFrames)

    for i in range(validatedLen if validatedLen > instanceLen else instanceLen):
        # While the shift have frames and there are frames in validated data update them
        if i < instanceLen and i < validatedLen:
            updateFrame(shift, frames[i], validatedFrames[i])
        # When there are extra frames from validated data but none in the shift, create a new frame
        elif i < validatedLen:
            updateFrame(shift, models.TimeFrame(), validatedFrames[i])
        # Lastly if there are less frames from the update delete the extra frames in the shift
        elif i < instanceLen:
            frame = frames[i]
            frame.delete()

    return shift


def updateFrame(shift, frame, validated_data):
    frame.shift = shift
    frame.start = validated_data['start']
    frame.end = validated_data['end']
    frame.save()


def updateSchedule(instance, validated_data):
    instance.name = validated_data.get('name')
    instance.owner = validated_data.get('owner')
    instance.save()

    for value in 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun':
        shift = getattr(instance, value) or models.Shift()
        shift = updateShift(instance, shift, validated_data.get(value))
        setattr(instance, value, shift)

    instance.save()
    return instance


class ScheduleReadSerializer(serializers.ModelSerializer):
    mon, tue, wed, thu, fri, sat, sun = [ShiftSerializer(many=False) for i in range(7)]

    class Meta:
        model = models.Schedule
        fields = ('id', 'owner', 'name', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

    def create(self, validated_data):
        return updateSchedule(models.Schedule(), validated_data)

    def update(self, instance, validated_data):
        return updateSchedule(instance, validated_data)


# class ScheduleWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Schedule
#         fields = ('id', 'owner', 'name', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('id', 'owner', 'first_name', 'last_name', 'name', 'phone', 'email')


class AppointmentReadSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    customer = PersonSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = models.Appointment
        fields = ('id', 'owner', 'start', 'end', 'employee', 'lock_employee', 'service',
                  'customer', 'status', 'internal_notes', 'request')


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    owner = CompanySerializer()
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        source='get_all_permissions'
    )

    class Meta:
        model = User
        fields = ('id', 'owner', 'email', 'first_name', 'last_name', 'name',
                  'person', 'groups', 'permissions')


class AppointmentHistorySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    customer = PersonSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    history_user = UserSerializer()

    class Meta:
        model = models.Appointment.history.model
        fields = (
            'id', 'owner', 'start', 'end', 'employee', 'service', 'customer', 'status', 'internal_notes'
            , 'history_date', 'history_user')


class AppointmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('id', 'owner', 'start', 'end', 'employee', 'service', 'customer'
                  , 'internal_notes', 'status')


class RequestSerializer(serializers.ModelSerializer):
    appointments = AppointmentReadSerializer(many=True, read_only=True, source='appointment_set')
    person = PersonSerializer(source='user.person')

    class Meta:
        model = models.Request
        fields = ('id', 'owner', 'appointments', 'complete', 'person', 'status')


class SelfAppointmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('id', 'owner', 'start', 'end', 'employee', 'customer', 'internal_notes', 'status')


class AppointmentQuerySerlializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(required=False)
    customer = serializers.IntegerField(required=False)
    employee = serializers.IntegerField(required=False)
    employees = serializers.ListField(required=False)
    services = serializers.ListField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RequestQuerySerlializer(serializers.Serializer):
    status = serializers.CharField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SchedulingPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchedulingPanel
        fields = ('id', 'owner', 'name', 'employees')
