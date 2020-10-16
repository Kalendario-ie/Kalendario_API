from customers.models import get_availability_for_service
from customers.tests.generics import TestCaseWF
from scheduling import models
from scheduling.tests import util


class SlotTest(TestCaseWF):

    def setUp(self):
        self.emp = models.Employee.objects.get(pk=1)
        self.customer = models.Person.objects.get(pk=2001)
        self.service = self.emp.services.first()

    def book_appointment(self, date):
        return util.book_appointment(self.emp, self.customer, date, self.service)

    def get_slots(self, date_to_check, emp=None):
        return get_availability_for_service(self.service,
                                            date_to_check.replace(hour=0, minute=0),
                                            date_to_check.replace(hour=23, minute=59),
                                            emp)

    def get_slots_for_emp(self, date_to_check):
        return self.get_slots(date_to_check, self.emp)

    def test_day_without_appointments(self):
        slots = self.get_slots_for_emp(util.next_tuesday())
        self.assertEqual(len(slots), 14)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration)

    def test_day_with_one_appointment_start_of_shift(self):
        appointment_1_date = util.next_tuesday().replace(hour=9, minute=00)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots_for_emp(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration)

    def test_day_with_one_appointment_start_of_shift_1_offset(self):
        appointment_1_date = util.next_tuesday().replace(hour=9, minute=30)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots_for_emp(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration)

        self.assertEqual(len(slots), 13)

    def test_day_with_one_appointment_start_of_shift_half_time_offset(self):
        appointment_1_date = util.next_tuesday().replace(hour=9, minute=15)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots_for_emp(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration)

        self.assertEqual(len(slots), 12)

    def test_day_without_schedule(self):
        slots = self.get_slots_for_emp(util.next_monday())
        self.assertEqual(len(slots), 0)

    def test_shift_with_break(self):
        appointment_1_date = util.next_tuesday().replace(hour=15, minute=30)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots_for_emp(util.next_tuesday())

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration)

        self.assertEqual(len(slots), 13)

    def test_slot_(self):
        appointment_1_date = util.next_tuesday().replace(hour=9, minute=0)
        appointment_2_date = util.next_tuesday().replace(hour=10, minute=0)
        self.book_appointment(appointment_1_date)
        self.book_appointment(appointment_2_date)
        slots = self.get_slots_for_emp(util.next_tuesday())

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration)

        self.assertEqual(len(slots), 12)

    def test_rejected_appointment(self):
        appointment_1_date = util.next_tuesday().replace(hour=9, minute=15)
        appointment = self.book_appointment(appointment_1_date)

        util.reject_appointment(appointment)

        slots = self.get_slots_for_emp(appointment_1_date)
        self.assertEqual(len(slots), 14)

    def test_get_without_employee(self):
        slots = self.get_slots(util.next_tuesday())
        self.assertEqual(len(slots), 14)
