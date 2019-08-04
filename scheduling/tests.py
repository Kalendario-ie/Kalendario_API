from django.test import TestCase
from scheduling.models import *
from datetime import datetime, time, timedelta, timezone

from scheduling.utility import get_availability_for_service


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
            name='Customer A',
            email='gustavo@email.com',
            phone='0988',
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


class ScheduleTest(TestCase):

    def setUp(self):
        schedule = add_schedule()
        self.assertIsNotNone(schedule)

    def test_get_availability_scheduled_day(self):
        schedule = Schedule.objects.filter(name='simple schedule').first()
        availability = schedule.get_availability(date=datetime(2019, 7, 2))
        self.assertEquals(len(availability), 2)

        self.assertEquals(availability[0].start, time(9))
        self.assertEquals(availability[0].end, time(13, 00))

        self.assertEquals(availability[1].start, time(14))
        self.assertEquals(availability[1].end, time(18))

    def test_get_availability_unscheduled_day(self):
        schedule = Schedule.objects.filter(name='simple schedule').first()
        availability = schedule.get_availability(date=datetime(2019, 7, 1))
        self.assertEquals(len(availability), 0)


class AppointmentTest(TestCase):

    def setUp(self):
        self.helper = TestHelper()

    def test_add_appointment_unscheduled_day(self):
        print('test_add_appointment_unscheduled_day')

        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          next_monday())

    def test_add_appointment_scheduled_day_incorrect_time(self):
        """
        trying to schedule a 30 minutes job at 8 am when the schedule starts at 9 am
        this should thorw an exception and not schedule anything
        """
        print('test_add_appointment_scheduled_day_incorrect_time')

        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          next_tuesday().replace(hour=8, minute=0))

    def test_add_appointment_scheduled_day_correct_time(self):
        print('test_add_appointment_scheduled_day_correct_time')

        appointment_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_date)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_not_overlapping(self):
        """
        Two appointments where the start and end time are not overlapping and not close to each other should not
        cause issues
        """
        print('test_two_appointments_not_overlapping')

        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        appointment_2_date = next_tuesday().replace(hour=9, minute=45)
        appointment = self.helper.book_appointment(appointment_2_date)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_end_on_start(self):
        """
        When a appointment starts on the same minute another one has finished, this should not fail
        """
        print('test_two_appointments_end_on_start')

        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        appointment_2_date = next_tuesday().replace(hour=9, minute=30)
        appointment = self.helper.book_appointment(appointment_2_date)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_start_on_end(self):
        """
        When a appointment ends on the same minute another one has started, this should not fail
        """
        print('test_two_appointments_start_on_end')

        appointment_1_date = next_tuesday().replace(hour=9, minute=30)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        appointment_2_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_2_date)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_same_time(self):
        """
        Two appointments on the exact same start / end time, the second should error and not create
        """
        print('test_two_appointments_same_time')

        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          appointment_1_date)

    def test_appointment_starting_in_middle_of_another(self):
        """
        Two appointments where the second starts in the middle of the first, the second should error and not create
        """
        print('test_appointment_starting_in_middle_of_another')

        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        appointment_2_date = next_tuesday().replace(hour=9, minute=15)
        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          appointment_2_date)

    def test_appointment_finishing_in_middle_of_another(self):
        """
        Two appointments where the second finishes in the middle of the first, the second should error and not create
        """
        print('test_appointment_finishing_in_middle_of_another')

        appointment_1_date = next_tuesday().replace(hour=9, minute=30)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        appointment_2_date = next_tuesday().replace(hour=9, minute=15)
        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          appointment_2_date)

    def test_appointment_on_a_service_not_provided_by_employee(self):
        """
        Booking an appointment against an employee with a service that employee doesn't provide should fail
        :return:
        """
        print('test_appointment_finishing_in_middle_of_another')

        appointment_1_date = next_tuesday().replace(hour=9, minute=30)
        service = Service.objects.create(name='service B', duration=time(0, 30))

        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment_with_service,
                          appointment_1_date,
                          service)

    def test_appointment_with_date_on_past(self):
        """
        Booking an appointment against an employee with a service that employee doesn't provide should fail
        :return:
        """
        print('test_appointment_with_date_on_past')

        appointment_1_date = datetime.today()
        print(appointment_1_date)
        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          appointment_1_date)


class SlotTest(TestCase):
    def setUp(self):
        self.helper = TestHelper()
        self.emp = self.helper.emp

    def get_slots(self, date):
        return get_availability_for_service(self.helper.emp, date, self.helper.service)

    def test_day_without_appointments(self):
        print("test_day_without_appointments", end="\n\n")

        slots = self.get_slots(next_wednesday())
        self.assertEqual(len(slots), 17)

        for slot in slots:
            self.assertEqual(slot.duration(), self.helper.service.duration_delta())

    def test_day_with_one_appointment_start_of_shift(self):
        print("test_day_with_one_appointment_start_of_shift", end="\n\n")

        appointment_1_date = next_wednesday().replace(hour=9, minute=00)
        self.helper.book_appointment(appointment_1_date)
        slots = self.get_slots(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.helper.service.duration_delta())

        self.assertEqual(len(slots), 16)

    def test_day_with_one_appointment_start_of_shift_1_offset(self):
        print("test_day_with_one_appointment_start_of_shift_1_offset", end="\n\n")

        appointment_1_date = next_wednesday().replace(hour=9, minute=30)
        self.helper.book_appointment(appointment_1_date)
        slots = self.get_slots(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.helper.service.duration_delta())

        self.assertEqual(len(slots), 16)

    def test_day_with_one_appointment_start_of_shift_half_time_offset(self):
        print("test_day_with_one_appointment_start_of_shift_half_time_offset", end="\n\n")

        appointment_1_date = next_wednesday().replace(hour=9, minute=15)
        self.helper.book_appointment(appointment_1_date)
        slots = self.get_slots(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.helper.service.duration_delta())

        self.assertEqual(len(slots), 15)

    def test_day_without_schedule(self):
        print('test_day_without_schedule', end='\n\n')

        slots = self.get_slots(next_monday())
        self.assertEqual(len(slots), 0)
