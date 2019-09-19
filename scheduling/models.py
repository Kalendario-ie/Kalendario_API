from cloudinary.models import CloudinaryField
from django.db.models import Q

from core.models import User
from scheduling.managers import *


class TimeFrame(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE)

    def __str__(self):
        return 'start: ' + self.start.__str__() + ', end: ' + self.end.__str__()


class Shift(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    name = models.CharField(max_length=20)
    mon = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='mon')
    tue = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='tue')
    wed = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='wed')
    thu = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='thu')
    fri = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='fri')
    sat = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='sat')
    sun = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='sun')

    def get_availability(self, date):
        dayofweek = date.weekday()
        if dayofweek == 0:
            shift = self.mon
        elif dayofweek == 1:
            shift = self.tue
        elif dayofweek == 2:
            shift = self.wed
        elif dayofweek == 3:
            shift = self.thu
        elif dayofweek == 4:
            shift = self.fri
        elif dayofweek == 5:
            shift = self.sat
        else:
            shift = self.sun

        if shift is None:
            return []

        return shift.timeframe_set.all()

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    duration = models.TimeField()

    def duration_delta(self):
        return datetime.datetime.combine(datetime.datetime.min, self.duration) - datetime.datetime.min

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.name()


class Employee(Person):
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, blank=True)
    services = models.ManyToManyField(Service)
    instagram = models.CharField(max_length=200, null=True)
    profile_img = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(max_length=600, null=True, blank=True)

    def email(self):
        return self.user.email

    def provides_service(self, service: Service):
        return self.services.filter(id=service.id).first() is not None

    def get_availability(self, date):
        return self.schedule.get_availability(date)

    def confirmed_appointments(self, start, end):
        appointments = self.baseappointment_set.filter(start__gte=start, start__lte=end).select_subclasses()
        return list(filter(lambda x: x.is_active(), appointments))

    # To be available the times must fit inside a frame and not overlap existing appointments
    def is_available(self, start, end):
        return self.__has_availability__(start, end) and not self.__is_overlapping__(start, end)

    # Check id the appointment fits inside a frame
    def __has_availability__(self, start, end):
        availability = self.get_availability(start.date())
        for frame in availability:
            if start.time() >= frame.start and end.time() <= frame.end:
                return True
        return False

    # Check if the appointment overlaps with any other appointment already booked.
    def __is_overlapping__(self, start, end):
        starts_or_ends_between = self.baseappointment_set.filter(
            Q(start__gte=start, start__lt=end) | Q(end__gt=start, end__lte=end)).select_subclasses()
        return len(list(filter(lambda x: x.is_active(), starts_or_ends_between))) > 0


class Customer(Person):
    pass


class BaseAppointment(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    objects = BaseAppointmentManager()

    # System shouldn't be able to book over active appointments but it should ignore inactive
    def is_active(self):
        return True

    def __str__(self):
        return "{emp}: {start} to {end}".format(
            date=self.start,
            start=self.start,
            end=self.end,
            emp=self.employee.name()
        )


class Appointment(BaseAppointment):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    customer_notes = models.TextField(max_length=255, null=True, blank=True)

    objects = AppointmentManager()

    def is_active(self):
        return self.status != Appointment.REJECTED

    def __str__(self):
        return "{customer} on {date} from {start} to {end} {service} with {emp}. {status}".format(
            customer=self.customer.name(),
            date=self.start.date(),
            start=self.start.time(),
            end=self.end,
            service=self.service.name,
            emp=self.employee.name(),
            status=self.status
        )


# This will lock a period without a customer, so employees can block appointments by booking this
class SelfAppointment(BaseAppointment):
    reason = models.TextField(max_length=255, null=True, blank=True)
