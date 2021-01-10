from unittest.mock import patch
from django.test import TestCase
from billing import models as billing_models
from billing.stripe.helpers.mock import create_customer, create_subscription, create_customer_fail
from core.models import User
from scheduling.models import Company


class TestModels(TestCase):

    fixtures = ['companies.json', 'users.json']

    @patch('billing.stripe.helpers.create_customer', side_effect=create_customer)
    @patch('billing.stripe.helpers.create_subscription', side_effect=create_subscription)
    def test_create_company_creates_billing_customer(self, subscription_mock, customer_mock):
        company = Company()
        company.save()

        self.assertTrue(customer_mock.called)
        self.assertEqual(customer_mock.call_count, 1)

        self.assertTrue(subscription_mock.called)
        self.assertEqual(subscription_mock.call_count, 1)

        billing_customer = billing_models.BillingCompanyCustomer.objects.filter(company=company).first()
        self.assertIsNotNone(billing_customer.stripe_id)

        subscriptions = billing_models.Subscription.objects.filter(customer=billing_customer)
        subscription = subscriptions.first()

        self.assertEqual(subscriptions.count(), 1)
        self.assertTrue(subscription.is_trial)

    @patch('billing.stripe.helpers.create_customer', side_effect=create_customer_fail)
    @patch('billing.stripe.helpers.create_subscription', side_effect=create_subscription)
    def test_create_company_creates_billing_customer_error(self, subscription_mock, customer_mock):
        """
        when an error occurs in stripe the system should not create billing or subscription
        """
        company = Company()
        company.save()

        self.assertTrue(customer_mock.called)

        self.assertFalse(subscription_mock.called)

        billing_customer = billing_models.BillingCompanyCustomer.objects.filter(company=company).first()
        self.assertIsNone(billing_customer)

        subscriptions = billing_models.Subscription.objects.filter(customer=billing_customer)
        subscription = subscriptions.first()

        self.assertEqual(subscriptions.count(), 0)

    @patch('billing.stripe.helpers.create_customer', side_effect=create_customer)
    @patch('billing.stripe.helpers.create_subscription', side_effect=create_subscription)
    def test_create_user_creates_billing_customer(self, subscription_mock, customer_mock):
        user = User(email='billing_user@user.com')
        user.save()

        self.assertTrue(customer_mock.called)
        self.assertEqual(customer_mock.call_count, 1)

        self.assertFalse(subscription_mock.called)

        billing_customer = billing_models.BillingUserCustomer.objects.filter(user=user).first()
        self.assertIsNotNone(billing_customer.stripe_id)

        subscriptions = billing_models.Subscription.objects.filter(customer=billing_customer)

        self.assertEqual(subscriptions.count(), 0)
