from django.urls import reverse
from rest_framework import status
from scheduling.models import Appointment, SelfAppointment, Person
from scheduling.tests.generics import ViewTestCase
from scheduling.tests.util import TestHelper, next_tuesday, next_wednesday


def create_apt_data(emp, customer, service, date):
    return {'employee': emp.id,
            'customer': customer.id,
            'service': service.id,
            'start': str(date)
            }


# TODO: test filtering when the parameters are not right
class AppointmentViewSetTest(ViewTestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.list_url = reverse('appointment-list')

    def emp_customer_service(self):
        emp, customer = self.helper.employees.pop(), self.helper.customers.pop()
        service = emp.services.first()
        return emp, customer, service

    def assertCreated(self, response, emp, customer, service):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['employee']['id'], emp.id)
        self.assertEqual(response.data['customer']['id'], customer.id)
        self.assertEqual(response.data['service']['id'], service.id)

    def test_detail_anonymous_user_access(self):
        """
        Anonymous users trying to access appointments
        shouldn't have access to anything
        """
        detail_url = reverse('appointment-detail', kwargs={'pk': self.helper.appointments[0].id})
        self.ensure_all_unauthorized(detail_url)

    def test_list_auth_as_customer(self):
        """
        Customer trying to access all appointments
        The return list should only show appointments for to the logged in customer
        """
        customer = self.helper.customers[0]
        self.client.force_authenticate(user=customer.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        [self.assertEqual(apt['customer']['id'], customer.id) for apt in response.data]

    def test_list_auth_as_employee(self):
        """
        employee trying to access all appointments
        Should only see his appointments
        """
        emp = self.helper.employees.pop()
        self.client.force_authenticate(user=emp.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        [self.assertEqual(apt['employee']['id'], emp.id) for apt in response.data]

    def test_list_auth_as_company_admin(self):
        """
        Company admin tries to access all appointments
        Should return only appointments to his company
        """
        c_admin = self.helper.admins.pop()
        self.client.force_authenticate(user=c_admin.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        [self.assertEqual(apt['employee']['company']['name'], c_admin.company.name) for apt in response.data]

    def test_create_unauthenticated(self):
        """
        trying to book an appointment without being logged in
        Should return 401 unauthorized
        """
        emp, customer, service = self.emp_customer_service()
        data = create_apt_data(emp, customer, service, next_wednesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_auth_as_customer(self):
        """
        trying to book an appointment as a customer with the customer id as the receiver
        should allow the service to be booked
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=customer.user)  # authenticates as customer
        data = create_apt_data(emp, customer, service, next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertCreated(response, emp, customer, service)

    def test_create_auth_as_customer_omitting_customer(self):
        """
        omitting the customer value should return an error
        to the customer logged in
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=customer.user)
        data = {'employee': emp.id,
                'service': service.id,
                'start': str(next_wednesday().replace(hour=10, minute=0))
                }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auth_as_another_customer(self):
        """
        trying to book an appointment as a customer with someone else's customer id as the receiver
        Should return forbidden
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=self.helper.customers.pop().user)
        data = create_apt_data(emp, customer, service, next_wednesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_auth_as_employee(self):
        """
        employee trying to create an appointment to himself
        should create appointment
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=emp.user)
        data = create_apt_data(emp, customer, service, next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertCreated(response, emp, customer, service)

    def test_create_omitting_employee(self):
        """
        Should not create an appointment if the employee id is omitted
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=customer.user)
        data = create_apt_data(emp, customer, service, next_wednesday().replace(hour=10, minute=0))
        del(data['employee'])
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auth_as_employee_another_employee(self):
        """
        Employee trying to book an appointment to another employee
        should return 401 unauthorized
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=self.helper.employees.pop().user)
        data = create_apt_data(emp, customer, service, next_wednesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated_as_company_admin(self):
        """
        A scheduler should have access to read/write appointments
        A scheduler user doesn't need to be linked to an employee to book appointments
        A scheduled should be able to book appointments to any employees.
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=self.helper.admins[0].user)
        data = create_apt_data(emp, customer, service, next_tuesday().replace(hour=10, minute=0))
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_overlapping_appointments(self):
        """
        overlapping appointments shouldn't be able to be created and should return the proper response
        """
        emp, customer, service = self.emp_customer_service()
        self.client.force_authenticate(user=customer.user)
        data = create_apt_data(emp, customer, service, next_tuesday().replace(hour=10, minute=0))
        first_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(first_post.status_code, status.HTTP_201_CREATED)
        second_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(second_post.status_code, status.HTTP_403_FORBIDDEN)


class SelfAppointmentViewSetTest(ViewTestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.list_url = reverse('self-appointment-list')
        self.emp1 = self.helper.employees[0]
        self.emp2 = self.helper.employees[1]
        self.cust1 = self.helper.customers[0]

    def test_anonymous_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        sa = SelfAppointment.objects.create(employee=self.emp1,
                                            start=next_tuesday().replace(hour=9, minute=00),
                                            end=next_tuesday().replace(hour=10, minute=00))
        detail_url = reverse('self-appointment-detail', kwargs={'pk': sa.id})
        self.ensure_all_unauthorized(detail_url)

    def test_customer_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        sa = SelfAppointment.objects.create(employee=self.emp1,
                                            start=next_tuesday().replace(hour=9, minute=00),
                                            end=next_tuesday().replace(hour=10, minute=00))
        detail_url = reverse('self-appointment-detail', kwargs={'pk': sa.id})
        self.client.force_authenticate(user=self.cust1.user)
        self.ensure_all_forbidden(detail_url)

    def test_list_authenticated_as_employee(self):
        """
        Employee trying to access all appointments
        Should only see his appointments
        """
        SelfAppointment.objects.create(employee=self.emp1,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        SelfAppointment.objects.create(employee=self.emp2,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        self.client.force_authenticate(user=self.emp1.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_authenticated_as_scheduler(self):
        """
        Scheduler trying to access all appointments
        Should see all appointments
        """
        SelfAppointment.objects.create(employee=self.emp1,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        SelfAppointment.objects.create(employee=self.emp2,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        self.client.force_authenticate(user=self.helper.scheduler)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_unauthenticated(self):
        data = {'employee': self.emp1.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated_as_customer(self):
        """
        Customers shouldn't create appointments throw this view
        """
        self.client.force_authenticate(user=self.cust1.user)
        data = {'employee': self.emp1.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_authenticated_as_employee(self):
        """
        employee should be able to create appointment for himself
        """
        emp = self.emp1
        self.client.force_authenticate(user=emp.user)
        data = {'employee': self.emp1.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee']['id'], emp.id)

    def test_create_omitting_employee(self):
        """
        Should not create an appointment if the employee id is omitted
        """
        self.client.force_authenticate(user=self.emp1.user)
        data = {
            'start': next_tuesday().replace(hour=10, minute=0).__str__(),
            'end': next_tuesday().replace(hour=11, minute=0).__str__()
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_another_employee(self):
        """
        Should not be able to create an appointment to another employee
        """
        emp = self.emp1
        other_emp = self.emp2
        self.client.force_authenticate(user=emp.user)
        data = {'employee': other_emp.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=11, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated_as_scheduler(self):
        """
        A scheduler should have access to read/write appointments
        A scheduler user doesn't need to be linked to an employee to book appointments
        A scheduled should be able to book appointments to any employees.
        """
        self.client.force_authenticate(user=self.helper.scheduler)

        data = {'employee': self.emp1.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=11, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_overlapping_appointments(self):
        """
        overlapping appointments shouldn't be able to be created and should return the proper response
        """
        self.client.force_authenticate(user=self.helper.scheduler)

        data = {'employee': self.emp1.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=11, minute=0).__str__()
                }

        first_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(first_post.status_code, status.HTTP_201_CREATED)

        second_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(second_post.status_code, status.HTTP_403_FORBIDDEN)
