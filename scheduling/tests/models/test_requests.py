from decimal import Decimal

from scheduling import exceptions
from scheduling.models import Request, Appointment
from scheduling.tests.generics import TestCaseWF
from util.test_util import next_tuesday
from core.models import User


def get_current(owner_id=1, user_id=2):
    return Request.objects.get_current(owner_id=owner_id, user_id=user_id)


class RequestTest(TestCaseWF):

    def assert_request_status(self, request, status):
        self.assertEqual(request.status, status)
        for apt in request.appointment_set.all():
            self.assertEqual(apt.status, status)

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
        r1.add_appointment(start=next_tuesday().replace(hour=9, minute=0),
                           service_id=1,
                           customer_id=2001,
                           employee_id=1,
                           owner_id=1)
        self.assertEqual(len(r1.appointment_set.all()), 1)

    def test_add_appointment_no_employee(self):
        """
        requests can have appointments without an employee id
        """
        r1 = get_current()
        r1.add_appointment(start=next_tuesday().replace(hour=9, minute=0),
                           service_id=1,
                           customer_id=2001,
                           owner_id=1)
        self.assertEqual(len(r1.appointment_set.all()), 1)

    def test_add_appointment_using_user(self):
        """
        Adding appointment providing the user instead of the customer should work the same way
        """
        user_id = 2
        r1 = get_current(user_id=user_id)
        r1.add_appointment(start=next_tuesday().replace(hour=9, minute=0),
                           service_id=1,
                           user=User.objects.get(pk=user_id),
                           employee_id=1,
                           owner_id=1)
        self.assertEqual(len(r1.appointment_set.all()), 1)
        appointment = r1.appointment_set.first()
        self.assertEqual(appointment.customer_id, 2001)

    def test_add_appointment_wrong_owner(self):
        r1 = get_current(owner_id=2)
        before = [*Appointment.objects.all()]
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 2001,
                  'employee_id': 1,
                  'owner_id': 1}
        self.assertRaises(exceptions.DifferentOwnerError, r1.add_appointment, **params)
        after = [*Appointment.objects.all()]
        self.assertEqual(len(before), len(after))

    def test_add_appointment_wrong_customer(self):
        """
        if the person is not the same as the user's person save should fail
        """
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

    def test_add_appointment_different_date(self):
        """
        The system should throw an error when the new appointment is not in the same date assigned in the request
        """
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 2001,
                  'employee_id': 1,
                  'owner_id': 1}

        request = get_current()
        initial_apt_len = len(Appointment.objects.all())
        request.add_appointment(**params)  # Adds appointment
        after_request_add_len = len(Appointment.objects.all())
        params['start'] = next_tuesday(7).replace(hour=9, minute=0)

        self.assertRaises(exceptions.ValidationError, request.add_appointment, **params)
        after_error_len = len(Appointment.objects.all())
        self.assertEqual(initial_apt_len + 1, after_request_add_len)
        self.assertEqual(after_request_add_len, after_error_len)

    def test_add_two_appointments_same_service(self):
        """
        if the person is not the same as the user's person save should fail
        """
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 2001,
                  'employee_id': 1,
                  'owner_id': 1}

        request = get_current() # Get request
        request.add_appointment(**params)  # Adds appointment
        # Adds a new appointment with the same service for another time
        params['start'] = next_tuesday().replace(hour=11, minute=0, second=0, microsecond=0)
        request.add_appointment(**params)

        # Make sure there's a single appointment in the request
        self.assertEqual(len(request.appointment_set.all()), 1)
        # Make sure the date is related to the last appointment booked
        self.assertEqual(request.appointment_set.first().start, params['start'])

    def test_accept(self):
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 2001,
                  'employee_id': 1,
                  'owner_id': 1}
        request = get_current()  # Get request
        request.add_appointment(**params)  # Adds appointment
        params.update({'service_id': 2, 'start': next_tuesday().replace(hour=11)})

        self.assert_request_status(request, Appointment.PENDING)
        request.accept()
        self.assert_request_status(request, Appointment.ACCEPTED)

    def test_costs(self):
        params = {'start': next_tuesday().replace(hour=9, minute=0),
                  'service_id': 1,
                  'customer_id': 2001,
                  'employee_id': 1,
                  'owner_id': 1}
        request = get_current()  # Get request
        request.add_appointment(**params)  # Adds appointment
        params.update({'service_id': 2, 'start': next_tuesday().replace(hour=11)})
        request.add_appointment(**params)  # Adds appointment

        self.assertEqual(request.total, Decimal(23 + 15))  # service 1 + service 2 cost from fixtures
        self.assertEqual(request.fee, 1)  # service 1 + service 2 cost from fixtures

    def test_get_pending(self):
        objs = Request.objects.filter(_status='P')
        self.assertEqual(len(objs), 1)

    def test_messages(self):
        request = get_current()

        self.assertIn(request.owner.config.appointment_accepted_message, request.request_accepted_email_message)
        self.assertIn(request.owner.config.appointment_rejected_message, request.request_rejected_email_message)
