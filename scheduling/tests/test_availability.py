from scheduling.availability import get_availability_for_service
from scheduling.models import Customer, Employee
from scheduling.tests.generics import TestCaseWF
from scheduling.tests.util import *


class SlotTest(TestCaseWF):

    def setUp(self):
        self.emp = Employee.objects.get(pk=1)
        self.customer = Customer.objects.get(pk=5)
        self.service = self.emp.services.first()

    def book_appointment(self, date):
        return book_appointment(self.emp, self.service, self.customer, date)

    def get_slots(self, date_to_check):
        return get_availability_for_service(self.emp, self.service,
                                            date_to_check.replace(hour=0, minute=0),
                                            date_to_check.replace(hour=23, minute=59))

    def test_day_without_appointments(self):
        print("test_day_without_appointments", end="\n\n")

        slots = self.get_slots(next_wednesday())
        self.assertEqual(len(slots), 17)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration_delta())

    def test_day_with_one_appointment_start_of_shift(self):
        print("test_day_with_one_appointment_start_of_shift", end="\n\n")

        appointment_1_date = next_tuesday().replace(hour=9, minute=00)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration_delta())

        self.assertEqual(len(slots), 16)

    def test_day_with_one_appointment_start_of_shift_1_offset(self):
        print("test_day_with_one_appointment_start_of_shift_1_offset", end="\n\n")

        appointment_1_date = next_wednesday().replace(hour=9, minute=30)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration_delta())

        self.assertEqual(len(slots), 16)

    def test_day_with_one_appointment_start_of_shift_half_time_offset(self):
        print("test_day_with_one_appointment_start_of_shift_half_time_offset", end="\n\n")

        appointment_1_date = next_wednesday().replace(hour=9, minute=15)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots(appointment_1_date)

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration_delta())

        self.assertEqual(len(slots), 15)

    def test_day_without_schedule(self):
        print('test_day_without_schedule', end='\n\n')

        slots = self.get_slots(next_monday())
        self.assertEqual(len(slots), 0)

    def test_shift_with_break(self):
        print('test_shift_with_break', end='\n\n')

        appointment_1_date = next_tuesday().replace(hour=15, minute=30)
        self.book_appointment(appointment_1_date)
        slots = self.get_slots(next_tuesday())

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration_delta())

        self.assertEqual(len(slots), 13)

    def test_slot_(self):
        print('test_slot_', end='\n\n')

        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment_2_date = next_tuesday().replace(hour=10, minute=0)
        self.book_appointment(appointment_1_date)
        self.book_appointment(appointment_2_date)
        slots = self.get_slots(next_tuesday())

        for slot in slots:
            self.assertEqual(slot.duration(), self.service.duration_delta())

        self.assertEqual(len(slots), 12)

    def test_rejected_appointment(self):
        print("test_rejected_appointment", end="\n\n")

        appointment_1_date = next_wednesday().replace(hour=9, minute=15)
        appointment = self.book_appointment(appointment_1_date)

        reject_appointment(appointment)

        slots = self.get_slots(appointment_1_date)
        self.assertEqual(len(slots), 17)
