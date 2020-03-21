import cloudinary.uploader as cloudinary_uploader
from cloudinary import CloudinaryResource
from django.db.models import Q
from drf_rw_serializers import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scheduling.util import StandardResultsSetPagination
from scheduling.api_admin import serializers
from scheduling.api_admin.permissions import IsCompanyAdmin, ModelPermissionFactory
from scheduling.models import Employee, Service, Schedule, Shift, Customer


class WithPermissionsModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardResultsSetPagination
    queryset_class = None

    action_perm_map = {'list': 'view',
                       'retrieve': 'view',
                       'create': 'add',
                       'update': 'change',
                       'partial_update': 'change'}

    def get_action_map(self):
        return self.action_perm_map

    def get_permissions(self):
        permission_classes = [IsAuthenticated,
                              ModelPermissionFactory(self.get_action_map().get(self.action), self.queryset_class)]

        if self.action == 'create':
            permission_classes.append(IsCompanyAdmin)
        if self.action in ['update', 'partial_update']:
            permission_classes.append(IsCompanyAdmin)

        return [perm() for perm in permission_classes]

    def get_queryset(self):
        queryset = self.queryset.order_by('id')
        return queryset.filter(owner_id=self.request.user.company_id)


class EmployeeViewSet(WithPermissionsModelViewSet):
    read_serializer_class = serializers.EmployeeReadSerializer
    write_serializer_class = serializers.EmployeeWriteSerializer
    queryset = Employee.objects.all()
    queryset_class = 'employee'

    def get_action_map(self):
        self.action_perm_map['photo'] = 'change'
        return self.action_perm_map

    # TODO: Delete old profile picture when a new one is added
    @action(detail=True, methods=['post'])
    def photo(self, request, pk=None):
        file = request.data.get('image')

        u = cloudinary_uploader.upload(file)

        employee = self.queryset.get(id=pk)
        employee.profile_img = CloudinaryResource(u['public_id'], u['format'], u['version'], u['signature'],
                                                  type=u['type'], resource_type=u['resource_type'])
        employee.save()

        return Response({
            'url': u['url']
        }, status=status.HTTP_200_OK)


class ServiceViewSet(WithPermissionsModelViewSet):
    read_serializer_class = serializers.ServiceReadSerializer
    write_serializer_class = serializers.ServiceReadSerializer
    queryset = Service.objects.all()
    queryset_class = 'service'


class ShiftViewSet(WithPermissionsModelViewSet):
    read_serializer_class = serializers.ShiftReadSerializer
    write_serializer_class = serializers.ShiftWriteSerializer
    queryset = Shift.objects.all()
    queryset_class = 'shift'


class ScheduleViewSet(WithPermissionsModelViewSet):
    read_serializer_class = serializers.ScheduleReadSerializer
    write_serializer_class = serializers.ScheduleWriteSerializer
    queryset = Schedule.objects.all()
    queryset_class = 'schedule'


class CustomerViewSet(WithPermissionsModelViewSet):
    read_serializer_class = serializers.CustomerReadSerializer
    write_serializer_class = serializers.CustomerWriteSerializer
    queryset = Customer.objects.all()
    queryset_class = 'customer'

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))

        return queryset
