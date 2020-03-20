import datetime
from django.db import models
from scheduling.customException import ModelCreationFailedException


class AppointmentManager(models.Manager):
    def create(self, *args, **kwargs):
        employee = kwargs['employee']
        start = kwargs['start'] = kwargs['start'].replace(second=0, microsecond=0)

        service = kwargs.get('service')
        if not service and employee.id != kwargs['customer'].id:
            raise ModelCreationFailedException(r"A service must be provided")

        if service and not employee.provides_service(service):
            raise ModelCreationFailedException(r"Employee doesn't provide this service")

        if service:
            kwargs['end'] = kwargs['start'] + service.duration_delta()

        kwargs['end'] = kwargs['end'].replace(second=0, microsecond=0)

        if start <= datetime.datetime.now():
            raise ModelCreationFailedException(r'Date can\'t be on the past')

        if not employee.is_available(start, kwargs['end']):
            raise ModelCreationFailedException(r'No time available for the date selected')

        return super().create(*args, **kwargs)


class EmployeeManager(models.Manager):
    def create(self, *args, **kwargs):
        user = kwargs['user']
        user.is_staff = True
        return super().create(*args, **kwargs)
