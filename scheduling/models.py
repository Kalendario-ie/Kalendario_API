from django.db import models
import datetime

from scheduling.customException import ModelCreationFailedException


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
    mon = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='mon')
    tue = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='tue')
    wed = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='wed')
    thu = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='thu')
    fri = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='fri')
    sat = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='sat')
    sun = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='sun')

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


class Person(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    duration = models.TimeField()

    def duration_delta(self):
        return datetime.datetime.combine(datetime.datetime.min, self.duration) - datetime.datetime.min

    def __str__(self):
        return self.name


class Employee(Person):
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null='true')
    services = models.ManyToManyField(Service)
    instagram = models.CharField(max_length=200, null=True)

    def provides_service(self, service: Service):
        return self.services.filter(id=service.id).first() is not None

    def get_availability(self, date):
        return self.schedule.get_availability(date)

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
        date = start.date()
        appointments = self.appointment_set.filter(start__year=date.year,
                                                   start__month=date.month,
                                                   start__day=date.day)
        for appointment in appointments:
            if appointment.start <= start < appointment.end():
                return True
            if appointment.start < end <= appointment.end():
                return True
        return False


class Customer(Person):
    pass


class AppointmentManager(models.Manager):
    def create(self, *args, **kwargs):
        employee = kwargs['employee']
        service = kwargs['service']
        start = kwargs['start'] = kwargs['start'].replace(second=0, microsecond=0)
        end = start + datetime.timedelta(hours=service.duration.hour, minutes=service.duration.minute)
        service_id = service.id

        if start.date() <= datetime.date.today():
            raise ModelCreationFailedException('Date can\'t be on the past')

        if not employee.provides_service():
            raise ModelCreationFailedException('Employee doesn\'t provide this service')

        if not employee.is_available(start, end):
            raise ModelCreationFailedException('No time available for the date selected')

        return super().create(*args, **kwargs)


class Appointment(models.Model):
    start = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    objects = AppointmentManager()

    def day(self):
        return self.start.date()

    def end(self):
        return self.start + datetime.timedelta(hours=self.service.duration.hour, minutes=self.service.duration.minute)

    def __str__(self):
        return "{customer} on {date} from {start} to {end} {service} with {emp}".format(
            customer=self.customer.name,
            date=self.start.date(),
            start=self.start.time(),
            end=self.end(),
            service=self.service.name,
            emp=self.employee.name
        )
