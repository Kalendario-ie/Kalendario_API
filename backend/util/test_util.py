from datetime import *

from django.contrib.auth.models import Permission

from scheduling.models import Shift, TimeFrame, Schedule, Appointment
from core.models import GroupProfile


def next_monday():
    today = datetime.now()
    return today + timedelta(7 - today.weekday())


def next_tuesday(modifier=0):
    today = datetime.now()
    return today + timedelta(8 - today.weekday()) + timedelta(modifier)


def next_wednesday():
    today = datetime.now()
    return today + timedelta(9 - today.weekday())


def tomorrow():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)


def schedule_a(comp):
    shift_a = Shift.objects.create(owner=comp)
    TimeFrame.objects.create(start=time(9), end=time(17, 30), shift=shift_a)

    shift_b = Shift.objects.create(owner=comp)
    TimeFrame.objects.create(start=time(9), end=time(13, 00), shift=shift_b)
    TimeFrame.objects.create(start=time(14), end=time(17, 00), shift=shift_b)

    return Schedule.objects.create(
        owner=comp,
        name='simple schedule',
        tue=shift_b,
        wed=shift_a,
        thu=shift_a,
        fri=shift_a,
        sat=shift_a,
        sun=shift_a
    )


def reject_appointment(appointment):
    appointment.status = appointment.REJECTED
    appointment.save()


def book_appointment(employee, customer=None, start=None, service=None, end=None, ignore_availability=False):
    if service is not None:
        end = start + service.duration
    return Appointment.objects.create(start=start,
                                      end=end,
                                      service=service,
                                      customer=customer,
                                      employee=employee,
                                      owner=employee.owner,
                                      ignore_availability=ignore_availability)


def company_1_master_group():
    group = GroupProfile.objects.create(owner_id=1, name='Master')
    permissions = Permission.objects.filter(codename__endswith='appointment')
    group.permissions.add(*permissions)
    group.save()
    return group.group


def add_permissions(user, model):
    user.user_permissions.add(*Permission.objects.all().filter(codename__endswith=model))
