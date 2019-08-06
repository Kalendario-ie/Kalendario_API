from datetime import *

from scheduling.models import Shift, TimeFrame, Schedule, Service, Employee, Customer, Appointment


def next_monday():
    today = datetime.now(timezone.utc)
    return today + timedelta(7 - today.weekday())


def next_tuesday():
    today = datetime.now(timezone.utc)
    return today + timedelta(9 - today.weekday())


def next_wednesday():
    today = datetime.now(timezone.utc)
    return today + timedelta(9 - today.weekday())


def add_schedule():
    shift_a = Shift.objects.create()
    TimeFrame.objects.create(start=time(9), end=time(17, 30), shift=shift_a)

    shift_b = Shift.objects.create()
    TimeFrame.objects.create(start=time(9), end=time(13, 00), shift=shift_b)
    TimeFrame.objects.create(start=time(14), end=time(18, 00), shift=shift_b)

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

        schedule = add_schedule()

        self.emp = Employee.objects.create(
            name='Employee A',
            email='gustavo@email.com',
            phone='0988',
            schedule=schedule,
        )
        self.emp.services.add(self.service)
        self.emp.save()

        self.customer = Customer.objects.create(
            first_name='Customer',
            email='gustavo@email.com',
        )

    def book_appointment_with_service(self, start, service):
        print('Booking a {time} service appointment on {date}'.format(time=self.service.duration, date=start))
        try:
            appointment = Appointment.objects.create(start=start,
                                                     service=service,
                                                     customer=self.customer,
                                                     employee=self.emp)
        except Exception as e:
            print('failed to create appointment: ' + str(e), end='\n\n')
            raise

        print('appointment created: ' + str(appointment), end='\n\n')

        return appointment

    def book_appointment(self, start):
        return self.book_appointment_with_service(start, self.service)

    def tearDown(self):
        Customer.objects.all().delete()