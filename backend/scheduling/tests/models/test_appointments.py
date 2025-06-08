from datetime import timedelta, datetime

from django.core.exceptions import ValidationError

from scheduling.models import Employee, Customer, Service, Appointment
from scheduling.tests.generics import TestCaseWF
from util.test_util import next_tuesday, book_appointment, next_monday, reject_appointment


class AppointmentTest(TestCaseWF):

    def data(self):
        return {
            'employee': Employee.objects.get(pk=1),
            'customer': Customer.objects.get(pk=1001),
            # Service: owner 1, duration 30 min
            'service': Service.objects.get(pk=1)
        }

    def test_add_appointment_with_service_and_no_customer(self):
        """This should throw an error as the appointment must have a customer"""
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        del(data['service'])
        self.assertRaises(ValidationError, book_appointment, **data)

    def test_add_appointment_scheduled_day_correct_time(self):
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

    def test_add_appointment_scheduled_day_incorrect_time(self):
        """
        trying to schedule a 30 minutes job at 8 am when the schedule starts at 9 am
        this should throw an exception and not schedule anything
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=8, minute=0)
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_add_appointment_unscheduled_day(self):
        data = self.data()
        data['start'] = next_monday()
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_two_appointments_not_overlapping(self):
        """
        Two appointments where the start and end time are not overlapping and not close to each other should not
        cause issues
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_start_on_end_of_previous(self):
        """
        Appointment starts on the same minute another one has finished
        Should create Appointment
        """
        data = self.data()
        # Starts at 9 finishes at 9:30
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        # Starts at 9:30 (the end of previous appointment)
        data['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_start_a_minute_before_end_of_previous(self):
        """
        Appointment starts a minute before previous appointment has finished
        Should Fail
        """
        data = self.data()
        # Starts at 9 finishes at 9:30
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        # Starts at 9:29 (the end of previous appointment)
        data['start'] = next_tuesday().replace(hour=9, minute=29)
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_two_appointments_start_a_minute_before_end_of_previous_ignore_availability_true(self):
        """
        Appointment starts a minute before previous appointment has finished
        with ignore_availability set to True
        Should create appointment
        """
        data = self.data()
        # Starts at 9 finishes at 9:30
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        # Starts at 9:29 (the end of previous appointment)
        data['start'] = next_tuesday().replace(hour=9, minute=29)
        appointment = book_appointment(**data, ignore_availability=True)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_end_on_start_of_previous(self):
        """
        When a appointment ends on the same minute another one has started
        this should not fail
        """
        data = self.data()
        # Start at 9:45
        data['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        # Starts at 9:15 finishes at 9:45 (start of previous appointment)
        data['start'] = next_tuesday().replace(hour=9, minute=15)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

    def test_appointment_end_a_minute_after_next_starts(self):
        """
        Two appointments where the second finishes a minute after the previous started
        Should raise Validation Error
        """
        data = self.data()
        # Start at 9:45
        data['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        # Starts at 9:16 finishes at 9:46 (a minute after previous started)
        data['start'] = next_tuesday().replace(hour=9, minute=16)
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_appointment_end_a_minute_after_next_starts_ignore_availability_true(self):
        """
        Two appointments where the second finishes a minute after the previous started
        Should raise Validation Error
        """
        data = self.data()
        # Start at 9:45
        data['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        # Starts at 9:16 finishes at 9:46 (a minute after previous started)
        data['start'] = next_tuesday().replace(hour=9, minute=16)
        appointment = book_appointment(**data, ignore_availability=True)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_same_time(self):
        """
        Two appointments on the exact same start / end time, the second should error and not create
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_appointment_on_a_service_not_provided_by_employee(self):
        """
        Booking an appointment against an employee with a service that employee doesn't provide should fail
        :return:
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=30)
        data['service'] = Service.objects.create(name='service B', duration=timedelta(hours=0, minutes=30), owner_id=1)
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_appointment_with_date_on_past(self):
        """
        Booking an appointment against an employee with a service that employee doesn't provide should fail
        :return:
        """
        data = self.data()
        data['start'] = datetime.today()
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_appointment_between_2_appointments_exact_times(self):
        """
        Booking an appointment that starts at another end and finishes at another start
        :return:
        """
        print('test_appointment_between_2_appointments_exact_times')
        data = self.data()

        data['start'] = next_tuesday().replace(hour=9, minute=0)
        self.assertIsInstance(book_appointment(**data), Appointment)

        data['start'] = next_tuesday().replace(hour=10, minute=0)
        self.assertIsInstance(book_appointment(**data), Appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=30)
        self.assertIsInstance(book_appointment(**data), Appointment)

    def test_appointment_finishing_in_middle_of_another_canceled(self):
        """
        Booking an appointment that starts at another end and finishes at another start
        :return:
        """
        data = self.data()

        data['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        reject_appointment(appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=15)
        self.assertIsInstance(book_appointment(**data), Appointment)

    def test_book_self_appointment(self):
        """self appointment should be possible, when this happens the service field will be null"""
        employee = self.data()['employee']
        appointment = Appointment.objects.create(start=next_tuesday().replace(hour=9, minute=0),
                                                 end=next_tuesday().replace(hour=10, minute=0),
                                                 employee=employee,
                                                 owner=employee.owner)
        self.assertIsInstance(appointment, Appointment)

    def test_book_appointment_without_service(self):
        """Only self appointment can be created without services"""
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        data['end'] = next_tuesday().replace(hour=10, minute=0)
        del (data['service'])

        self.assertRaises(ValidationError, book_appointment, **data)

    def test_appointment_with_service_and_employees_on_different_owner(self):
        """
        An error should be raised when creating an appointment where the service and the employee have different owners
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        data['service'] = Service.objects.get(pk=3)

        self.assertRaises(ValidationError, book_appointment, **data)

    def test_appointment_with_customer_and_employees_on_different_owner(self):
        """
        An error should be raised when creating an appointment where the service and the employee have different owners
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        data['customer'] = Customer.objects.get(pk=1003)

        self.assertRaises(ValidationError, book_appointment, **data)

    def test_delete_appointments_should_not_show_on_all_queryset(self):
        """
        The normal objects.all should not return safe deleted appointments
        :return:
        """
        before = [*Appointment.objects.all()]
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        created = book_appointment(**data)
        after_create = [*Appointment.objects.all()]
        self.assertEqual(len(before) + 1, len(after_create))
        created.delete()
        after_delete = [*Appointment.objects.all()]
        self.assertEqual(len(before), len(after_delete))

    def test_delete_appointments_should_show_on_all_with_deleted_queryset(self):
        """
        objecsts.all_with_deleted should return safe deleted appointments
        :return:
        """
        before = [*Appointment.objects.all_with_deleted()]
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        created = book_appointment(**data)
        after_create = [*Appointment.objects.all_with_deleted()]
        self.assertEqual(len(before) + 1, len(after_create))
        created.delete()
        after_delete = [*Appointment.objects.all_with_deleted()]
        self.assertEqual(len(after_create), len(after_delete))

    def test_hard_delete_appointments_should_not_show_on_all_with_deleted_queryset(self):
        """
        objecsts.all_with_deleted should not return hard deleted appointments
        :return:
        """
        before = [*Appointment.objects.all_with_deleted()]
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        created = book_appointment(**data)
        after_create = [*Appointment.objects.all_with_deleted()]
        self.assertEqual(len(before) + 1, len(after_create))
        created.hard_delete()
        after_delete = [*Appointment.objects.all_with_deleted()]
        self.assertEqual(len(before), len(after_delete))

    def test_soft_delete_appointment_overlapping(self):
        """
        Two appointments where the second finishes a minute after the previous started
        Should raise Validation Error
        """
        data = self.data()
        # Start at 9:45
        data['start'] = next_tuesday().replace(hour=9, minute=45)
        a1 = book_appointment(**data)
        self.assertIsInstance(a1, Appointment)

        # Starts at 9:16 finishes at 9:46 (a minute after previous started)
        data['start'] = next_tuesday().replace(hour=9, minute=16)
        a2 = book_appointment(**data, ignore_availability=True)
        self.assertIsInstance(a2, Appointment)
        # the bellow should not throw an error
        a2.delete()