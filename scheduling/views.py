from django.http import HttpResponseForbidden
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from scheduling.availability import get_availability_for_service
from scheduling.customException import InvalidActionException
from scheduling.permissions import IsEmployee
from scheduling.serializers import EmployeeSerializer, AppointmentReadSerializer, SlotSerializer, CustomerSerializer, \
    SelfAppointmentWriteSerializer, AppointmentWriteSerializer, SelfAppointmentReadSerializer
from scheduling.models import Employee, Appointment, Customer, SelfAppointment


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        if request.user.is_employee():
            serializer = self.get_serializer(request.user.employee)
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


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = self.get_queryset()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(first_name__istartswith=search)
        result = list(map(lambda x: {'id': x.id, 'name': x.name()}, queryset))
        return Response(result)


class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )

    def request_data(self):
        return self.request.data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request_data())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def custom_queryset_filter(self, queryset):
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AppointmentReadSerializer
        return AppointmentWriteSerializer

    def get_queryset(self):
        queryset = base_appointment_filter(Appointment.objects.all(), self.request.query_params)

        queryset = self.custom_queryset_filter(queryset)

        customer = self.request.query_params.get('customer')
        if customer is not None:
            queryset = queryset.filter(customer=customer)

        param_status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=param_status)

        return queryset


class SelfAppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, IsEmployee)

    def request_data(self):
        data = self.request.data.copy()
        if not self.request.user.has_perm('scheduling.change_appointment'):
            data['employee'] = self.request.user.employee.id
        return data

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SelfAppointmentReadSerializer
        return SelfAppointmentWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request_data())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return base_appointment_filter(SelfAppointment.objects.all(), self.request.query_params)


def base_appointment_filter(queryset, query_params):
    employee = query_params.get('employee')
    if employee is not None:
        queryset = queryset.filter(employee=employee)

    from_date = query_params.get('from_date')
    if from_date is not None:
        queryset = queryset.filter(start__gte=from_date)

    to_date = query_params.get('to_date')
    if to_date is not None:
        queryset = queryset.filter(start__lte=to_date)

    return queryset
