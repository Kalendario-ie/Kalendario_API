import datetime

from scheduling.customException import InvalidActionException
from scheduling.models import Service, Employee


class Slot:

    def __init__(self, start, end):
        self.start = start.replace(second=0, microsecond=0)
        self.end = end.replace(second=0, microsecond=0)

    def duration(self):
        return self.end - self.start

    def breakdown_slot(self, duration):
        if self.duration() > duration:
            break_point = self.start + duration
            return [Slot(self.start, break_point)] + Slot(break_point, self.end).breakdown_slot(duration)
        if self.duration() == duration:
            return [self]
        return []

    @staticmethod
    def create_slot(date, start, end):
        return Slot(date.replace(hour=start.hour, minute=start.minute), date.replace(hour=end.hour, minute=end.minute))

    def __str__(self):
        return '{start} - {end}'.format(start=self.start, end=self.end)

    def __dict__(self):
        return {'start': self.start.isoformat(), 'end': self.end.isoformat()}


def get_availability(employee: Employee, date_time: datetime.datetime):
    """
    :param employee: Employee
    :param date_time: type of datetime.datetime
    :return: a list of slots the start / end times should be exactly the available times
    """
    frames = employee.get_availability(date_time)
    appointments = employee.appointment_set.filter(start__year=date_time.year, start__month=date_time.month,
                                                   start__day=date_time.day)
    slots = list(map(lambda x: Slot.create_slot(date_time, x.start, x.end), frames))

    if date_time.date() <= datetime.date.today():
        raise InvalidActionException("Date can't be in the past")

    # goes through appointments removing the time of an appointment from the slot belongs to
    for appointment in appointments:
        for i in range(len(slots)):
            slot = slots[i]
            if appointment.start >= slot.start:
                slots = slots[:i] + [Slot(slot.start, appointment.start),
                                     Slot(appointment.end(), slot.end)] + slots[i + 1:]
    return slots


def get_availability_for_service(employee: Employee, date_time: datetime, service: Service) -> list:

    if not employee.provides_service(service):
        raise InvalidActionException("Employee doesn't provide the service specified")

    result = []
    for slot in get_availability(employee, date_time):
        result.extend(slot.breakdown_slot(service.duration_delta()))
    return result
