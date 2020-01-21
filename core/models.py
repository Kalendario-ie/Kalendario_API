from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from scheduling.models import Person

from core.managers import UserManager


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_employee(self):
        return hasattr(self, 'person') and hasattr(self.person, 'employee')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'person'):
            person = Person(user=self)
            person.save()
