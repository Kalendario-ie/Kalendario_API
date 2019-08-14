from datetime import *

from core.models import User
from scheduling.models import Shift, TimeFrame, Schedule, Service, Employee, Customer, Appointment


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


class TestHelper:

    def __init__(self):
        self.service = Service.objects.create(name='service A', duration=time(0, 30))

        schedule = schedule_a()

        user = User.objects.create(email='employee@email.com')

        self.employeeA = Employee.objects.create(
            schedule=schedule,
            user=user
        )
        self.employeeA.services.add(self.service)
        self.employeeA.save()

        c1 = Customer.objects.create(email='c1@email.com')
        c1.set_password('1234')
        c1.save()
        self.customerA = c1
        c2 = Customer.objects.create(email='c2@email.com')
        c2.set_password('1234')
        c2.save()
        self.customerB = c2

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

    def tearDown(self):
        Appointment.objects.all().delete()
        Employee.objects.all().delete()
        Customer.objects.all().delete()
        Schedule.objects.all().delete()
        Shift.objects.all().delete()
