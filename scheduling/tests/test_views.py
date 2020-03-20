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
            'start': str(date)
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
    user.save()
    return user


def emp_customer_service(company=Company.objects.first()):
    emp, customer = company.employee_set.first(), company.customer_set.first()
    service = emp.services.first()
    return emp, customer, service


class AppointmentViewSetTest(ViewTestCase):
    """
    Tests should follow the convention of test_<type of user>_<action type>_<extra information>
    """

    def setUp(self):
        self.list_url = reverse('appointment-list')

        kwargs = {}

        for emp in Employee.objects.all():
            kwargs['service'] = emp.services.first()
            kwargs['start'] = util.next_wednesday().replace(hour=9, minute=00)
            kwargs['employee'] = emp
            for customer in Customer.objects.all():
                if customer.owner_id == emp.owner_id:
                    kwargs['customer'] = customer
                    Appointment.objects.create(**kwargs)
                    kwargs['start'] = kwargs['start'] + kwargs['service'].duration_delta()

    def assertCreated(self, response, emp, customer, service):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['employee']['id'], emp.id)
        self.assertEqual(response.data['customer']['id'], customer.id)
        if service is None:
            self.assertEqual(response.data['service'], None)
        else:
            self.assertEqual(response.data['service']['id'], service.id)

    def test_anonymous_list(self):
        """
        Anonymous users trying to access appointments
        shouldn't have access to anything
        """
        detail_url = reverse('appointment-detail', kwargs={'pk': Appointment.objects.first().id})
        self.ensure_all_unauthorized(detail_url)

    def test_anonymous_create(self):
        """
        trying to book an appointment without being logged in
        Should return 401 unauthorized
        """
        emp, customer, service = emp_customer_service()
        data = create_apt_data(emp, customer, service, util.next_wednesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_list(self):
        """
        Customer trying to access all appointments
        The return list should only show appointments for to the logged in customer
        """
        customer = Customer.objects.first()
        customer.user = test_user(customer)
        self.client.force_authenticate(user=customer.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        [self.assertEqual(apt['customer']['id'], customer.id) for apt in response.data]

    def test_customer_list_with_no_appointments(self):
        """
        Customer trying to access all appointments
        The return list should only show appointments for to the logged in customer
        """
        user = test_user()
        self.client.force_authenticate(user=user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_customer_create(self):
        """
        trying to book an appointment as a customer with the customer id as the receiver
        should allow the service to be booked
        """
        emp, customer, service = emp_customer_service()
        customer.user = test_user(customer)
        self.client.force_authenticate(user=customer.user)  # authenticates as customer
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertCreated(response, emp, customer, service)

    def test_customer_create_self_appointment(self):
        emp, customer, service = emp_customer_service()
        customer.user = test_user(customer)
        self.client.force_authenticate(user=customer.user)  # authenticates as customer
        data = create_self_apt_data(emp, customer, util.next_tuesday().replace(hour=10, minute=0),
                                    util.next_tuesday().replace(hour=11, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_create_omitting_service(self):
        emp, customer, service = emp_customer_service()
        customer.user = test_user(customer)
        self.client.force_authenticate(user=customer.user)  # authenticates as customer
        data = create_self_apt_data(customer, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_create_omitting_customer(self):
        """
        omitting the customer value should return an error
        to the customer logged in
        """
        emp, customer, service = emp_customer_service()
        customer.user = test_user(customer)
        self.client.force_authenticate(user=customer.user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        del (data['customer'])
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_create_for_other_customer(self):
        """
        trying to book an appointment as a customer with someone else's customer id as the receiver
        Should return forbidden
        """
        emp, customer, service = emp_customer_service()
        user = test_user()
        self.client.force_authenticate(user=user)
        data = create_apt_data(emp, customer, service, util.next_wednesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_list(self):
        """
        employee trying to access all appointments
        Should only see his appointments
        """
        emp = Employee.objects.first()
        emp.user = test_user(emp)
        self.client.force_authenticate(user=emp.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        [self.assertEqual(apt['employee']['id'], emp.id) for apt in response.data]

    def test_employee_create(self):
        """
        employee trying to create an appointment to himself
        should create appointment
        """
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        self.client.force_authenticate(user=emp.user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertCreated(response, emp, customer, service)

    def test_employee_create_self_appointment(self):
        """
        employee trying to create an appointment to himself
        should create appointment
        """
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        self.client.force_authenticate(user=emp.user)
        data = create_self_apt_data(emp, emp, util.next_tuesday().replace(hour=10, minute=0),
                                    util.next_tuesday().replace(hour=11, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertCreated(response, emp, emp, None)

    def test_employee_create_omitting_employee(self):
        """
        Should not create an appointment if the employee id is omitted
        """
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        self.client.force_authenticate(user=emp.user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        del (data['employee'])
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_create_for_other_employee(self):
        """
        Employee trying to book an appointment to another employee
        should return 401 unauthorized
        """
        company = Company.objects.first()
        emp, customer, service = emp_customer_service(company)
        emp2 = company.employee_set.last()
        emp2.user = test_user(emp2)
        self.client.force_authenticate(user=emp2.user)
        data = create_apt_data(emp, customer, service, util.next_wednesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_list(self):
        """
        A user with read access should be able to view appointments for anyone in the company
        """
        user = User.objects.get(pk=1)
        user.groups.add(util.appointment_permissions())
        self.client.force_authenticate(user=user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        [self.assertEqual(apt['employee']['owner']['name'], user.company.name) for apt in response.data]

    def test_admin_create(self):
        """
        A user with with access should be able to create appointments for anyone in the company
        """
        emp, customer, service = emp_customer_service()
        user = User.objects.get(pk=1)
        user.groups.add(util.appointment_permissions())
        self.client.force_authenticate(user=user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_create_different_company(self):
        """
        A user with with access should be able to create appointments for anyone in the company
        """
        emp, customer, service = emp_customer_service(Company.objects.get(pk=2))
        user = User.objects.get(pk=1)
        user.groups.add(util.appointment_permissions())
        self.client.force_authenticate(user=user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_overlapping_appointments(self):
        """
        overlapping appointments shouldn't be able to be created and should return the proper response
        """
        emp, customer, service = emp_customer_service()
        customer.user = test_user(customer)
        self.client.force_authenticate(user=customer.user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        first_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(first_post.status_code, status.HTTP_201_CREATED)
        second_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(second_post.status_code, status.HTTP_403_FORBIDDEN)


class CompanyViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('company-list')

    def test_anonymous_create_company(self):
        data = {'name': 'test'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):
        user = test_user()
        self.client.force_authenticate(user=user)
        user.groups.add(util.company_permissions())
        data = {'name': 'test'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=user.pk)
        self.assertIsNotNone(user.company)
        print(user.get_all_permissions())
        perm = []
        permissions = ['appointment', 'employee', 'shift', 'schedule', 'service']
        for name in permissions:
            perm.extend(Permission.objects.filter(codename__endswith=name))
        for p in perm:
            self.assertTrue(user.has_perm(f'{p.content_type.app_label}.{p.codename}'))

    def test_user_create_twice(self):
        user = test_user()
        self.client.force_authenticate(user=user)
        user.groups.add(util.company_permissions())
        data = {'name': 'test'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=user.pk)
        self.assertIsNotNone(user.company)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

