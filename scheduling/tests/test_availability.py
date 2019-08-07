from unittest import TestCase

from scheduling.availability import get_availability_for_service
from scheduling.tests.util import *


class SlotTest(TestCase):
    def setUp(self):
        self.helper = TestHelper()
        self.emp = self.helper.emp
        print(self.helper.emp.schedule.thu)

    def tearDown(self):
        self.helper.tearDown()

    def get_slots(self, date_to_check):
        return get_availability_for_service(self.helper.emp, date_to_check, self.helper.service)

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

    def test_shift_with_break(self):
        print('test_shift_with_break', end='\n\n')

        appointment_1_date = next_tuesday().replace(hour=15, minute=30)
        self.helper.book_appointment(appointment_1_date)
        slots = self.get_slots(next_tuesday())

        for slot in slots:
            self.assertEqual(slot.duration(), self.helper.service.duration_delta())

        self.assertEqual(len(slots), 13)

    def test_slot_(self):
        print('test_shift_with_break', end='\n\n')

        appointment_1_date = next_tuesday().replace(hour=9, minute=0)
        appointment_2_date = next_tuesday().replace(hour=10, minute=0)
        self.helper.book_appointment(appointment_1_date)
        self.helper.book_appointment(appointment_2_date)
        slots = self.get_slots(next_tuesday())

        for slot in slots:
            self.assertEqual(slot.duration(), self.helper.service.duration_delta())

        self.assertEqual(len(slots), 12)