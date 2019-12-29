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
from scheduling.api_admin.permissions import ModelPermission

import cloudinary.uploader


class WithPermissionsModelViewSet(viewsets.ModelViewSet):
    queryset_class = None

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]

        if self.action in ['list', 'retrieve']:
            permission_classes.append(ModelPermission('view', self.queryset_class))

        if self.action == 'create':
            permission_classes.append(ModelPermission('add', self.queryset_class))

        if self.action == 'update':
            permission_classes.append(ModelPermission('change', self.queryset_class))

        return [permission() for permission in permission_classes]


class EmployeeViewSet(WithPermissionsModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.EmployeeReadSerializer
    write_serializer_class = serializers.EmployeeWriteSerializer
    queryset = Employee.objects.all()
    queryset_class = 'employee'

    # TODO: Delete old profile picture when a new one is added
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
    queryset_class = 'service'


class ShiftViewSet(WithPermissionsModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.ShiftReadSerializer
    write_serializer_class = serializers.ShiftWriteSerializer
    queryset = Shift.objects.all()
    queryset_class = 'shift'

