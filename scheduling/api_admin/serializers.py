from rest_framework import serializers

from scheduling.models import Service, Employee, Shift


class ServiceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class EmployeeReadSerializer(serializers.ModelSerializer):
    services = ServiceReadSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'first_name', 'last_name', 'instagram',
                  'email', 'phone', 'services', 'profile_img', 'bio')


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'instagram', 'email', 'phone', 'services', 'profile_img', 'bio')


class ShiftReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift


class ShiftWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
