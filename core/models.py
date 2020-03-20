from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.managers import UserManager
from scheduling.models import Person, Company


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_employee(self):
        return hasattr(self, 'person') and hasattr(self.person, 'employee')

    def is_company_admin(self):
        return self.company and self.has_perm('scheduling.add_appointment')

    def change_to_emp(self, emp):
        self.person.delete()
        self.person = emp
        self.save()

    def enable_company_editing(self):
        permissions = ['appointment', 'employee', 'shift', 'schedule', 'service', 'customer']
        for name in permissions:
            list(map(self.user_permissions.add, Permission.objects.filter(codename__endswith=name)))
        self.save()
