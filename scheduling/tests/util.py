from datetime import *

from django.contrib.auth.models import Permission, Group

from core.models import User
from scheduling.models import Shift, TimeFrame, Schedule, Service, Employee, Person, Appointment, Company


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

        self.comp1 = Company.objects.create(name='company 1')
        self.comp2 = Company.objects.create(name='company 2')

        self.employees = [create_employee('c1e1@email.com', schedule, self.comp1, [self.service]),
                          create_employee('c1e2@email.com', schedule, self.comp1, [self.service]),
                          create_employee('c2e1@email.com', schedule, self.comp2, [self.service]),
                          create_employee('c2e2@email.com', schedule, self.comp2, [self.service])]

        self.admins = [create_employee('c1e3@email.com', schedule, self.comp1, [self.service], True)]

        self.customers = [create_customer('c1@test.com'),
                          create_customer('c2@test.com'),
                          create_customer('c3@test.com')]

        self.appointments = []

        for emp in self.employees:
            service = emp.services.first()
            start = next_wednesday().replace(hour=9, minute=00)
            for customer in self.customers:
                self.appointments.append(book_appointment(emp, customer, service, start))
                start = start + service.duration_delta()

    def book_appointment_with_service(self, start, service):
        print('Booking a {time} service appointment on {date}'.format(time=self.service.duration, date=start))
        try:
            appointment = Appointment.objects.create(start=start,
                                                     service=service,
                                                     customer=self.customers[0],
                                                     employee=self.employees[0])
        except Exception as e:
            print('failed to create appointment: ' + str(e), end='\n\n')
            raise

        print('appointment created: ' + str(appointment), end='\n\n')

        return appointment

    def book_appointment(self, start):
        return self.book_appointment_with_service(start, self.service)


def create_employee(email, schedule, company, services, is_admin=False):
    emp = Employee.objects.create(first_name='j', last_name='b', schedule=schedule, company=company,
                                  company_admin=is_admin)
    [emp.services.add(service) for service in services], emp.save()
    User.objects.create(email=email, person=emp)
    return emp


def create_customer(email):
    customer = Person.objects.create(first_name='Customer', last_name='second')
    customer.user = User.objects.create(email=email)
    customer.user.set_password('Customer2Pass'), customer.user.save()
    return customer


def book_appointment(emp, customer, service, start):
    return Appointment.objects.create(customer=customer, employee=emp, service=service, start=start)
