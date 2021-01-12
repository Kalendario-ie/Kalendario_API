from django.urls.exceptions import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from billing import models
from billing.stripe.helpers import mock
from core.models import User
from scheduling.models import Request
from util import test_util


class TestStripeViewSet(APITestCase):
    fixtures = ['companies.json', 'users.json']

    def detail_post_results(self, owner_id):
        detail_url = reverse('billing-account-detail', kwargs={'owner_id': owner_id})
        get_detail = self.client.get(detail_url, format='json')
        post = self.client.post(detail_url + 'connect/', format='json')
        return get_detail, post

    def test_list_url_does_not_exist(self):
        self.assertRaises(NoReverseMatch, reverse, 'billing-account-list')

    def test_anonymous_users_access(self):
        """
        Anonymous users should have no access
        """
        get_detail, post = self.detail_post_results(1)

        self.assertEqual(get_detail.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_access_own_company(self):
        """
        A user should not be able to access the view when trying to see a different company
        """
        user = User.objects.get(pk=1)

        self.client.force_authenticate(user)
        get_detail, post = self.detail_post_results(1)

        self.assertEqual(get_detail.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_rights_access_own_company(self):
        """
        A user that has read/write rights to StripeConnectedAccount should be able to access the views
        """

        user = User.objects.get(pk=1)
        user.add_permissions(models.Account)

        self.client.force_authenticate(user)
        get_detail, post = self.detail_post_results(1)

        self.assertEqual(get_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(post.status_code, status.HTTP_200_OK)

    def test_user_access_to_different_company(self):
        """
        A user should not be able to access the view when trying to see a different company
        """
        user = User.objects.get(pk=1)
        user.add_permissions(models.Account)

        self.client.force_authenticate(user)
        get_detail, post = self.detail_post_results(2)

        self.assertEqual(get_detail.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post.status_code, status.HTTP_404_NOT_FOUND)


class TestPaymentIntentView(APITestCase):
    fixtures = ['companies.json', 'users.json', 'services.json', 'timeframes.json', 'shifts.json',
                'schedules.json', 'people.json', 'employees.json']

    def test_intent_created(self):
        request = Request.objects.get_current(1, 3)
        user = User.objects.get(pk=3)
        request.add_appointment(user, service_id=1, employee_id=1, owner_id=1,
                                start=test_util.next_wednesday().replace(hour=9, minute=00))

        self.client.force_authenticate(user)
        intent_result = self.client.post(reverse('stripe-payment'), data={'request_id': request.id})

        self.assertEqual(intent_result.status_code, status.HTTP_200_OK)


class TestAccountHookView(APITestCase):
    fixtures = ['companies.json', 'users.json', 'services.json', 'timeframes.json', 'shifts.json',
                'schedules.json', 'people.json', 'employees.json']

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.get_account_updated_event)
    def test_invalid_event(self, mock_func):
        result = self.client.post(reverse('account-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.raise_value_error)
    def test_construct_event_throwing_error(self, mock_func):
        result = self.client.post(reverse('account-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.get_intent_succeeded_event)
    def test_valid_event_without_database_object(self, mock_func):
        intent_result = self.client.post(reverse('account-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(intent_result.status_code, status.HTTP_404_NOT_FOUND)

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.get_intent_succeeded_event)
    @patch('billing.stripe.helpers.create_payment_intent', side_effect=mock.get_payment_intent)
    def test_valid_event_database_link(self, mock_construct, mock_create):
        request = Request.objects.get_current(1, 3)
        intent, created = models.PaymentIntent.objects.get_or_create(request.id)

        result = self.client.post(reverse('account-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_construct.called)
        self.assertEqual(mock_construct.call_count, 1)
        self.assertTrue(mock_create.called)
        self.assertEqual(mock_create.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_200_OK)


class TestConnectedAccountHookView(APITestCase):
    fixtures = ['companies.json', 'users.json', 'services.json', 'timeframes.json', 'shifts.json',
                'schedules.json', 'people.json', 'employees.json']

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.get_intent_succeeded_event)
    def test_invalid_event(self, mock_func):
        result = self.client.post(reverse('connected-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.raise_value_error)
    def test_construct_event_throwing_error(self, mock_func):
        result = self.client.post(reverse('connected-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.get_account_updated_event)
    def test_valid_event_without_database_object(self, mock_func):
        result = self.client.post(reverse('connected-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    @patch('billing.stripe.helpers.construct_event', side_effect=mock.get_account_updated_event)
    def test_valid_event_database_link(self, mock_construct):
        event_account = mock.get_account()
        account = models.Account.objects.first()
        account.stripe_id = event_account.id
        account.save()

        result = self.client.post(reverse('connected-webhook'), data={}, HTTP_STRIPE_SIGNATURE='test')

        self.assertTrue(mock_construct.called)
        self.assertEqual(mock_construct.call_count, 1)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
