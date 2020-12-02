import cloudinary.uploader as cloudinary_uploader
from cloudinary import CloudinaryResource

from django.db.models import Q
from django.urls import reverse

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from appointment_manager.common import viewsets, mixins, stripe_helpers
from scheduling import serializers, models


class EmployeeViewSet(mixins.WithPermissionsMixin,
                      mixins.AuthOwnerFilterMixin,
                      viewsets.ModelViewSet):
    serializer_class = serializers.EmployeeSerializer
    queryset = models.Employee.objects.order_by('first_name')

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


class ServiceCategoryViewSet(mixins.WithPermissionsMixin,
                             mixins.AuthOwnerFilterMixin,
                             viewsets.ModelViewSet):
    serializer_class = serializers.ServiceCategorySerializer
    queryset = models.ServiceCategory.objects.all()


class ServiceViewSet(mixins.WithPermissionsMixin,
                     mixins.AuthOwnerFilterMixin,
                     viewsets.ModelViewSet):
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all().order_by('category__name').order_by('name')


class ScheduleViewSet(mixins.WithPermissionsMixin,
                      mixins.AuthOwnerFilterMixin,
                      viewsets.ModelViewSet):
    read_serializer_class = serializers.ScheduleReadSerializer
    write_serializer_class = serializers.ScheduleReadSerializer
    queryset = models.Schedule.objects.all().order_by('name')


class CustomerViewSet(mixins.WithPermissionsMixin,
                      mixins.AuthOwnerFilterMixin,
                      viewsets.ModelViewSet):
    serializer_class = serializers.CustomerSerializer

    def get_queryset(self):
        queryset = models.Customer.objects.all().order_by('first_name')

        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(first_name__icontains=search) |
                                       Q(last_name__icontains=search) |
                                       Q(email__icontains=search) |
                                       Q(phone__icontains=search))

        return queryset


class RequestViewSet(mixins.WithPermissionsMixin,
                     mixins.AuthOwnerFilterMixin,
                     viewsets.ModelViewSet):
    serializer_class = serializers.RequestSerializer

    def get_queryset(self):
        queryset = models.Request.objects.filter(complete=True).order_by('last_updated')

        serializer = serializers.RequestQuerySerlializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        if params.get('status') is not None:
            queryset = queryset.filter(_status=params.get('status'))

        return queryset

    @action(detail=True, methods=['patch'])
    def accept(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = models.Appointment.ACCEPTED
        serializer = self.get_read_serializer(instance)
        response = Response(serializer.data)
        # TODO: PENDING EMAIL
        return response

    @action(detail=True, methods=['patch'])
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = models.Appointment.REJECTED
        serializer = self.get_read_serializer(instance)
        response = Response(serializer.data)
        return response


class AppointmentViewSet(mixins.WithPermissionsMixin,
                         mixins.AuthOwnerFilterMixin,
                         mixins.QuerysetSerializerMixin,
                         viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.AppointmentReadSerializer
    queryset_serializer_class = serializers.AppointmentQuerySerlializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_write_serializer_class(self):
        if self.action in ('lock', 'plock'):
            return serializers.SelfAppointmentWriteSerializer
        return serializers.AppointmentWriteSerializer

    @action(detail=False, methods=['post'])
    def lock(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def plock(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def history(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.history.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.AppointmentHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.AppointmentHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        params = self.get_queryset_params()

        if params.get('show_all'):
            queryset = models.Appointment.objects.all_with_deleted()
        elif params.get('deleted_only'):
            queryset = models.Appointment.objects.deleted_only()
        else:
            queryset = models.Appointment.objects.all()

        # if a request reaches here and the user has no permission to view appointments
        # it means the user is an employee and
        # should only view appointments related to the employee of the user
        if not self.request.user.has_perm('scheduling.view_appointment') and self.request.user.employee_id is not None:
            queryset = queryset.filter(employee=self.request.user.employee_id)

        if params.get('employee') is not None:
            queryset = queryset.filter(employee=params.get('employee'))

        if params.get('employees') is not None:
            queryset = queryset.filter(employee_id__in=params.get('employees'))

        if params.get('services') is not None:
            queryset = queryset.filter(service_id__in=params.get('services'))

        from_date = params.get('from_date')
        to_date = params.get('to_date')
        if from_date is not None and to_date is None:
            queryset = queryset.filter(start__gte=from_date)

        if to_date is not None and from_date is None:
            queryset = queryset.filter(start__lte=to_date)

        if from_date is not None and to_date is not None:
            queryset = queryset.filter(Q(start__gte=from_date, start__lte=to_date) |
                                       Q(end__gte=from_date, end__lte=to_date) |
                                       Q(start__lte=from_date, end__gte=to_date))

        if params.get('customer') is not None:
            queryset = queryset.filter(customer=params.get('customer'))

        return queryset.order_by('start')


class CompanyViewSet(mixins.WithPermissionsMixin,
                     mixins.AuthOwnerFilterMixin,
                     viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()

    def get_write_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateCompanySerializer
        return self.serializer_class

    # TODO: Only verified users can write to the database
    def create(self, request, *args, **kwargs):
        r = super().create(request, *args, **kwargs)
        request.user.enable_company_editing(r.data.get('id'))
        return r

    @action(detail=True, methods=['patch'])
    def config(self, request, *args, **kwargs):
        instance = self.get_object().config
        serializer = serializers.ConfigSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def photo(self, request, pk=None):
        file = request.data.get('image')

        u = cloudinary_uploader.upload(file)

        instance = self.get_object()
        instance.avatar = CloudinaryResource(u['public_id'], u['format'], u['version'], u['signature'],
                                             type=u['type'], resource_type=u['resource_type'])
        instance.save()

        serializer = self.get_read_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='stripe', url_name='stripe')
    def post_stripe(self, request, *args, **kwargs):
        instance = self.get_object()
        stripe_id = instance.stripe_id()

        origin = self.request.headers['origin'] + '/admin/home'
        refresh_url = origin + reverse('company-stripe', kwargs={'pk': instance.id})

        account_link_url = stripe_helpers.generate_account_link(stripe_id, refresh_url, origin)
        try:
            return Response({'url': account_link_url})
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], url_path='stripe/details', url_name='stripe-details')
    def get_stripe(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_stripe_fields()
        serializer = serializers.StripeSerializer(instance)
        return Response(serializer.data)


class SchedulingPanelViewSet(mixins.WithPermissionsMixin,
                             mixins.AuthOwnerFilterMixin,
                             viewsets.ModelViewSet):
    serializer_class = serializers.SchedulingPanelSerializer
    queryset = models.SchedulingPanel.objects.all()
