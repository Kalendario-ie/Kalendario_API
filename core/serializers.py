from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from core import models
from scheduling.models import Company, Employee
from scheduling.serializers import ScheduleReadSerializer, ServiceSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    schedule = ScheduleReadSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'private', 'name', 'instagram', 'schedule',
                  'email', 'phone', 'services', 'profile_img', 'bio')


class UserSerializer(serializers.ModelSerializer):
    owner = CompanySerializer()
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        source='get_all_permissions'
    )
    employee = EmployeeSerializer()

    class Meta:
        model = models.User
        fields = ('id', 'owner', 'email', 'first_name', 'last_name', 'name',
                  'groups', 'permissions', 'employee', 'verified')


class UserAdminSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.IntegerField()

    class Meta:
        model = models.User
        fields = ('id', 'owner', 'email', 'first_name', 'last_name', 'name', 'groups', 'employee', 'employee_id')


class PasswordChangeSerializer(serializers.Serializer):
    user_password = serializers.CharField(max_length=128)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_user_password(self, value):
        invalid_password_conditions = (
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        password1 = self.initial_data.get('password1')
        password2 = self.initial_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError('password_mismatch')
        return attrs

    def save(self):
        self.instance.set_password(self.validated_data.get('password1'))
        self.instance.save()
        return self.user


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_cleaned_data(self):
        cleaned_data = RegisterSerializer.get_cleaned_data(self)
        cleaned_data['first_name'] = self.validated_data.get('first_name', '')
        cleaned_data['last_name'] = self.validated_data.get('last_name', '')
        return cleaned_data

    def save(self, request):
        return RegisterSerializer.save(self, request)


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ('id', 'name', 'codename')


class GroupProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, source='group_id')
    permissions = serializers.PrimaryKeyRelatedField(many=True,
                                                     queryset=models.permissions())

    class Meta:
        model = models.GroupProfile
        fields = ('id', 'owner', 'name', 'permissions')

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions')
        instance = serializers.ModelSerializer.update(self, instance, validated_data)
        instance.permissions.set(permissions)
        return instance

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        instance = serializers.ModelSerializer.create(self, validated_data)
        instance.permissions.set(permissions)
        return instance


