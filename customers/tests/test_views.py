from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status

import scheduling.tests.util as util
from core.models import User
from scheduling.models import Appointment, Person, Employee, Customer, Company
from scheduling.tests.generics import ViewTestCase


def create_apt_data(emp, customer, service, date):
    return {'employee': emp.id,
            'customer': customer.id,
            'service': service.id,
            'start': str(date),
            }


def create_self_apt_data(emp, customer, start, end):
    return {'employee': emp.id,
            'customer': customer.id,
            'start': str(start),
            'end': str(end)
            }


def test_user(person=Person(email="user@email.com")):
    person.save()
    user = User.objects.create(email='user@email.com')
    user.set_password('UserPass')
    user.person = person
    if hasattr(person, 'owner_id'):
        user.owner_id = person.owner_id
    user.save()
    return user


def company_1_admin():
    user = User.objects.get(pk=1)
    user.person = Person.objects.create(first_name=user.first_name, last_name=user.last_name)
    user.save()
    user.groups.add(util.company_1_master_group())
    return user


def emp_service(company=Company.objects.first()):
    emp = company.employee_set.first()
    service = emp.services.first()
    return emp, service


def emp_customer_service(company=Company.objects.first()):
    emp, service = emp_service(company)
    return emp, company.customer_set.first(), service


class CompanyViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('customer-company-list')

    def slot_url(self):
        return self.list_url + 'slots/'

    def test_anonymous_view(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_slots(self):
        pass


class RequestViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('customer-request-list')

    def current_url(self):
        return f'{self.list_url}current/'

    # def appointment_url(self):
    #     return f'{self.list_url}appointment/'

    def test_get_current_no_owner_id(self):
        self.client.force_authenticate(user=test_user())
        response = self.client.get(self.current_url(), format='json')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_current(self):
        self.client.force_authenticate(user=test_user())
        response = self.client.get(self.current_url(), data={'owner': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_appointment(self):
        emp, service = emp_service()
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, user.person, service, util.next_tuesday().replace(hour=10, minute=0))

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_appointment_omitting_employee(self):
        emp, service = emp_service()
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, user.person, service, util.next_tuesday().replace(hour=10, minute=0))
        data.pop('employee')

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_and_remove_appointment(self):
        emp, service = emp_service()
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, user.person, service, util.next_tuesday().replace(hour=10, minute=0))

        self.client.force_authenticate(user=user)
        response1 = self.client.post(self.list_url, data, format='json')
        request_id = response1.data['id']
        apt_id = response1.data['appointments'][0]['id']
        response = self.client.delete(self.list_url + f'{request_id}/?appointment={apt_id}&owner={emp.owner_id}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
