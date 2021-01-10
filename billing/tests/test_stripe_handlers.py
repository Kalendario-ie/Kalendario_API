import json
from django.test import TestCase
from billing import models
from billing.stripe.hook_handler import StripeHookHandler
from types import SimpleNamespace
from scheduling.models import Request, Service, Employee
from core.models import User
from util import test_util


def get_account_updated_event():
    file = open('billing/fixtures/stripe_event_account_updated.json')
    return json.load(file, object_hook=lambda d: SimpleNamespace(**d))


def get_intent_succeeded_event():
    file = open('billing/fixtures/payment_intent_succeeded.json')
    return json.load(file, object_hook=lambda d: SimpleNamespace(**d))


class TestStripeWebhookHandler(TestCase):

    fixtures = ['companies.json', 'users.json', 'services.json', 'timeframes.json', 'shifts.json',
                'schedules.json', 'people.json', 'employees.json']

    def test_account_updated(self):
        stripe_account = models.Account.objects.first()
        event = get_account_updated_event()
        event_account = event.data.object
        requirements = event_account.requirements
        event_account.id = stripe_account.stripe_id

        handler_result = StripeHookHandler(event).handle()
        updated_account = models.Account.objects.get(pk=stripe_account.id)

        self.assertEqual(updated_account.currently_due, requirements.currently_due)
        self.assertEqual(updated_account.requirements_disabled_reason, requirements.disabled_reason)
        self.assertTrue(handler_result)

    def test_payment_intent_success(self):
        request = Request.objects.get_current(1, 3)
        user = User.objects.get(pk=3)
        request.add_appointment(user, service_id=1, employee_id=1, owner_id=1,
                                start=test_util.next_wednesday().replace(hour=9, minute=00))
        event = get_intent_succeeded_event()
        intent, created = models.PaymentIntent.objects.get_or_create(request.id)
        intent.stripe_id = event.data.object.id
        intent.save()

        handler_result = StripeHookHandler(event).handle()

        self.assertTrue(handler_result)
