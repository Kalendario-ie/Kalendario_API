from django.urls import reverse
from django.core import mail
from rest_framework import status

import scheduling.tests.util as util
from core.models import User
from scheduling.models import Person, Company
from scheduling.tests.generics import ViewTestCase


def create_apt_data(emp, service, date):
    return {'employee': emp.id,
            'service': service.id,
            'start': str(date),
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


def emp_service(company=None):
    if company is None:
        company = Company.objects.first()
    emp = company.employee_set.first()
    service = emp.services.first()
    return emp, service


def emp_customer_service(company=None):
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
        self.url_name = 'customer-request'
        self.list_url = reverse(self.url_name + '-list')

    def current_url(self):
        return f'{self.list_url}current/'

    def detail_url(self, pk):
        return reverse(self.url_name + '-detail', kwargs={'pk': pk})

    def assert_user_customers_same_params(self, user):
        for c in user.customer_set.all():
            self.assertEqual(user.email, c.email)
            self.assertEqual(user.first_name, c.first_name)
            self.assertEqual(user.last_name, c.last_name)

    def assert_response_contains_customer_with_user_data(self, user, request_response):
        for appointment in request_response.data['appointments']:
            customer = appointment['customer']
            self.assertEqual(customer['first_name'], user.first_name)
            self.assertEqual(customer['last_name'], user.last_name)
            self.assertEqual(customer['email'], user.email)

    def test_get_current_no_owner_id(self):
        self.client.force_authenticate(user=test_user())
        response = self.client.get(self.current_url(), format='json')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_current(self):
        self.client.force_authenticate(user=test_user())
        response = self.client.get(self.current_url(), data={'owner': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_appointment(self):
        """
        Adding an appointment to a request should require employee, service and start date.
        In the case where the user is already linked to customer in the company,
            no additional customer model should be created
        """

        emp, service = emp_service()
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, service, util.next_tuesday().replace(hour=10, minute=0))

        before_count = user.customer_set.all().count()

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url + 'add/', data, format='json')

        after_count = user.customer_set.all().count()

        self.assert_user_customers_same_params(user)
        self.assert_response_contains_customer_with_user_data(user, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count, after_count)

    def test_create_appointment_new_company(self):
        """
        Adding an appointment to a request should require employee, service and start date.
        In the case where the user is not linked to a customer in the company,
            a new additional customer model should be created for the company the appointment is being created
        """

        emp, service = emp_service(Company.objects.get(pk=2))
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, service, util.next_wednesday().replace(hour=10, minute=0))

        before_count = user.customer_set.all().count()

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url + 'add/', data, format='json')

        after_count = user.customer_set.all().count()

        self.assert_user_customers_same_params(user)
        self.assert_response_contains_customer_with_user_data(user, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count + 1, after_count)

    def test_create_appointment_existing_email_not_linked(self):
        """
        Adding an appointment to a request should require employee, service and start date.
        In the case where the user is not linked to a customer in the company,
            a new additional customer model should be created for the company the appointment is being created
        """

        emp, service = emp_service(Company.objects.get(pk=2))
        user = User.objects.create(email='Finn.TheHuman@adventuretime.com', first_name='Finn',
                                   last_name='The Human')
        data = create_apt_data(emp, service, util.next_wednesday().replace(hour=10, minute=0))

        before_count = user.customer_set.all().count()

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url + 'add/', data, format='json')

        after_count = user.customer_set.all().count()

        self.assert_user_customers_same_params(user)
        self.assert_response_contains_customer_with_user_data(user, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count + 1, after_count)

    def test_create_appointment_omitting_employee(self):
        emp, service = emp_service()
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, service, util.next_tuesday().replace(hour=10, minute=0))
        data.pop('employee')

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url + 'add/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_and_remove_appointment(self):
        emp, service = emp_service()
        user = User.objects.get(pk=2)
        data = create_apt_data(emp, service, util.next_tuesday().replace(hour=10, minute=0))

        self.client.force_authenticate(user=user)
        response1 = self.client.post(self.list_url + 'add/', data, format='json')
        request_id = response1.data['id']
        apt_id = response1.data['appointments'][0]['id']
        response = self.client.delete(self.list_url + f'{request_id}/?appointment={apt_id}&owner={emp.owner_id}',
                                      format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_submit_request(self):
        # Login
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        # get current request
        get = self.client.get(self.current_url(), {'owner': 1}, format='json')
        request_id = get.data.get('id')

        # Add one appointment to request
        company = Company.objects.first()
        emp, service = emp_service(company)
        data = create_apt_data(emp, service, util.next_tuesday().replace(hour=10, minute=0))
        post = self.client.post(self.list_url + 'add/', data, format='json')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)

        confirm = self.client.patch(self.detail_url(request_id) + 'confirm/')
        self.assertEqual(confirm.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, 'Request Submitted')
        self.assertEqual(sent_mail.body, company.config.post_book_email_message)
        self.assertIn(user.email, sent_mail.to)
