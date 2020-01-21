from django.urls import reverse
from rest_framework import status
from scheduling.models import Appointment, SelfAppointment, Person
from scheduling.tests.generics import ViewTestCase
from scheduling.tests.util import TestHelper, next_tuesday


# TODO: test filtering when the parameters are not right
class AppointmentViewSetTest(ViewTestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.list_url = reverse('appointment-list')

    def test_anonymous_user_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        appointment = Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeA,
                                                 service=self.helper.service,
                                                 start=next_tuesday().replace(hour=9, minute=00))
        detail_url = reverse('appointment-detail', kwargs={'pk': appointment.id})
        self.ensure_all_unauthorized(detail_url)

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
        emp = self.helper.employeeA
        service = self.helper.employeeA.services.first()
        data = {'employee': emp.id,
                'customer': customer.id,
                'service': service.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee']['id'], emp.id)
        self.assertEqual(response.data['customer']['id'], customer.id)
        self.assertEqual(response.data['service']['id'], service.id)

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

        self.assertEqual(response.data['employee']['id'], emp.id)
        self.assertEqual(response.data['customer']['id'], customerId)
        self.assertEqual(response.data['service']['id'], serviceId)

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

    def test_create_overlapping_appointments(self):
        """
        overlapping appointments shouldn't be able to be created and should return the proper response
        """
        customer = self.helper.customerA
        self.client.force_authenticate(user=customer.user)
        emp = self.helper.employeeA
        service = self.helper.employeeA.services.first()
        data = {'employee': emp.id,
                'customer': customer.id,
                'service': service.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        first_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(first_post.status_code, status.HTTP_201_CREATED)

        second_post = self.client.post(self.list_url, data, format='json')

        self.assertEqual(second_post.status_code, status.HTTP_403_FORBIDDEN)


class SelfAppointmentViewSetTest(ViewTestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.list_url = reverse('self-appointment-list')

    def test_anonymous_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        sa = SelfAppointment.objects.create(employee=self.helper.employeeA,
                                            start=next_tuesday().replace(hour=9, minute=00),
                                            end=next_tuesday().replace(hour=10, minute=00))
        detail_url = reverse('self-appointment-detail', kwargs={'pk': sa.id})
        self.ensure_all_unauthorized(detail_url)

    def test_customer_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        sa = SelfAppointment.objects.create(employee=self.helper.employeeA,
                                            start=next_tuesday().replace(hour=9, minute=00),
                                            end=next_tuesday().replace(hour=10, minute=00))
        detail_url = reverse('self-appointment-detail', kwargs={'pk': sa.id})
        self.client.force_authenticate(user=self.helper.customerA.user)
        self.ensure_all_forbidden(detail_url)

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

        self.assertEqual(response.data['employee']['id'], emp.id)

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

    def test_create_overlapping_appointments(self):
        """
        overlapping appointments shouldn't be able to be created and should return the proper response
        """
        self.client.force_authenticate(user=self.helper.scheduler)

        data = {'employee': self.helper.employeeA.id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__(),
                'end': next_tuesday().replace(hour=11, minute=0).__str__()
                }

        first_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(first_post.status_code, status.HTTP_201_CREATED)

        second_post = self.client.post(self.list_url, data, format='json')
        self.assertEqual(second_post.status_code, status.HTTP_403_FORBIDDEN)


# class CustomerViewSetTest(ViewTestCase):
#     list_url = reverse('customer-list')
#
#     def setUp(self):
#         self.helper = TestHelper()
#         Person.objects.create(first_name='Gustavo', last_name='Francelino')
#         Person.objects.create(first_name='Isabela', last_name='Loz')
#         Person.objects.create(first_name='Gleyci', last_name='Figueiredo')
#         Person.objects.create(first_name='Amanda', last_name='Francelino')
#         Person.objects.create(first_name='Guilherme', last_name='Portugues')
#
#     def test_unauthenticated_access(self):
#         """
#         Shouldn't be able to retrieve any data when unauthenticated
#         """
#         customer = self.helper.customerA
#         detail_url = reverse('customer-detail', kwargs={'pk': customer.id})
#         self.ensure_all_unauthorized(detail_url)
#
#     def test_customer_access(self):
#         """
#         Customer shouldn't be able to see access this view
#         """
#         auth_customer, check_customer = self.helper.customerA, self.helper.customerB
#         self.client.force_authenticate(user=auth_customer.user)
#         detail_url = reverse('customer-detail', kwargs={'pk': check_customer.id})
#         self.ensure_all_forbidden(detail_url)
#
#         customer = self.helper.customerA
#         self.client.force_authenticate(user=customer.user)
#         detail_url = reverse('customer-detail', kwargs={'pk': customer.id})
#         self.ensure_all_forbidden(detail_url)
#
#     def test_search_2_letters(self):
#         url = reverse('customer-list')
#         data = {'search': 'gu'}
#         self.client.force_authenticate(user=self.helper.employeeA.user)
#         response = self.client.get(url, data=data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 3)
