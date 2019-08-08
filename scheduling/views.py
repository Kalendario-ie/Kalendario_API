from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from scheduling.customException import InvalidActionException
from scheduling.serializers import *
from scheduling.models import *

import datetime
from django.http import JsonResponse, HttpResponseForbidden

from scheduling.availability import get_availability_for_service


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AppointmentReadSerializer
        return AppointmentWriteSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()

        # employees and customers should only be able to see their own appointments
        if self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(employee_id=self.request.user.id)

        if not self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(customer_id=self.request.user.id)

        employee = self.request.query_params.get('employee')
        if employee is not None:
            queryset = queryset.filter(employee=employee)

        year = self.request.query_params.get('year')
        if year is not None:
            queryset = queryset.filter(start__year=year)

        month = self.request.query_params.get('month')
        if month is not None:
            queryset = queryset.filter(start__month=month)

        day = self.request.query_params.get('day')
        if day is not None:
            queryset = queryset.filter(start__day=day)

        from_date = self.request.query_params.get('from_date')
        if from_date is not None:
            queryset = queryset.filter(start__gte=from_date)

        to_date = self.request.query_params.get('to_date')
        if to_date is not None:
            queryset = queryset.filter(start__lte=to_date)

        customer = self.request.query_params.get('customer')
        if customer is not None:
            queryset = queryset.filter(customer__id=customer)

        return queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


def slot_list(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    employee_id = request.GET.get('employee')
    service_id = request.GET.get('service')

    employee = Employee.objects.get(id=employee_id)
    service = Service.objects.get(id=service_id)

    date = datetime.datetime(int(year), int(month), int(day))

    try:
        slots = get_availability_for_service(employee, date, service)
        slots = list(map(lambda slot: slot.__dict__(), slots))
        # TODO: find way to return list without having to set safe to false
        return JsonResponse(slots, safe=False)
    except InvalidActionException as e:
        return HttpResponseForbidden(str(e))


