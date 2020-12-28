from django.urls import reverse
from django.core import mail
from rest_framework import status
from .generics import ViewTestCase
from core import models
import re


def company_a_user():
    user = models.User.objects.create(email='user@email.com')
    user.set_password('UserPass')
    user.save()
    user.enable_company_editing(1)
    return user


class RegisterUserView(ViewTestCase):

    def register_user(self, data=None):
        data = data or {
            'first_name': 'Finn',
            'last_name': 'TheHuman',
            'email': 'Finn.TheHuman@adventuretime.com',
            'password1': 'Abcde1234!',
            'password2': 'Abcde1234!'
        }
        url = reverse('rest_register')
        return self.client.post(url, data, format='json'), data

    def test_register_user_creates_user(self):
        """
        Registering a user should create a user
        The newly created user shouldn't be linked to any customers
        """
        register_response, data = self.register_user()
        user = models.User.objects.last()
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.has_perm('scheduling.add_company'))
        self.assertEqual(user.customer_set.all().count(), 0)

    def test_verify_email(self):
        """
        After a user is verified
        """
        register_response, data = self.register_user()

        # Get token from email
        token_regex = r"/account-confirm-email/([A-Za-z0-9:\-_]+)\/"
        email_content = mail.outbox[0].body
        match = re.search(token_regex, email_content)
        self.assertIsNotNone(match.groups())
        token = match.group(1)

        # Verify
        response = self.client.post(reverse('rest_verify_email'), {'key': token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email=data['email'])
        self.assertTrue(user.verified)
        self.assertEqual(user.customer_set.all().count(), 2)


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