from django.http import HttpResponseForbidden

from drf_rw_serializers.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scheduling.permissions import CanCreateAppointment, CanCreateCompany
from scheduling.availability import get_availability_for_service
from scheduling.customException import InvalidActionException
from scheduling import serializers
from scheduling.models import Appointment, Employee, Company
from scheduling import permissions as cp

from drf_rw_serializers import viewsets
from django.db.models import Q


class EmployeeViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()

        if self.action == 'slots':
            return queryset

        company = self.request.query_params.get('company')
        if company is None:
            return None
        queryset = queryset.filter(owner__name=company)
        return queryset

    @action(detail=False, methods=['get'])
    def current(self, request):
        if request.user.is_employee():
            serializer = self.get_serializer(request.user.person.employee)
            return Response(serializer.data)
        return HttpResponseForbidden({'error': 'not an employee'})

    @action(detail=True, methods=['get'])
    def slots(self, request, pk=None):
        serializer = serializers.SlotSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            slots = get_availability_for_service(**serializer.validated_data, employee=self.get_object())
            slots = list(map(lambda slot: slot.__dict__(), slots))
            return Response(slots)
        except InvalidActionException as e:
            return HttpResponseForbidden(str(e))


class CompanyViewSet(viewsets.ModelViewSet):
    read_serializer_class = serializers.CompanyReadSerializer
    write_serializer_class = serializers.CompanyWriteSerializer

    def get_queryset(self):
        queryset = Company.objects.all()
        params = self.request.query_params
        name = params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

    def get_permissions(self):
        permission_classes = [cp.IsOwnerOrReadOnly]

        if self.action in ['create', 'update']:
            permission_classes.append(IsAuthenticated)
        if self.action == 'create':
            permission_classes.append(CanCreateCompany)

        return [perm() for perm in permission_classes]

    def create(self, request, *args, **kwargs):
        r = super().create(request, *args, **kwargs)
        request.user.company_id = r.data.get('id')
        request.user.enable_company_editing()
        return r


class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.AppointmentReadSerializer
    write_serializer_class = serializers.AppointmentWriteSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]

        if self.action == 'create':
            permission_classes.append(CanCreateAppointment)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        serializer = serializers.AppointmentQuerySerlializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        queryset = Appointment.objects.all()

        if params.get('employee') is not None:
            queryset = queryset.filter(employee=params.get('employee'))

        if params.get('from_date') is not None:
            queryset = queryset.filter(start__gte=params.get('from_date'))

        if params.get('to_date') is not None:
            queryset = queryset.filter(start__lte=params.get('to_date'))

        if params.get('customer') is not None:
            queryset = queryset.filter(customer=params.get('customer'))

        if params.get('status') is not None:
            queryset = queryset.filter(status=params.get('status'))

        if self.request.user.has_company() and self.request.user.has_perm('scheduling.view_appointment'):
            queryset = queryset.filter(employee__owner_id=self.request.user.company_id)
        else:
            queryset = queryset.filter(Q(customer_id=self.request.user.person.id) |
                                       Q(employee_id=self.request.user.person.id))

        return queryset
