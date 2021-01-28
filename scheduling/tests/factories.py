import factory
from factory.django import DjangoModelFactory

from scheduling import models


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Faker('name')
    email = factory.Faker('email')


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = models.Employee

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = models.Service

    name = factory.Faker('name')
    duration = factory.Faker('time_delta')
