from cloudinary import CloudinaryResource
from cloudinary.templatetags import cloudinary
from drf_rw_serializers import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from scheduling.api_admin import serializers
from scheduling.models import Employee, Service, Shift
from scheduling.api_admin import permissions

import cloudinary.uploader


class WithPermissionsModelViewSet(viewsets.ModelViewSet):
    custom_permissions = {'view': [], 'create': [], 'change': [], 'delete': []}

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]

        if self.action in ['list', 'retrieve']:
            permission_classes.extend(self.custom_permissions['view'])

        if self.action == 'create':
            permission_classes.extend(self.custom_permissions['create'])

        if self.action == 'update':
            permission_classes.extend(self.custom_permissions['change'])

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

    @action(detail=True, methods=['post'])
    def photo(self, request, pk=None):
        file = request.data.get('image')

        u = cloudinary.uploader.upload(file)

        employee = self.queryset.get(id=pk)
        employee.profile_img = CloudinaryResource(u['public_id'], u['format'], u['version'], u['signature'],
                                                  type=u['type'], resource_type=u['resource_type'])
        employee.save()

        return Response({
            'url': u['url']
        }, status=status.HTTP_200_OK)


class ServiceViewSet(WithPermissionsModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.ServiceReadSerializer
    write_serializer_class = serializers.ServiceReadSerializer
    queryset = Service.objects.all()
    custom_permissions = {'view': [permissions.CanViewServices],
                          'create': [permissions.CanAddServices],
                          'change': [permissions.CanChangeServices],
                          'delete': [permissions.CanDeleteServices]}


class ShiftViewSet(WithPermissionsModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.ShiftReadSerializer
    write_serializer_class = serializers.ShiftWriteSerializer
    queryset = Shift.objects.all()
    custom_permissions = {'view': [permissions.CanViewShifts],
                          'create': [permissions.CanAddShifts],
                          'change': [permissions.CanChangeShifts],
                          'delete': [permissions.CanDeleteShifts]}
