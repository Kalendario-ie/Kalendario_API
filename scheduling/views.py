import datetime

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from scheduling.availability import get_availability_for_service
from scheduling.customException import InvalidActionException
from scheduling.customer.serializers import CustomerSerializer
from scheduling.serializers import EmployeeSerializer, AppointmentReadSerializer, AppointmentWriteSerializer
from scheduling.models import Employee, Service, Appointment, Customer


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
        date = request.GET.get('date')
        if date is None:
            return HttpResponseBadRequest('date is required')

        service_id = request.GET.get('service')
        if service_id is None:
            return HttpResponseBadRequest('service is required')

        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return HttpResponseBadRequest('invalid employee id')

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return HttpResponseBadRequest('invalid service id')

        try:
            date = datetime.datetime.fromisoformat(date)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        try:
            slots = get_availability_for_service(employee, date, service)
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


class AppointmentViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

    authentication_classes = (TokenAuthentication, )

    def custom_queryset_filter(self, queryset):
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AppointmentReadSerializer
        return AppointmentWriteSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()

        queryset = self.custom_queryset_filter(queryset)

        customer = self.request.query_params.get('customer')
        if customer is not None:
            queryset = queryset.filter(customer=customer)

        employee = self.request.query_params.get('employee')
        if employee is not None:
            queryset = queryset.filter(employee=employee)

        from_date = self.request.query_params.get('from_date')
        if from_date is not None:
            queryset = queryset.filter(start__gte=from_date)

        to_date = self.request.query_params.get('to_date')
        if to_date is not None:
            queryset = queryset.filter(start__lte=to_date)

        return queryset
