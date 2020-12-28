from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .generics import ViewTestCase
from core import models


class RegisterUserView(TestCase):

    def test_register_user_creates_user(self):
        """
        Registering a user should create a user
        """
        data = {
            'first_name': 'gustavo',
            'last_name': 'francelino',
            'email': 'gustavo.francelino@testingusers.com',
            'password1': 'Abcde1234!',
            'password2': 'Abcde1234!'
        }
        url = reverse('rest_register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.last()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.has_perm('scheduling.add_company'))


def company_a_user():
    user = models.User.objects.create(email='user@email.com')
    user.set_password('UserPass')
    user.save()
    user.enable_company_editing(1)
    return user


class GroupViewTest(ViewTestCase):

    def setUp(self):
        self.list_url = reverse('group-list')
        self.company_a_user = company_a_user()

    def detail_url(self, id):
        return f'{self.list_url}{id}/'

    def test_create(self):
        data = {'name': 'test', 'permissions': []}

        self.client.force_authenticate(user=self.company_a_user)
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        data = {'name': 'test', 'permissions': []}

        self.client.force_authenticate(user=self.company_a_user)
        response = self.client.patch(self.detail_url(1), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)