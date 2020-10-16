from core.models import User
from scheduling.models import *
from scheduling import exceptions
from datetime import datetime, time, timedelta

from scheduling.tests.generics import TestCaseWF
from scheduling.tests.util import next_monday, next_tuesday, book_appointment, reject_appointment

from django.core.exceptions import ValidationError

from django.db.utils import IntegrityError


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

    def test_changing_shift_same_owner(self):
        """
        Should allow to change shift on the schedule if shift belongs to the same owner
        """
        schedule = Schedule.objects.get(pk=1)
        shift = Shift.objects.get(pk=1)
        schedule.tue = shift
        schedule.save()

        schedule = Schedule.objects.get(pk=1)
        self.assertEquals(schedule.tue, shift)

    def test_changing_shift_different_owner(self):
        """
        Should raise an error when change shift on the schedule if shift belongs to the a different owner
        """
        schedule = Schedule.objects.get(pk=1)
        shift = Shift.objects.get(pk=3)
        schedule.tue = shift

        self.assertRaises(ValidationError, schedule.save)


class AppointmentTest(TestCaseWF):

    def data(self):
        return {
            'employee': Employee.objects.get(pk=1),
            'customer': Customer.objects.get(pk=1001),
            'service': Service.objects.get(pk=1)
        }

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

    def test_two_appointments_end_on_start(self):
        """
        When a appointment starts on the same minute another one has finished, this should not fail
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

    def test_two_appointments_start_on_end(self):
        """
        When a appointment ends on the same minute another one has started, this should not fail
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=45)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
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

    # TODO: Managed to create 2 appointments with the same date via the web fix this bug
    # TODO: When moving an appointment via the web the endtime is not updating accoringly to the service

    def test_appointment_starting_in_middle_of_another(self):
        """
        Two appointments where the second starts in the middle of the first, the second should error and not create
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=15)
        self.assertRaises(ValidationError,
                          book_appointment,
                          **data)

    def test_appointment_finishing_in_middle_of_another(self):
        """
        Two appointments where the second finishes in the middle of the first, the second should error and not create
        """
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=30)
        appointment = book_appointment(**data)
        self.assertIsInstance(appointment, Appointment)

        data['start'] = next_tuesday().replace(hour=9, minute=15)
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
        """self appointment should be possible, when this hapens the service field will be null"""
        data = self.data()
        data['start'] = next_tuesday().replace(hour=9, minute=0)
        data['end'] = next_tuesday().replace(hour=10, minute=0)
        data['customer'] = data['employee']
        del (data['service'])
        appointment = book_appointment(**data)
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
        self.assertEqual(customer.id, last_id + 1)
        self.assertEqual(emp.id, customer.id + 1)


class EmployeeTest(TestCaseWF):

    def test_add_service(self):
        """Adding a service to an employee should be allowed where both entities belong to the same owner"""
        emp = Employee.objects.get(pk=2)
        service = Service.objects.get(pk=2)
        emp.services.add(service)

        self.assertEquals(emp.services.get(pk=2), service)

    def test_add_service_different_owner(self):
        """Adding a service to an employee with different owners in entities should raise an error"""
        emp = Employee.objects.get(pk=2)
        service = Service.objects.get(pk=3)

        self.assertRaises(ValidationError, emp.services.add, service)

    def test_add_multiple_services_different_owners(self):
        """Adding a service to an employee with different owners in entities should raise an error"""
        emp = Employee.objects.get(pk=2)
        services = [Service.objects.get(pk=3), Service.objects.get(pk=4)]

        self.assertRaises(ValidationError, emp.services.add, *services)

    def test_add_multiple_services_mixed_owners(self):
        """Adding a service to an employee with mixed owners in entities should raise an error"""
        emp = Employee.objects.get(pk=2)
        services = [Service.objects.get(pk=2), Service.objects.get(pk=4)]

        self.assertRaises(ValidationError, emp.services.add, *services)

    def test_changing_schedule(self):
        """
        Employees can only be assigned schedule from the same owner
        """
        emp = Employee.objects.get(pk=1)
        sch = Schedule.objects.get(pk=3)
        emp.schedule = sch
        emp.save()

        self.assertEquals(emp.schedule, sch)

    def test_changing_schedule_different_owner(self):
        """
        An error should be thrown
        When assigned to a schedule of a different owner
        """
        emp = Employee.objects.get(pk=1)
        sch = Schedule.objects.get(pk=2)
        emp.schedule = sch

        self.assertRaises(ValidationError, emp.save)


class ServiceTest(TestCaseWF):

    def test_add_employee(self):
        """Adding an employee to a service should be allowed where both entities belong to the same owner"""
        emp = Employee.objects.get(pk=2)
        service = Service.objects.get(pk=2)
        service.employee_set.add(emp)

        self.assertEquals(service.employee_set.get(pk=2), emp)

    def test_add_service_different_owner(self):
        """Adding an employee to a service with different owners in entities should raise an error"""
        service = Service.objects.get(pk=3)
        emp = Employee.objects.get(pk=2)

        self.assertRaises(ValidationError, service.employee_set.add, emp)

    def test_add_multiple_employees_different_owners(self):
        """Adding multiple employees to a service with different owners in entities should raise an error"""
        service = Service.objects.get(pk=3)
        employees = [Employee.objects.get(pk=2), Employee.objects.get(pk=1)]

        self.assertRaises(ValidationError, service.employee_set.add, *employees)

    def test_add_multiple_employees_mixed_owners(self):
        """Adding multiple employees to a service with mixed owners in entities should raise an error"""
        service = Service.objects.get(pk=3)
        employees = [Employee.objects.get(pk=2), Employee.objects.get(pk=5)]

        self.assertRaises(ValidationError, service.employee_set.add, *employees)


class CompanyTest(TestCaseWF):

    def test_add_company_with_existing_name(self):
        """creating a company with the same name as another should not be allowed"""
        name = 'company-name'
        Company.objects.create(name=name)
        self.assertRaises(IntegrityError, Company.objects.create, name=name)

    def test_add_company_space_in_name(self):
        """company names shouldn't have spaces"""
        name = 'company with spaces'
        self.assertRaises(ValidationError, Company.objects.create, name=name)
        self.assertRaises(ValidationError, Company.objects.create, name=' startsWithSpace')

    def test_update_company_name_existing_name(self):
        """if the name of an already existing company is updated to a used name the company should fail on save"""
        name1 = 'company-1'
        name2 = 'company-2'
        Company.objects.create(name=name1)
        c2 = Company.objects.create(name=name2)
        c2.name = name1
        self.assertRaises(IntegrityError, c2.save)


class ConfigTest(TestCaseWF):

    def test_add_message(self):
        c1 = Company.objects.all().last()
        m = Config.objects.create(owner=c1)
        self.assertEqual(m.owner_id, c1.id)
        c2 = Company.objects.get(pk=c1.id)


def get_current(owner_id=1, user_id=2):
    return Request.objects.get_current(owner_id=owner_id, user_id=user_id)


class RequestTest(TestCaseWF):

    def test_create_request(self):
        r = Request.objects.create(owner_id=1, user_id=2, scheduled_date='2020-08-05')
        self.assertEqual(r.owner_id, 1)
        self.assertEqual(r.user_id, 2)

    def test_get_current(self):
        """
        get current should create a new request if none exists
        or return the first incomplete request found
        """
        initial_len = len(Request.objects.all())
        r1 = get_current()
        self.assertEqual(len(Request.objects.all()), initial_len + 1)
        r2 = get_current()
        self.assertEqual(len(Request.objects.all()), initial_len + 1)

    def test_add_appointment(self):
        """
        appointments added to a request should have the user's person set to the customer
        """
        r1 = get_current()
        appointment = Appointment.objects.create(start=next_tuesday().replace(hour=9, minute=0),
                                                 service_id=1,
                                                 customer_id=2001,
                                                 employee_id=1,
                                                 owner_id=1)
        r1.appointment_set.add(appointment)
        r1.save()

        self.assertEqual(len(r1.appointment_set.all()), 1)

    def test_add_appointment_wrong_customer(self):
        """
        if the person is not the same as the user's person save should fail
        """
        r1 = get_current()
        appointment = Appointment.objects.create(start=next_tuesday().replace(hour=9, minute=0),
                                                 service_id=1,
                                                 customer_id=1001,
                                                 employee_id=1,
                                                 owner_id=1)
        r1.appointment_set.add(appointment)

        self.assertRaises(exceptions.InvalidCustomer, r1.save)

    def test_add_appointment_wrong_owner(self):
        """
        if the person is not the same as the user's person save should fail
        """
        r1 = get_current(owner_id=2)
        appointment = Appointment.objects.create(start=next_tuesday().replace(hour=9, minute=0),
                                                 service_id=1,
                                                 customer_id=2001,
                                                 employee_id=1,
                                                 owner_id=1)
        r1.appointment_set.add(appointment)

        self.assertRaises(exceptions.DifferentOwnerError, r1.save)

    def test_add_appointment(self):
        r1 = get_current()
        r1.add_appointment(start=next_tuesday().replace(hour=9, minute=0),
                           service_id=1,
                           customer_id=2001,
                           employee_id=1,
                           owner_id=1)
        self.assertEqual(len(r1.appointment_set.all()), 1)

    def test_add_appointment_wrong_customer(self):
        r1 = get_current()
        c1 = len(Appointment.objects.all())
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 1001,
                  'employee_id': 1,
                  'owner_id': 1}
        self.assertRaises(exceptions.InvalidCustomer, r1.add_appointment, **params)
        c2 = len(Appointment.objects.all())
        self.assertEqual(c1, c2)

    def test_add_appointment_wrong_owner(self):
        r1 = get_current(owner_id=2)
        c1 = len(Appointment.objects.all())
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 2001,
                  'employee_id': 1,
                  'owner_id': 1}
        self.assertRaises(exceptions.DifferentOwnerError, r1.add_appointment, **params)
        c2 = len(Appointment.objects.all())
        self.assertEqual(c1, c2)

    def test_get_pending(self):
        objs = Request.objects.filter(_status='P')
        self.assertEqual(len(objs), 1)

    def test_update_status(self):
        instance = Request.objects.get(pk=1)
        instance.status = Appointment.ACCEPTED
        for apt in instance.appointment_set.all():
            self.assertEqual(apt.status, Appointment.ACCEPTED)
