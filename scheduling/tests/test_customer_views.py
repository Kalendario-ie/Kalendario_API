from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from scheduling.models import Appointment
from scheduling.tests.util import TestHelper, datetime, next_tuesday


class AppointmentViewSetTest(APITestCase):

    def setUp(self):
        self.helper = TestHelper()

    def test_list_anonymous_user_access(self):
        """
        Ensure that anonymous users have no access to list
        """
        url = reverse('c-appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        """
        When the customer is authenticated the system should return 200
        """
        url = reverse('c-appointment-list')
        self.client.force_authenticate(user=self.helper.customerA)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employees_cant_access_this_view(self):
        """
        employees will have their own viewset and shouldn't have access to this view
        """
        url = reverse('c-appointment-list')
        print(self.helper.employeeA.user.is_staff)
        self.client.force_authenticate(user=self.helper.employeeA.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_should_show_current_users_appointments_only(self):
        """
        When the customer is authenticated the system should return 200
        """
        url = reverse('c-appointment-list')
        Appointment.objects.create(customer=self.helper.customerA, employee=self.helper.employeeA,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=00))
        Appointment.objects.create(customer=self.helper.customerB, employee=self.helper.employeeA,
                                   service=self.helper.service, start=next_tuesday().replace(hour=9, minute=30))
        self.client.force_authenticate(user=self.helper.customerA)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_unauthenticated(self):
        url = reverse('c-appointment-list')
        data = {'employee': self.helper.employeeA.id,
                'customer': self.helper.customerA.id,
                'service': self.helper.employeeA.services.first().id,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_appointment(self):
        """
        customer should be able to create appointment for himslef
        :return:
        """
        url = reverse('c-appointment-list')
        self.client.force_authenticate(user=self.helper.customerA)
        empId = self.helper.employeeA.id
        customerId = self.helper.customerA.id
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': empId,
                'customer': customerId,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee'], empId)
        self.assertEqual(response.data['customer'], customerId)
        self.assertEqual(response.data['service'], serviceId)

    def test_create_appointment_omitting_customer(self):
        """
        requesting creation without the customer id should still book an appointment
        to the customer logged in
        """
        url = reverse('c-appointment-list')
        self.client.force_authenticate(user=self.helper.customerA)
        empId = self.helper.employeeA.id
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': empId,
                'service': serviceId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee'], empId)
        self.assertEqual(response.data['customer'], self.helper.customerA.id)
        self.assertEqual(response.data['service'], serviceId)

    def test_create_appointment_another_customer(self):
        """
        requesting creation without the customer id should still book an appointment
        to the customer logged in
        """
        url = reverse('c-appointment-list')
        self.client.force_authenticate(user=self.helper.customerA)
        empId = self.helper.employeeA.id
        customerId = self.helper.customerB.id
        serviceId = self.helper.employeeA.services.first().id
        data = {'employee': empId,
                'service': serviceId,
                'customer': customerId,
                'start': next_tuesday().replace(hour=10, minute=0).__str__()
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['employee'], empId)
        self.assertEqual(response.data['customer'], self.helper.customerA.id)
        self.assertEqual(response.data['service'], serviceId)
