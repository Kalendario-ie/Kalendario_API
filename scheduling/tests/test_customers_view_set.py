from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from scheduling.models import Customer


class CustomerViewSetTest(APITestCase):

    def setUp(self):
        Customer.objects.create(first_name='Gustavo', last_name='Francelino', email='g@f.com')
        Customer.objects.create(first_name='Isabela', last_name='Loz', email='i@l.com')
        Customer.objects.create(first_name='Gleyci', last_name='Figueiredo', email='g@fi.com')
        Customer.objects.create(first_name='Amanda', last_name='Francelino', email='a@f.com')
        Customer.objects.create(first_name='Guilherme', last_name='Portugues', email='g@p.com')

    def test_search_2_letters(self):
        url = reverse('customer-search')
        data = {'search': 'gu'}
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
