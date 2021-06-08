from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from cloudinary.models import CloudinaryField
from django.db.models import Q
from simple_history.models import HistoricalRecords

from kalendario.common.model_mixins import CleanSaveMixin
from scheduling import managers, exceptions

from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class TimeFrame(CleanSaveMixin, models.Model):
    start = models.TimeField()
    end = models.TimeField()
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE)

    def is_beyond(self, start, end):
        """Returns true is the start/end time provided is between the frames start/end time"""
        return start >= self.start and end <= self.end

    def __str__(self):
        return str(self.id) + ' start: ' + self.start.__str__() + ', end: ' + self.end.__str__()


class Shift(CleanSaveMixin, models.Model):
    pass


class Schedule(CleanSaveMixin, models.Model):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    mon = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='mon')
    tue = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='tue')
    wed = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='wed')
    thu = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='thu')
    fri = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='fri')
    sat = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='sat')
    sun = models.OneToOneField(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='sun')

    def get_week(self):
        """
        :return: a tuple with the shifts in the order of date.weekday to make it easy to access
        """
        return self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun

    def get_availability(self, date):
        shift = self.get_week()[date.weekday()]
        return [] if shift is None else shift.timeframe_set.all()

    def __str__(self):
        return self.name


class ServiceCategory(CleanSaveMixin, models.Model):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=7, default='#FFFFFF')


class Service(CleanSaveMixin, models.Model):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    name = models.CharField(max_length=120)
    duration = models.DurationField()
    color = models.CharField(max_length=7, default='#FFFFFF')
    description = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_from = models.BooleanField(default=False)
    category = models.ForeignKey(ServiceCategory, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def price(self):
        if self.cost == 0:
            return 'TBC'
        if self.is_from:
            return f'from €{self.cost}'
        return f'€{self.cost}'

    def find_available_employee(self, apt):
        for emp in self.employee_set.all():
            if emp.is_available(apt):
                return emp
        return None

    def __str__(self):
        return self.name


class Person(CleanSaveMixin, models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def clean(self):
        self.name = self.first_name + ' ' + self.last_name
        self.email = self.email.lower()

    def __str__(self):
        return self.name


class Employee(Person):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, blank=True)
    services = models.ManyToManyField(Service, null=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    profile_img = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(max_length=600, null=True, blank=True)

    def provides_service(self, service):
        return self.services.filter(id=service.id).first() is not None

    def get_availability(self, date):
        """Returns the employee's time frames for the date provided"""
        return [] if self.schedule is None else self.schedule.get_availability(date)

    def confirmed_appointments(self, start, end):
        """Returns the appointments that overlaps with the start/end date range"""
        return Appointment.objects.overlapping(start, end, employee=self)

    def is_available(self, apt):
        """
        Returns true if the employee has availability in the schedule
        and no overlapping appointments for the appointment
        """
        return self._has_availability(apt.start, apt.end) and not self._is_overlapping(apt.start, apt.end, apt.id)

    def _has_availability(self, start, end):
        """Returns true if the employee has availability in the schedule for the start / end date provided"""
        return any(frame.is_beyond(start.time(), end.time()) for frame in self.get_availability(start.date()))

    def _is_overlapping(self, start, end, exclude_id):
        """Returns true if the appointment overlaps with any other appointment booked for this employee"""
        return Appointment.objects.overlapping(start, end, employee=self, exclude_id=exclude_id)

    def clean(self):
        Person.clean(self)
        # Make sure that the schedule belongs to the same owner as self
        if self.schedule and self.schedule.owner_id != self.owner_id:
            raise ValidationError(r'The schedule does not belong to the same owner of the employee')


class Customer(Person):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    warning = models.CharField(max_length=255, null=True, blank=True)

    def confirmed_appointments(self, start, end):
        appointments = self.service_received.filter(start__gte=start, start__lte=end)
        return [appointment for appointment in appointments if appointment.is_active()]

    def clean(self):
        Person.clean(self)
        # Make sure that the there is no other customer with this email before saving
        if Customer.objects.filter(email=self.email, owner_id=self.owner_id).filter(~Q(id=self.id)).count() > 0:
            raise ValidationError("There's already a customer created with this email address")

    @staticmethod
    def get_customer_for_user(user, owner_id):
        customer, created = Customer.objects.get_or_create(owner_id=owner_id, email=user.email.lower())
        if created:
            customer.email = user.email
            customer.first_name = user.first_name
            customer.last_name = user.last_name
            customer.user = user
            customer.save()

        if customer.user is None:
            customer.user = user
            customer.save()

        return customer


class Appointment(SafeDeleteModel):
    PENDING, ACCEPTED, REJECTED = 'P', 'A', 'R'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='service_provided')
    lock_employee = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_received', null=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    internal_notes = models.TextField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    objects = managers.AppointmentManager()

    class Meta:
        permissions = [
            ("overlap_appointment", "Can overlap appointment"),
        ]

    def is_active(self):
        return self.status != Appointment.REJECTED

    def clean(self):
        self.start = self.start.replace(second=0, microsecond=0)

        # Ensures that if a service is provided the end time is driven by the service duration
        if self.service:

            # Can't provide service for an inexisting customer
            if self.customer is None:
                raise ValidationError('Missing customer parameters')

            # If the cost is zero set the cost to be the same as of the service provided
            if self.cost == 0:
                self.cost = self.service.cost

            if self.end is None:
                self.end = self.start + self.service.duration

        # Ensures that and end time is present in the model
        if self.end is None:
            raise ValidationError('Either a service or an end time was not provided')

        self.end = self.end.replace(second=0, microsecond=0)

        # When an employee is not provided a service must be provided to allow the appointment to find an employee
        if self.employee_id is None and self.service_id is None:
            raise ValidationError('Either a service or an employee has to be provided')

        # If an appointment is being created without an employee this will find an employee available
        if self.employee_id is None:
            self.employee = self.service.find_available_employee(self)  #
            self.lock_employee = False

        # If the above didn't find an employee the appointment can't be saved
        if self.employee is None:
            raise ValidationError('No employee available for the service/date provided')

        # Ensures that the appointment owner is the same as the employee
        if self.owner_id != self.employee.owner_id:
            raise ValidationError('Appointment and Employees does not belong to the same owner')

        # Ensures that if a customer is provided it has the same owner as the employee
        if isinstance(self.customer, Customer) and self.customer.owner_id != self.owner_id:
            raise ValidationError('Customer does not belong to the same owner as employee')

        # An appointment must have a service if the customer of the service is not the employee
        if not self.service and self.customer is not None and self.employee.id != self.customer.id:
            raise ValidationError(r"A service must be provided")

        # The employee must provide the service for the appointment to be valid
        if self.service and not self.employee.provides_service(self.service):
            raise ValidationError(r"Employee doesn't provide this service")

        if self.request is not None:
            self.request.scheduled_date = self.start.date()

        if self.end < self.start:
            raise ValidationError(r"End time can't be before start time")

    def save(self, ignore_availability=False, **kwargs):
        self.clean()

        # Employee must be available for a service to be saved
        if not ignore_availability and not self.employee.is_available(self):
            raise ValidationError(r'No time available for the date selected')

        SafeDeleteModel.save(self, **kwargs)

    def delete(self, force_policy=None, **kwargs):
        return SafeDeleteModel.delete(self, force_policy, ignore_availability=True)

    def hard_delete(self):
        return self.delete(force_policy=HARD_DELETE)

    def __str__(self):
        return f"{self.start} {self.end} C: {self.customer} E: {self.employee}"


class Request(CleanSaveMixin, models.Model):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    scheduled_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    customer_notes = models.TextField(max_length=255, null=True, blank=True)
    _status = models.CharField(max_length=1, choices=Appointment.STATUS_CHOICES, default=Appointment.PENDING)

    objects = managers.RequestManager()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        for a in self.appointment_set.all():
            a.status = status
            a.save()
        self._status = status
        self.save()

    def accept(self):
        self.status = Appointment.ACCEPTED

    @property
    def request_accepted_email_message(self):
        message = f'Request for {self.owner.name} has been confirmed.\n\n'
        message += f'{self.owner.config.appointment_accepted_message}'
        return message

    @property
    def request_rejected_email_message(self):
        message = f'Request for {self.owner.name} has been rejected.\n'
        message += f'{self.owner.config.appointment_rejected_message}'
        return message

    @property
    def total(self):
        return sum(appointment.cost for appointment in self.appointment_set.all())

    @property
    def fee(self):
        return 1

    def add_appointment(self, user=None, **kwargs):
        """
        Creates an appointment for the request, if when trying to save the request there are validation errors
        it will delete the newly created appointment
        After the appointment is created it'll delete any appointments that have the same service
        :param user: This is the user requesting to add an appointment, it's used to link to a customer in the system
        :param kwargs: arguments for the creation of the appointment
        :return: newly created appointment
        """

        if user:
            owner_id = kwargs.get('owner_id') or kwargs.get('owner').id
            kwargs['customer'] = Customer.get_customer_for_user(user, owner_id)

        appointment = self.appointment_set.create(**kwargs)
        try:
            self.save()
            for apt in self.appointment_set.all():
                if apt.service_id == appointment.service_id and apt.id != appointment.id:
                    apt.hard_delete()
            return appointment
        except ValidationError as e:
            appointment.hard_delete()
            raise e

    def clean(self):
        # if self.user.person_id is None:
        #     raise ValidationError(r'User must have a person')

        appointments = [*self.appointment_set.all()]

        if len(appointments) == 1:
            self.scheduled_date = appointments[0].start.date()

        for appointment in appointments:
            if appointment.customer.user_id != self.user.id:
                raise exceptions.InvalidCustomer(r'Appointment customer is not the same as the user')
            if appointment.owner_id != self.owner_id:
                raise exceptions.DifferentOwnerError('Appointment does not belong to the same owner as Request')
            if appointment.start.date() != self.scheduled_date:
                raise exceptions.ValidationError('Appointment does not start on the scheduled date of the request')


class Photo(CleanSaveMixin, models.Model):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=True)
    url = CloudinaryField('image', blank=True)


class Config(CleanSaveMixin, models.Model):
    owner = models.OneToOneField('Company', on_delete=models.CASCADE, primary_key=True)
    pre_book_warn = models.CharField(max_length=2550, default='')
    post_book_message = models.CharField(max_length=2550, default='')
    post_book_email_message = models.CharField(max_length=2550, default='')
    appointment_reminder_message = models.CharField(max_length=2550, default='')
    appointment_accepted_message = models.CharField(max_length=2550, default='')
    appointment_rejected_message = models.CharField(max_length=2550, default='')

    # This flag will allow managers to take their webpage OFFLINE
    private = models.BooleanField(default=True)
    # Show services should be used by the UI to determine if the services section of the webpage should be shown
    show_services = models.BooleanField(default=True)
    # Show employees should be used by the UI to determine if the employees section of the webpage should be shown
    show_employees = models.BooleanField(default=True)

    allow_card_payment = models.BooleanField(default=False)
    allow_unpaid_request = models.BooleanField(default=False)

    @property
    def can_receive_card_payments(self):
        return (hasattr(self.owner, 'account')
                and self.owner.account.is_stripe_enabled
                and self.allow_card_payment)

    @property
    def can_receive_unpaid_request(self):
        return self.allow_unpaid_request

    def clean(self):
        self.owner.save()


class Company(models.Model):
    objects = managers.CompanyManager()

    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=255, null=True)
    instagram = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    whatsapp = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    facebook = models.CharField(max_length=255, null=True)
    avatar = CloudinaryField('image', null=True)
    about = models.CharField(max_length=2550, default='')

    """
    the below flag will be used by the manager to define which companies should be shown to the public
    it's defined as a flag rather than a property to be filtered via SQL
    """
    _is_viewable = models.BooleanField(default=False)

    @property
    def employees(self):
        return self.employee_set.filter(private=False)

    @property
    def services(self):
        return self.service_set.filter(private=False)

    @property
    def slug(self):
        return self.name.replace(' ', '_')

    def update_is_viewable(self):
        """
        This method updates the _is_viewable variable
        A company is viewable if it is not set to private and users can book requests through the webpage
        """
        self._is_viewable = (not self.config.private
                             and (self.config.can_receive_card_payments or self.config.allow_unpaid_request))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name.count('_') > 0:
            raise ValidationError({"name": "name should not contain spaces"})

        if self.id is None:
            models.Model.save(self, force_insert, force_update, using, update_fields)
            self.config = Config.objects.create(owner=self)
            self.save()
        else:
            self.update_is_viewable()
            models.Model.save(self, force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class SchedulingPanel(CleanSaveMixin, models.Model):
    owner = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    employees = models.ManyToManyField(Employee, blank=True)
