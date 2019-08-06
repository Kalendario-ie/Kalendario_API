from django.test import TestCase
from scheduling.models import *
from datetime import datetime, time

from scheduling.tests.util import next_monday, next_tuesday, add_schedule, TestHelper


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


