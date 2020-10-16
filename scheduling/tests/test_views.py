from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status

import scheduling.tests.util as util
from core.models import User
from scheduling.models import Appointment, Person, Employee, Customer, Company, Schedule
from scheduling.tests.generics import ViewTestCase


def employee_user():
    user = User.objects.get(pk=1)
    user.employee = Employee.objects.filter(owner=1).first()
    user.save()
    return user


def create_apt_data(emp, customer, service, date):
    return {'employee': emp.id,
            'customer': customer.id,
            'service': service.id,
            'start': str(date),
            'owner': emp.owner_id
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


def company_a_owner():
    user = User.objects.get(pk=1)
    util.add_permissions(user, 'employee')
    return user


def emp_service(company=Company.objects.first()):
    emp = company.employee_set.first()
    service = emp.services.first()
    return emp, service


def emp_customer_service(company=Company.objects.first()):
    emp, service = emp_service(company)
    return emp, company.customer_set.first(), service


class AppointmentViewSetTest(ViewTestCase):
    """
    Tests should follow the convention of test_<type of user>_<action type>_<extra information>
    Customer: user that has no company but belongs to the appointment
    Employee: Belongs to the company of the object but has no permissions
    Admin: Has a company and the correct rights
    """

    def setUp(self):
        self.list_url = reverse('appointment-list')

        kwargs = {}

        for emp in Employee.objects.all():
            kwargs['service'] = emp.services.first()
            kwargs['start'] = util.next_wednesday().replace(hour=9, minute=00)
            kwargs['employee'] = emp
            kwargs['owner'] = emp.owner
            for customer in Customer.objects.all():
                if customer.owner_id == emp.owner_id:
                    kwargs['customer'] = customer
                    kwargs['status'] = 'A'
                    Appointment.objects.create(**kwargs)
                    kwargs['start'] = kwargs['start'] + kwargs['service'].duration

    def assertCreated(self, response, emp, customer, service):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['employee']['id'], emp.id)
        self.assertEqual(response.data['customer']['id'], customer.id)
        if service is None:
            self.assertEqual(response.data['service'], None)
        else:
            self.assertEqual(response.data['service']['id'], service.id)

    def assertPending(self, response):
        self.assertEqual(response.data['status'], 'P')

    def assertAccepted(self, response):
        self.assertEqual(response.data['status'], 'A')

    def test_anonymous_list(self):
        detail_url = reverse('appointment-detail', kwargs={'pk': Appointment.objects.first().id})
        self.ensure_all_unauthorized(detail_url)

    def test_anonymous_create(self):
        emp, customer, service = emp_customer_service()
        data = create_apt_data(emp, customer, service, util.next_wednesday().replace(hour=10, minute=0))

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_list(self):
        user = test_user()
        self.client.force_authenticate(user=user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_create_pending(self):
        emp, service = emp_service()
        user = test_user()
        data = create_apt_data(emp, user.person, service, util.next_tuesday().replace(hour=10, minute=0))

        self.client.force_authenticate(user=user)  # authenticates as customer
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_view(self):
        user = test_user()

        self.client.force_authenticate(user=user)
        get_response = self.client.get(self.list_url + f"1/", format='json')

        self.assertEqual(get_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_view_for_other_customer(self):
        appointments = list(Appointment.objects.all())

        self.client.force_authenticate(user=test_user())
        responses = []
        for appointment in appointments:
            responses.append(self.client.get(self.list_url + f"{appointment.id}/", format='json'))

        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_delete_for_other_customer(self):
        appointments = list(Appointment.objects.all())

        self.client.force_authenticate(user=test_user())
        responses = []
        for appointment in appointments:
            responses.append(self.client.delete(self.list_url + f"{appointment.id}/", format='json'))

        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_list(self):
        user = employee_user()
        self.client.force_authenticate(user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for apt in response.data['results']:
            self.assertEqual(apt['employee']['id'], user.employee_id)

    def test_employee_create_pending(self):
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        data['status'] = 'P'

        self.client.force_authenticate(user=emp.user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_create_accepted(self):
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        data['status'] = 'A'

        self.client.force_authenticate(user=emp.user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_create_self_appointment(self):
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        data = create_self_apt_data(emp, emp, util.next_tuesday().replace(hour=10, minute=0),
                                    util.next_tuesday().replace(hour=11, minute=0))

        self.client.force_authenticate(user=emp.user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_create_omitting_employee(self):
        emp, customer, service = emp_customer_service()
        emp.user = test_user(emp)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        del (data['employee'])

        self.client.force_authenticate(user=emp.user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_create_for_other_employee(self):
        company = Company.objects.first()
        emp, customer, service = emp_customer_service(company)
        emp2 = company.employee_set.last()
        emp2.user = test_user(emp2)
        data = create_apt_data(emp, customer, service, util.next_wednesday().replace(hour=10, minute=0))

        self.client.force_authenticate(user=emp2.user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_view(self):
        emp = Employee.objects.first()
        apt = Appointment.objects.filter(employee=emp).first()
        user = test_user(emp)

        self.client.force_authenticate(user=user)
        get_response = self.client.get(self.list_url + f"{apt.id}/", format='json')

        self.assertEqual(get_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_list(self):
        user = User.objects.get(pk=1)
        user.groups.add(util.company_1_master_group())

        self.client.force_authenticate(user=user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertGreater(len(results), 0)
        [self.assertEqual(apt['employee']['owner'], user.owner_id) for apt in results]

    def test_admin_create(self):
        emp, customer, service = emp_customer_service()
        user = User.objects.get(pk=1)
        user.groups.add(util.company_1_master_group())
        self.client.force_authenticate(user=user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_create_self_appointment(self):
        emp, customer, service = emp_customer_service()
        user = User.objects.get(pk=1)
        user.groups.add(util.company_1_master_group())
        data = create_self_apt_data(emp, emp, util.next_tuesday().replace(hour=10, minute=0),
                                    util.next_tuesday().replace(hour=11, minute=0))

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url + 'lock/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_create_self_appointment_with_service(self):
        emp, customer, service = emp_customer_service()
        user = User.objects.get(pk=1)
        user.groups.add(util.company_1_master_group())
        data = create_self_apt_data(emp, emp, util.next_tuesday().replace(hour=10, minute=0),
                                    util.next_tuesday().replace(hour=11, minute=0))
        data['service'] = 0

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url + 'lock/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_create_different_company(self):
        emp, customer, service = emp_customer_service(Company.objects.get(pk=2))
        user = User.objects.filter(owner_id=1).first()
        user.groups.add(util.company_1_master_group())
        self.client.force_authenticate(user=user)
        data = create_apt_data(emp, customer, service, util.next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class CompanyViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('company-list')

    def test_anonymous_create_company(self):
        data = {'name': 'test'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):
        user = test_user()
        util.add_permissions(user, 'company')

        perm = []
        for name in ['appointment', 'employee', 'shift', 'schedule', 'service']:
            perm.extend(Permission.objects.filter(codename__endswith=name))
        perm = [f'{p.content_type.app_label}.{p.codename}' for p in perm]
        # Initial assertions that the user doesn't have a company and permissions to edit
        self.assertIsNone(user.owner)
        self.assertFalse(user.has_perms(perm))

        # Create a company through the api endpoint
        self.client.force_authenticate(user=user)
        data = {'name': 'test'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # reloads the user to update the permissions
        user = User.objects.get(pk=user.id)
        p = user.get_all_permissions()
        # checks that the user now has a company full permissions to edit company models
        # and no permissions to create other companies
        self.assertIsNotNone(user.owner)
        self.assertTrue(user.has_perms(perm))
        self.assertFalse(user.has_perm('scheduling.add_company'))

    def test_user_create_twice(self):
        user = test_user()
        util.add_permissions(user, 'company')

        self.client.force_authenticate(user=user)
        data = {'name': 'test'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=user.pk)
        self.assertIsNotNone(user.owner)

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('employee-list')

    def detail_url(self, id):
        return f'{self.list_url}{id}/'

    def emp_data(self, extra):
        data = {'firstName': 'empName',
                'lastName': 'empSurname',
                'email': 'emp@email.com',
                'phone': '0900'}
        data.update(extra)
        return data

    def test_company_a_owner_create(self):
        user = company_a_owner()
        data = self.emp_data({'services': [1], 'owner': 1})

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_company_a_owner_create_on_different_company(self):
        """
        Even if the request for creating an employee comes with a different owner number
        The system should always create the employee in the user's company
        """
        user = company_a_owner()
        data = self.emp_data({'services': [1], 'owner': 2})

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')
        emp_id = response.data.get('id')
        created = Employee.objects.get(pk=emp_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created.owner_id, user.owner_id)

    def test_company_a_owner_create_with_different_service(self):
        """
        The service list should only contain services that belong to the same owner for the employee
        """
        user = company_a_owner()
        data = self.emp_data({'services': [3], 'owner': 1})

        self.client.force_authenticate(user=user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_update_employee_from_other_company(self):
        """Trying to edit the employee from another company by providing misleading data"""
        user = company_a_owner()
        data = self.emp_data({'services': [1], 'owner': 1})

        self.client.force_authenticate(user=user)
        response = self.client.patch(self.detail_url(3), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_from_a_different_company(self):
        user = company_a_owner()
        self.client.force_authenticate(user=user)
        response = self.client.get(self.detail_url(3), format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RequestViewSetTest(ViewTestCase):
    def setUp(self):
        self.list_url = reverse('request-list')

    def accept_url(self, id):
        return f'{self.list_url}{id}/accept/'

    def reject_url(self, id):
        return f'{self.list_url}{id}/reject/'

    def test_admin_accept_request(self):
        user = User.objects.get(pk=1)
        user.enable_company_editing(1)

        self.client.force_authenticate(user=user)
        response = self.client.patch(self.accept_url(1), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'A')


class CustomerViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('customer-list')

    def detail_url(self, id=Customer.objects.first().id):
        return reverse('customer-detail', kwargs={'pk': id})

    def test_anonymous_user_all_unauthorized(self):
        self.ensure_all_unauthorized(self.detail_url())

    def test_common_user_all_unauthorized(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)
        self.ensure_all_forbidden(self.detail_url())

    def test_employee_user_list(self):
        self.client.force_authenticate(employee_user())

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_list(self):
        user = User.objects.get(pk=1)
        user.enable_company_editing(1)

        self.client.force_authenticate(user)

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ServiceViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('service-list')

    def detail_url(self, id=Customer.objects.first().id):
        return reverse('service-detail', kwargs={'pk': id})

    def test_anonymous_user_all_unauthorized(self):
        self.ensure_all_unauthorized(self.detail_url())

    def test_common_user_all_unauthorized(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)
        self.ensure_all_forbidden(self.detail_url())

    def test_employee_user_list(self):
        self.client.force_authenticate(employee_user())

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_list(self):
        user = User.objects.get(pk=1)
        user.enable_company_editing(1)

        self.client.force_authenticate(user)

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ScheduleViewSetTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('schedule-list')

    def detail_url(self, sid=Schedule.objects.first().id):
        return reverse('schedule-detail', kwargs={'pk': sid})

    def test_anonymous_user_all_unauthorized(self):
        self.ensure_all_unauthorized(self.detail_url())

    def test_common_user_all_unauthorized(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)
        self.ensure_all_forbidden(self.detail_url())

    def test_employee_user_list(self):
        self.client.force_authenticate(employee_user())

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_list(self):
        user = User.objects.get(pk=1)
        user.enable_company_editing(1)

        self.client.force_authenticate(user)

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_create(self):
        user = User.objects.get(pk=1)
        user.enable_company_editing(1)

        self.client.force_authenticate(user)

        data = {
            'name': 'teste',
            'mon': {'frames': [{'start': "09:00", 'end': "10:00"}]},
            'tue': {'frames': []},
            'wed': {'frames': []},
            'thu': {'frames': []},
            'fri': {'frames': []},
            'sat': {'frames': []},
            'sun': {'frames': []},
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
