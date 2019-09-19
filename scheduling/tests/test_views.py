from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from scheduling.models import Appointment, SelfAppointment, Customer
from scheduling.tests.util import TestHelper, next_tuesday


# TODO: test filtering when the parameters are not right
class AppointmentViewSetTest(APITestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.list_url = reverse('appointment-list')

    def test_list_anonymous_user_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_auth_as_customer(self):
        """
        When the customer is authenticated the system should return 200
        The return list should only show appointments for to the logged in customer
        """
        Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeA,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=00))
        Appointment.objects.create(customer=self.helper.customerB, employee=self.helper.employeeA,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=30))
        self.client.force_authenticate(user=self.helper.customerA.user)
        aps = Appointment.objects.all()
        print(aps)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_auth_as_employee(self):
        """
        Employee trying to access all appointments
        Should only see his appointments
        """
        Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeA,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=00))
        Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeB,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=30))
        self.client.force_authenticate(user=self.helper.employeeA.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_auth_as_scheduler(self):
        """
        Scheduler trying to access all appointments
        Should see all appointments
        """
        Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeA,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=00))
        Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeB,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=30))
        self.client.force_authenticate(user=self.helper.scheduler)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_unauthenticated(self):
        data = {'employee': self.helper.employeeA.id,
                'customer': self.helper.customerA.id,
                'service': self.helper.employeeA.services.first().id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_auth_as_customer(self):
        """
        customer should be able to create appointment for himslef
        """
        customer = self.helper.customerA
        self.client.force_authenticate(user=customer.user)
        empId = self.helper.employeeA.id
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': empId,
                'customer': customer.id,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee'], empId)
        self.assertEqual(response.data['customer'], customer.id)
        self.assertEqual(response.data['service'], serviceId)

    def test_create_auth_as_customer_omitting_customer(self):
        """
        omitting the customer value should return an error
        to the customer logged in
        """
        customer = self.helper.customerA
        self.client.force_authenticate(user=customer.user)
        empId = self.helper.employeeA.id
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': empId,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auth_as_another_customer(self):
        """
        User trying to book an appointment for a customer that's not linked to that user account
        Should return forbidden
        """
        self.client.force_authenticate(user=self.helper.customerA.user)
        emp = self.helper.employeeA
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': emp.id,
                'service': serviceId,
                'customer': self.helper.customerB.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_auth_as_employee(self):
        """
        employee should be able to create appointment for himself
        """
        emp = self.helper.employeeA
        self.client.force_authenticate(user=emp.user)
        customerId = self.helper.customerA.id
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': emp.id,
                'customer': customerId,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee'], emp.id)
        self.assertEqual(response.data['customer'], customerId)
        self.assertEqual(response.data['service'], serviceId)

    def test_create_auth_as_employee_another_employee(self):
        """
        Employee trying to book an appointment to another employee
        """
        serviceId = self.helper.employeeA.services.first().id
        self.client.force_authenticate(user=self.helper.employeeA.user)

        data = {'employee': self.helper.employeeB.id,
                'service': serviceId,
                'customer': self.helper.customerA.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated_as_scheduler(self):
        """
        A scheduler should have access to read/write appointments
        A scheduler user doesn't need to be linked to an employee to book appointments
        A scheduled should be able to book appointments to any employees.
        """
        emp = self.helper.employeeA
        customer = self.helper.customerA
        serviceId = self.helper.employeeA.services.first().id

        self.client.force_authenticate(user=self.helper.scheduler)

        data = {'employee': emp.id,
                'customer': customer.id,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_omitting_employee(self):
        """
        Should not create an appointment if the employee id is omitted
        """
        self.client.force_authenticate(user=self.helper.employeeA.user)
        customer = self.helper.customerA
        serviceId = self.helper.employeeA.services.first().id
        data = {'customer': customer.id,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SelfAppointmentViewSetTest(APITestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.list_url = reverse('self-appointment-list')

    def test_list_anonymous_user_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated_as_customer(self):
        """
        A customer shouldn't have access to this view at all
        """
        self.client.force_authenticate(user=self.helper.customerA.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_authenticated_as_employee(self):
        """
        Employee trying to access all appointments
        Should only see his appointments
        """
        SelfAppointment.objects.create(employee=self.helper.employeeA,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        SelfAppointment.objects.create(employee=self.helper.employeeB,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        self.client.force_authenticate(user=self.helper.employeeA.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_authenticated_as_scheduler(self):
        """
        Scheduler trying to access all appointments
        Should see all appointments
        """
        SelfAppointment.objects.create(employee=self.helper.employeeA,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        SelfAppointment.objects.create(employee=self.helper.employeeB,
                                       start=next_tuesday().replace(hour=9, minute=00),
                                       end=next_tuesday().replace(hour=10, minute=00))
        self.client.force_authenticate(user=self.helper.scheduler)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_unauthenticated(self):
        data = {'employee': self.helper.employeeA.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated_as_customer(self):
        """
        Customers shouldn't create appointments throw this view
        """
        self.client.force_authenticate(user=self.helper.customerA.user)
        data = {'employee': self.helper.employeeA.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_authenticated_as_employee(self):
        """
        employee should be able to create appointment for himself
        """
        emp = self.helper.employeeA
        self.client.force_authenticate(user=emp.user)
        data = {'employee': self.helper.employeeA.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee'], emp.id)

    def test_create_omitting_employee(self):
        """
        Should not create an appointment if the employee id is omitted
        """
        self.client.force_authenticate(user=self.helper.employeeA.user)
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
        emp = self.helper.employeeA
        other_emp = self.helper.employeeB
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

        data = {'employee': self.helper.employeeA.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=11, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CustomerViewSetTest(APITestCase):

    def setUp(self):
        Customer.objects.create(first_name='Gustavo', last_name='Francelino')
        Customer.objects.create(first_name='Isabela', last_name='Loz')
        Customer.objects.create(first_name='Gleyci', last_name='Figueiredo')
        Customer.objects.create(first_name='Amanda', last_name='Francelino')
        Customer.objects.create(first_name='Guilherme', last_name='Portugues')

    def test_search_2_letters(self):
        url = reverse('customer-list')
        data = {'search': 'gu'}
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
