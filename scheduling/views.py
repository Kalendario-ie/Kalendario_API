import datetime

from django.http import JsonResponse, HttpResponseForbidden
from rest_framework import viewsets

from scheduling.availability import get_availability_for_service
from scheduling.customException import InvalidActionException
from scheduling.serializers import EmployeeSerializer
from scheduling.models import Employee, Service


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


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
