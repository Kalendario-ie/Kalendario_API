from scheduling import exceptions
from scheduling.models import Request, Appointment
from scheduling.tests.generics import TestCaseWF
from util.test_util import next_tuesday


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

    def test_get_pending(self):
        objs = Request.objects.filter(_status='P')
        self.assertEqual(len(objs), 1)

    def test_update_status(self):
        instance = Request.objects.get(pk=1)
        instance.status = Appointment.ACCEPTED
        for apt in instance.appointment_set.all():
            self.assertEqual(apt.status, Appointment.ACCEPTED)