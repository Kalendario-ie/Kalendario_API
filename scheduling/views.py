from django.http import HttpResponseForbidden
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scheduling.availability import get_availability_for_service
from scheduling.customException import InvalidActionException
from scheduling.permissions import IsEmployee
from scheduling.serializers import EmployeeSerializer, AppointmentReadSerializer, SlotSerializer, CustomerSerializer, \
    SelfAppointmentWriteSerializer, AppointmentWriteSerializer, SelfAppointmentReadSerializer, \
    CustomerAppointmentWriteSerializer, EmployeeAppointmentWriteSerializer, AppointmentQuerySerlializer
from scheduling.models import Employee, Appointment, Customer, SelfAppointment


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        if request.user.is_employee():
            serializer = self.get_serializer(request.user.person.employee)
            return Response(serializer.data)

        return HttpResponseForbidden({'error': 'not an employee'})

    @action(detail=True, methods=['get'])
    def slots(self, request, pk=None):
        serializer = SlotSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        try:
            slots = get_availability_for_service(**serializer.validated_data, employee=self.get_object())
            slots = list(map(lambda slot: slot.__dict__(), slots))
            return Response(slots)
        except InvalidActionException as e:
            return HttpResponseForbidden(str(e))


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 300


class CustomerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsEmployee)

    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Customer.objects.all()

        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(first_name__istartswith=search)

        return queryset


class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def request_data(self):
        return self.request.data

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            if self.request.user.is_customer():
                return CustomerAppointmentWriteSerializer
            if self.request.user.is_employee():
                return EmployeeAppointmentWriteSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return AppointmentReadSerializer
        return AppointmentWriteSerializer

    def get_queryset(self):
        serializer = AppointmentQuerySerlializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        queryset = base_appointment_filter(Appointment.objects.all(), params)

        customer = key_or_none(params, 'customer')
        if customer is not None:
            queryset = queryset.filter(customer=customer)

        param_status = key_or_none(params, 'status')
        if param_status is not None:
            queryset = queryset.filter(status=param_status)

        if self.request.user.is_customer():
            queryset = queryset.filter(customer_id=self.request.user.person.id)

        if self.request.user.is_employee():
            queryset = queryset.filter(employee_id=self.request.user.person.id)

        return queryset

    def create(self, request, *args, **kwargs):
        if self.request.user.has_perm('scheduling.change_appointment'):
            return super().create(request, args, kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user

        # Customers should only be able to book appointment for themselves
        if user.is_customer() and serializer.validated_data['customer'].id != user.person.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Employees should only be able to book appointment for themselves
        if user.is_employee() and serializer.validated_data['employee'].id != user.person.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SelfAppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsEmployee)

    def create(self, request, *args, **kwargs):
        if self.request.user.has_perm('scheduling.change_appointment'):
            return super().create(request, args, kwargs)
        user, data = self.request.user, self.request.data
        if user.is_employee() and 'employee' in data and data['employee'] != user.person.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, args, kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SelfAppointmentReadSerializer
        return SelfAppointmentWriteSerializer

    def get_queryset(self):
        queryset = base_appointment_filter(SelfAppointment.objects.all(), self.request.query_params)

        if self.request.user.is_employee() and not self.request.user.has_perm('scheduling.view_appointment'):
            queryset = queryset.filter(employee_id=self.request.user.person.id)

        return queryset


def base_appointment_filter(queryset, params):
    employee = key_or_none(params, 'employee')
    if employee is not None:
        queryset = queryset.filter(employee=employee)

    from_date = key_or_none(params, 'from_date')
    if from_date is not None:
        queryset = queryset.filter(start__gte=from_date)

    to_date = key_or_none(params, 'to_date')
    if to_date is not None:
        queryset = queryset.filter(start__lte=to_date)

    return queryset


def key_or_none(values, key):
    return values[key] if key in values else None
