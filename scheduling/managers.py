import datetime

from django.db import models

from core.managers import UserManager
from scheduling.customException import ModelCreationFailedException


class AppointmentManager(models.Manager):
    def create(self, *args, **kwargs):
        employee = kwargs['employee']
        service = kwargs['service']
        start = kwargs['start'] = kwargs['start'].replace(second=0, microsecond=0)
        end = start + service.duration_delta()

        if start.date() <= datetime.date.today():
            raise ModelCreationFailedException(r'Date can\'t be on the past')

        if not employee.provides_service(service):
            raise ModelCreationFailedException(r'Employee doesn\'t provide this service')

        if not employee.is_available(start, end):
            raise ModelCreationFailedException(r'No time available for the date selected')

        return super().create(*args, **kwargs)


class CustomerManager(UserManager):

    def all(self):
        return super().all().filter(is_staff=False, is_superuser=False)


class EmployeeManager(models.Manager):
    def create(self, *args, **kwargs):
        user = kwargs['user']
        user.is_staff = True
        return super().create(*args, **kwargs)
