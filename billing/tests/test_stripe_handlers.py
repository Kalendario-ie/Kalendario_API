import json
from django.test import TestCase
from billing import models, stripe_hook_handlers
from types import SimpleNamespace


def get_account_updated_event():
    event_account_updated_file = open('billing/fixtures/stripe_event_account_updated.json')
    return json.load(event_account_updated_file, object_hook=lambda d: SimpleNamespace(**d))


class TestStripeWebhook(TestCase):

    fixtures = ['companies.json', 'users.json']

    def test_account_updated_handler(self):
        stripe_account = models.Account.objects.first()
        event = get_account_updated_event()
        event_account = event.data.object
        requirements = event_account.requirements
        event_account.id = stripe_account.stripe_id

        stripe_hook_handlers.account_updated(event)
        updated_account = models.Account.objects.get(pk=stripe_account.id)

        self.assertEqual(updated_account.currently_due, requirements.currently_due)
        self.assertEqual(updated_account.requirements_disabled_reason, requirements.disabled_reason)

