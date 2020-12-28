from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from kalendario.common.model_mixins import CleanSaveMixin
from core import managers
from scheduling.models import Customer

PERMISSIONS = ('company', 'historicalappointment', 'appointment', 'employee', 'shift', 'schedule', 'service',
               'servicecategory', 'customer', 'config', 'schedulingpanel', 'groupprofile', 'user', 'request')


def permissions():
    values = [f'{t}_{p}' for p in PERMISSIONS for t in ['add', 'delete', 'change', 'view']]
    values.remove('add_company')
    values.append('overlap_appointment')
    return Permission.objects.filter(codename__in=values)


class GroupProfile(models.Model):
    group = models.OneToOneField('auth.Group', on_delete=models.CASCADE, primary_key=True)
    owner = models.ForeignKey('scheduling.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    objects = managers.GroupProfileManager()

    @property
    def permissions(self):
        return self.group.permissions

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        group_name = f"{self.owner.id}_{self.name}"
        if self.group_id is None:
            self.group_id = self.create_group(group_name).id
        if self.group:
            self.group.name = group_name
            self.group.save()
        return models.Model.save(self, force_insert, force_update, using, update_fields)

    @staticmethod
    def create_group(group_name):
        group, created = Group.objects.get_or_create(name=group_name)
        return group

    def __repr__(self):
        return self.name


class User(CleanSaveMixin, AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    owner = models.ForeignKey('scheduling.Company', on_delete=models.CASCADE, null=True, blank=True)
    employee = models.OneToOneField('scheduling.Employee', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='user_link')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def email_address(self):
        return self.emailaddress_set.filter(email=self.email).first()

    @property
    def verified(self):
        email = self.email_address
        return email and email.verified

    def enable_company_editing(self, id):
        self.owner_id = id
        group, created = GroupProfile.objects.get_or_create(name='Master', owner_id=self.owner_id)
        group.permissions.add(*permissions())
        group.save()
        self.groups.add(group.group)
        self.user_permissions.remove(*Permission.objects.filter(codename='add_company'))
        self.save()

    def link_to_customers(self):
        for customer in Customer.objects.filter(email=self.email):
            customer.user = self
            customer.save()

    def clean(self):
        if self.employee_id is not None and self.employee.owner_id != self.owner_id:
            raise ValidationError({"employee": "Employee does not belong to the same owner as user"})

        if self.verified:
            self.link_to_customers()

    def has_perm(self, perm, obj=None):
        if self.employee_id is not None and perm in ['c.scheduling.view_customer', 'c.scheduling.view_service',
                                                     'c.scheduling.view_appointment', 'c.scheduling.view_schedule']:
            return True
        if perm.startswith('c.'):
            perm = perm[2:]
        return AbstractUser.has_perm(self, perm, obj)


def _get_owner(self: Group):
    if not hasattr(self, 'groupprofile'):
        return None
    return self.groupprofile.owner_id


Group.add_to_class('owner_id', property(_get_owner))
