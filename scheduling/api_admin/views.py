from drf_rw_serializers import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from scheduling.api_admin import serializers
from scheduling.models import Employee, Service
from scheduling.api_admin import permissions


class WithPermissionsModelViewSet(viewsets.ModelViewSet):
    custom_permissions = {'view': [], 'create': [], 'change': [], 'delete': []}

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ['list', 'retrieve']:
            permission_classes.extend(self.custom_permissions['view'])
        if self.action == 'create':
            permission_classes.extend(self.custom_permissions['create'])
        return [permission() for permission in permission_classes]


class EmployeeViewSet(WithPermissionsModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.EmployeeReadSerializer
    write_serializer_class = serializers.EmployeeWriteSerializer
    queryset = Employee.objects.all()
    custom_permissions = {'view': [permissions.CanViewEmployees],
                          'create': [permissions.CanAddEmployees],
                          'change': [permissions.CanChangeEmployees],
                          'delete': [permissions.CanDeleteEmployees]}


class ServiceViewSet(WithPermissionsModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.ServiceReadSerializer
    write_serializer_class = serializers.ServiceReadSerializer
    queryset = Service.objects.all()
    custom_permissions = {'view': [permissions.CanViewServices],
                          'create': [permissions.CanAddServices],
                          'change': [permissions.CanChangeServices],
                          'delete': [permissions.CanDeleteServices]}
