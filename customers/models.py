import datetime

from customers.customException import InvalidActionException
from scheduling.models import Employee


class Slot:

    def __init__(self, start: datetime.datetime, end):
        self.start = start
        self.end = end

    def duration(self):
        return self.end - self.start

    @property
    def id(self):
        return self.start.isoformat()

    def breakdown_slot(self, duration):
        if self.duration() > duration:
            break_point = self.start + duration
            a = {self.id: Slot(self.start, break_point)}
            b = Slot(break_point, self.end).breakdown_slot(duration)
            a.update(b)
            return a
        if self.duration() == duration:
            return {self.id: self}
        return {}

    @staticmethod
    def create_slot(date, start, end):
        return Slot(date.replace(hour=start.hour, minute=start.minute), date.replace(hour=end.hour, minute=end.minute))

    def __str__(self):
        return '{start} - {end}'.format(start=self.start.isoformat(), end=self.end.isoformat())

    def __dict__(self):
        return {'start': self.start.isoformat(), 'end': self.end.isoformat()}


def get_availability(employee: Employee, customer, start, end):
    if start < datetime.datetime.now():
        start = datetime.datetime.now()

    if end.date() <= datetime.date.today():
        raise InvalidActionException("Date can't be in the past")

    day = start.replace(hour=0, minute=0, second=0, microsecond=0)
    slots = []
    while day < end:
        frame_slots = [Slot.create_slot(day, frame.start, frame.end) for frame in employee.get_availability(day)]
        slots.extend([slot for slot in frame_slots if slot.start > start])
        day = day + datetime.timedelta(days=1)

    appointments = employee.confirmed_appointments(start, end)
    if customer:
        appointments.extend(customer.confirmed_appointments(start, end))

    # goes through appointments removing the time of an appointment from the slot belongs to
    for appointment in appointments:
        for i, slot in enumerate(slots):
            if appointment.start <= slot.start and appointment.end >= slot.end:
                slots = [x for x in slots if x != slot]
            if appointment.start >= slot.start and appointment.end <= slot.end:
                slots = slots[:i] + [Slot(slot.start, appointment.start),
                                     Slot(appointment.end, slot.end)] + slots[i + 1:]
    return slots


def get_availability_for_service(service, start, end, employee=None, customer=None):

    if employee is not None and not employee.provides_service(service):
        raise InvalidActionException("Employee doesn't provide the service specified")

    slots = {}
    if employee is not None:
        for slot in get_availability(employee, customer, start, end):
            slots.update(slot.breakdown_slot(service.duration))
    else:
        for employee in service.employee_set.all():
            for slot in get_availability(employee, customer, start, end):
                a = slot.breakdown_slot(service.duration)
                slots.update(a)
    return sorted(slots.values(), key=lambda x: x.start)

