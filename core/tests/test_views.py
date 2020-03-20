from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.models import User


class RegisterUserView(TestCase):

    def test_register_user_creates_user_and_person(self):
        """
        Registering a user should create a user as well as link this user to a person
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
        user = User.objects.last()
        self.assertEqual(user.email, data['email'])
        self.assertIsNotNone(user.person)
        self.assertTrue(user.has_perm('scheduling.add_company'))
