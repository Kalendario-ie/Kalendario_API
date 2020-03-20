from core.models import User
from scheduling.models import *
from datetime import datetime, time

from scheduling.tests.generics import TestCaseWF
from scheduling.tests.util import next_monday, next_tuesday, book_appointment, reject_appointment


class ScheduleTest(TestCaseWF):

    def test_get_availability_scheduled_day(self):
        schedule = Schedule.objects.get(pk=1)
        availability = schedule.get_availability(date=datetime(2019, 7, 2))
        self.assertEquals(len(availability), 2)

        self.assertEquals(availability[0].start, time(9))
        self.assertEquals(availability[0].end, time(13, 00))

        self.assertEquals(availability[1].start, time(14))
        self.assertEquals(availability[1].end, time(17))

    def test_get_availability_unscheduled_day(self):
        schedule = Schedule.objects.get(pk=1)
        availability = schedule.get_availability(date=datetime(2019, 7, 1))
        self.assertEquals(len(availability), 0)


class AppointmentTest(TestCaseWF):

    def kwargs(self):
        return {
            'employee': Employee.objects.get(pk=1),
            'customer': Customer.objects.get(pk=5),
            'service': Service.objects.get(pk=1)
        }

    def test_add_appointment_unscheduled_day(self):
        kwargs = self.kwargs()
        kwargs['start'] = next_monday()
        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_add_appointment_scheduled_day_incorrect_time(self):
        """
        trying to schedule a 30 minutes job at 8 am when the schedule starts at 9 am
        this should throw an exception and not schedule anything
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=8, minute=0)
        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_add_appointment_scheduled_day_correct_time(self):
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_not_overlapping(self):
        """
        Two appointments where the start and end time are not overlapping and not close to each other should not
        cause issues
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_end_on_start(self):
        """
        When a appointment starts on the same minute another one has finished, this should not fail
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_start_on_end(self):
        """
        When a appointment ends on the same minute another one has started, this should not fail
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_same_time(self):
        """
        Two appointments on the exact same start / end time, the second should error and not create
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_appointment_starting_in_middle_of_another(self):
        """
        Two appointments where the second starts in the middle of the first, the second should error and not create
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=15)
        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_appointment_finishing_in_middle_of_another(self):
        """
        Two appointments where the second finishes in the middle of the first, the second should error and not create
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=15)
        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_appointment_on_a_service_not_provided_by_employee(self):
        """
        Booking an appointment against an employee with a service that employee doesn't provide should fail
        :return:
        """
        kwargs = self.kwargs()
        kwargs['start'] = next_tuesday().replace(hour=9, minute=30)
        kwargs['service'] = Service.objects.create(name='service B', duration=time(0, 30), owner_id=1)
        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_appointment_with_date_on_past(self):
        """
        Booking an appointment against an employee with a service that employee doesn't provide should fail
        :return:
        """
        kwargs = self.kwargs()
        kwargs['start'] = datetime.today()
        self.assertRaises(ModelCreationFailedException,
                          book_appointment,
                          **kwargs)

    def test_appointment_between_2_appointments_exact_times(self):
        """
        Booking an appointment that starts at another end and finishes at another start
        :return:
        """
        kwargs = self.kwargs()

        kwargs['start'] = next_tuesday().replace(hour=9, minute=0)
        self.assertIsInstance(book_appointment(**kwargs), Appointment)

        kwargs['start'] = next_tuesday().replace(hour=10, minute=0)
        self.assertIsInstance(book_appointment(**kwargs), Appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=30)
        self.assertIsInstance(book_appointment(**kwargs), Appointment)

    def test_appointment_finishing_in_middle_of_another_canceled(self):
        """
        Booking an appointment that starts at another end and finishes at another start
        :return:
        """
        kwargs = self.kwargs()

        kwargs['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)

        reject_appointment(appointment)

        kwargs['start'] = next_tuesday().replace(hour=9, minute=15)
        self.assertIsInstance(book_appointment(**kwargs), Appointment)

    def test_appointment_edit_end_time_variable(self):
        """
        When editing an appointment the end time should always be the start + service duration
        regardless of what value is inserted in end
        """
        kwargs = self.kwargs()

        kwargs['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**kwargs)
        self.assertIsInstance(appointment, Appointment)
        self.assertEqual(appointment.end, appointment.start + appointment.service.duration_delta())

        # Here we change the start time but not the end time
        new_start = appointment.start.replace(hour=10)
        appointment.start = new_start
        appointment.save()

        # After saving the end time should have changed
        self.assertEqual(appointment.end, appointment.start + appointment.service.duration_delta())


    def test_book_self_appointment(self):
        """TODO: self appointment should be possible, when this hapens the service field will be null"""
        pass

    def book_appointment_without_service(self):
        """TODO: only self appointments are allowed to have no service"""
        pass


class UserTest(TestCaseWF):

    def test_user_create_generates_person(self):
        user = User.objects.create(email='scheduler@email.com')
        self.assertTrue(hasattr(user, 'person'))


class PersonTest(TestCaseWF):

    def test_customer_employee_id_sequence(self):
        last_id = Person.objects.last().id
        company = Company.objects.first()
        customer = Customer(owner=company)
        emp = Employee(owner=company)
        customer.save(), emp.save()
        self.assertEqual(customer.id, last_id+1)
        self.assertEqual(emp.id, customer.id+1)
