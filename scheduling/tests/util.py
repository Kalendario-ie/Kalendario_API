from datetime import *

from django.contrib.auth.models import Permission, Group

from core.models import User
from scheduling.models import Shift, TimeFrame, Schedule, Service, Employee, Person, Appointment


def next_monday():
    today = datetime.now()
    return today + timedelta(7 - today.weekday())


def next_tuesday():
    today = datetime.now()
    return today + timedelta(8 - today.weekday())


def next_wednesday():
    today = datetime.now()
    return today + timedelta(9 - today.weekday())


def tomorrow():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)


def schedule_a():
    shift_a = Shift.objects.create()
    TimeFrame.objects.create(start=time(9), end=time(17, 30), shift=shift_a)

    shift_b = Shift.objects.create()
    TimeFrame.objects.create(start=time(9), end=time(13, 00), shift=shift_b)
    TimeFrame.objects.create(start=time(14), end=time(17, 00), shift=shift_b)

    return Schedule.objects.create(
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


def tearDown():
    Appointment.objects.all().delete()
    Employee.objects.all().delete()
    Person.objects.all().delete()
    Schedule.objects.all().delete()
    Shift.objects.all().delete()
    User.objects.all().delete()
    Group.objects.all().delete()


class TestHelper:

    def __init__(self):
        self.service = Service.objects.create(name='service A', duration=time(0, 30))

        permissions = Permission.objects.all().filter(codename__endswith='appointment')
        schedulers_pg = Group.objects.create(name='schedulers')
        for permission in permissions:
            schedulers_pg.permissions.add(permission)

        scheduler = User.objects.create(email='scheduler@email.com')
        scheduler.set_password('SchedulerPassword')
        scheduler.groups.add(schedulers_pg)
        scheduler.save()
        self.scheduler = scheduler

        schedule = schedule_a()

        emp_a_user = User.objects.create(email='emp_a@email.com')
        self.employeeA = Employee.objects.create(
            first_name='Joe',
            last_name='Bloggs',
            schedule=schedule,
            user=emp_a_user
        )
        self.employeeA.services.add(self.service)
        self.employeeA.save()

        emp_b_user = User.objects.create(email='emp_b@email.com')
        self.employeeB = Employee.objects.create(
            first_name='jane',
            last_name='Doe',
            schedule=schedule,
            user=emp_b_user
        )
        self.employeeB.services.add(self.service)
        self.employeeB.save()

        self.customerA = Person.objects.create(first_name='Customer', last_name='first')
        c1_user = User.objects.create(email='c1@test.com')
        c1_user.set_password('Customer1Pass')
        c1_user.save()
        self.customerA.user = c1_user

        self.customerB = Person.objects.create(first_name='Customer', last_name='second')
        c2_user = User.objects.create(email='c2@test.com')
        c2_user.set_password('Customer2Pass')
        c2_user.save()
        self.customerB.user = c2_user

    def book_appointment_with_service(self, start, service):
        print('Booking a {time} service appointment on {date}'.format(time=self.service.duration, date=start))
        try:
            print(self.employeeA.schedule)
            appointment = Appointment.objects.create(start=start,
                                                     service=service,
                                                     customer=self.customerA,
                                                     employee=self.employeeA)
        except Exception as e:
            print('failed to create appointment: ' + str(e), end='\n\n')
            raise

        print('appointment created: ' + str(appointment), end='\n\n')

        return appointment

    def book_appointment(self, start):
        return self.book_appointment_with_service(start, self.service)
