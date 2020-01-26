from django.test import TestCase

from core.models import User
from scheduling.models import *
from datetime import datetime, time

from scheduling.tests.util import next_monday, next_tuesday, schedule_a, TestHelper, reject_appointment, tearDown


class ScheduleTest(TestCase):

    def setUp(self):
        schedule = schedule_a()
        self.assertIsNotNone(schedule)

    def test_get_availability_scheduled_day(self):
        schedule = Schedule.objects.filter(name='simple schedule').first()
        availability = schedule.get_availability(date=datetime(2019, 7, 2))
        self.assertEquals(len(availability), 2)

        self.assertEquals(availability[0].start, time(9))
        self.assertEquals(availability[0].end, time(13, 00))

        self.assertEquals(availability[1].start, time(14))
        self.assertEquals(availability[1].end, time(17))

    def test_get_availability_unscheduled_day(self):
        schedule = Schedule.objects.filter(name='simple schedule').first()
        availability = schedule.get_availability(date=datetime(2019, 7, 1))
        self.assertEquals(len(availability), 0)


class AppointmentTest(TestCase):

    def setUp(self):
        self.helper = TestHelper()

    def tearDown(self):
        tearDown()

    def test_add_appointment_unscheduled_day(self):
        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          next_monday())

    def test_add_appointment_scheduled_day_incorrect_time(self):
        """
        trying to schedule a 30 minutes job at 8 am when the schedule starts at 9 am
        this should throw an exception and not schedule anything
        """
        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          next_tuesday().replace(hour=8, minute=0))

    def test_add_appointment_scheduled_day_correct_time(self):
        appointment_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_date)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_not_overlapping(self):
        """
        Two appointments where the start and end time are not overlapping and not close to each other should not
        cause issues
        """
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
        appointment_1_date = datetime.today()
        self.assertRaises(ModelCreationFailedException,
                          self.helper.book_appointment,
                          appointment_1_date)

    def appointment_between_2_appointments_exact_times(self):
        """
        Booking an appointment that starts at another end and finishes at another start
        :return:
        """
        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        appointment_2_date = next_tuesday().replace(hour=10, minute=0)
        appointment2 = self.helper.book_appointment(appointment_2_date)
        self.assertIsInstance(appointment2, Appointment)

        appointment_3_date = next_tuesday().replace(hour=9, minute=30)
        appointment3 = self.helper.book_appointment(appointment_3_date)
        self.assertIsInstance(appointment3, Appointment)

    def test_appointment_finishing_in_middle_of_another_canceled(self):
        """
        Booking an appointment that starts at another end and finishes at another start
        :return:
        """
        appointment_1_date = next_tuesday().replace(hour=9, minute=30)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)

        reject_appointment(appointment)

        appointment_2_date = next_tuesday().replace(hour=9, minute=15)
        appointment2 = self.helper.book_appointment(appointment_2_date)
        self.assertIsInstance(appointment2, Appointment)

    def test_appointment_edit_end_time_variable(self):
        """
        When editing an appointment the end time should always be the start + service duration
        regardless of what value is inserted in end
        """
        appointment_1_date = next_tuesday().replace(hour=9, minute=30)
        appointment = self.helper.book_appointment(appointment_1_date)
        self.assertIsInstance(appointment, Appointment)
        self.assertEqual(appointment.end, appointment.start + appointment.service.duration_delta())

        # Here we change the start time but not the end time
        new_start = appointment.start.replace(hour=10)
        appointment.start = new_start
        appointment.save()

        # After saving the end time should have changed
        self.assertEqual(appointment.end, appointment.start + appointment.service.duration_delta())


class UserTest(TestCase):

    def test_user_create_generates_person(self):
        user = User.objects.create(email='scheduler@email.com')
        self.assertTrue(hasattr(user, 'person'))
