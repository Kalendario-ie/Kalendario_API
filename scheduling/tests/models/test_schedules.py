from scheduling.models import *
from datetime import datetime, time

from scheduling.tests.generics import TestCaseWF


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

    # TODO: test_changing_shift_different_owner
    # def test_changing_shift_different_owner(self):
    #     """
    #     Should raise an error when change shift on the schedule if shift belongs to the a different owner
    #     """
    #     schedule = Schedule.objects.get(pk=1)
    #     shift = Shift.objects.get(pk=3)
    #     schedule.tue = shift
    #
    #     self.assertRaises(ValidationError, schedule.save)


