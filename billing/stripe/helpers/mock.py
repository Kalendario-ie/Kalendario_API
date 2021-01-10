import uuid
from collections import namedtuple

from stripe.error import InvalidRequestError


class StripeMock:
    id = None

    @property
    def stripe_id(self):
        return self.id


class StripeCustomerMock(StripeMock):
    """
    {
        "id": "cus_IgtALbxQdPP53S",
        "object": "customer",
        "address": address,
        "balance": 0,
        "created": 1609675705,
        "currency": "eur",
        "default_source": None,
        "delinquent": False,
        "description": None,
        "discount": None,
        "email": email,
        "invoice_prefix": "09DD1E7",
        "invoice_settings": {
            "custom_fields": None,
            "default_payment_method": None,
            "footer": None
        },
        "livemode": False,
        "metadata": {'company_id': company_id},
        "name": name,
        "phone": None,
        "preferred_locales": [],
        "shipping": None,
        "tax_exempt": "none"
    }
    """

    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.email = email,
        self.name = name


class StripeSubscriptionMock(StripeMock):
    """
        {
      "id": "sub_IgtAsyoKV8ua4z",
      "object": "subscription",
      "application_fee_percent": null,
      "billing_cycle_anchor": 1609675711,
      "billing_thresholds": null,
      "cancel_at": null,
      "cancel_at_period_end": false,
      "canceled_at": null,
      "collection_method": "charge_automatically",
      "created": 1609675711,
      "current_period_end": 1612354111,
      "current_period_start": 1609675711,
      "customer": "cus_HuAgd8KV1uRghr",
      "days_until_due": null,
      "default_payment_method": null,
      "default_source": null,
      "default_tax_rates": [],
      "discount": null,
      "ended_at": null,
      "items": {
        "object": "list",
        "data": [
          {
            "id": "si_IgtAApsJSimqlv",
            "object": "subscription_item",
            "billing_thresholds": null,
            "created": 1609675711,
            "metadata": {},
            "price": {
              "id": "price_1I5VGlAe2CG5hLhg1L6zJsQu",
              "object": "price",
              "active": true,
              "billing_scheme": "per_unit",
              "created": 1609675271,
              "currency": "eur",
              "livemode": false,
              "lookup_key": null,
              "metadata": {},
              "nickname": null,
              "product": "prod_Igt2Z994K1xTdT",
              "recurring": {
                "aggregate_usage": null,
                "interval": "month",
                "interval_count": 1,
                "usage_type": "licensed"
              },
              "tiers_mode": null,
              "transform_quantity": null,
              "type": "recurring",
              "unit_amount": 3000,
              "unit_amount_decimal": "3000"
            },
            "quantity": 1,
            "subscription": "sub_IgtAsyoKV8ua4z",
            "tax_rates": []
          }
        ],
        "has_more": false,
        "url": "/v1/subscription_items?subscription=sub_IgtAsyoKV8ua4z"
      },
      "latest_invoice": null,
      "livemode": false,
      "metadata": {},
      "next_pending_invoice_item_invoice": null,
      "pause_collection": null,
      "pending_invoice_item_interval": null,
      "pending_setup_intent": null,
      "pending_update": null,
      "schedule": null,
      "start_date": 1609675711,
      "status": "active",
      "transfer_data": null,
      "trial_end": null,
      "trial_start": null
    }
    """

    def __init__(self, customer_id, complete=True):
        self.id = str(uuid.uuid4())
        self.customer = customer_id
        self.start_date = 1609675711
        self.current_period_start = 1609675711
        self.current_period_end = 1612354111
        self.status = 'active' if complete else 'incomplete'


class Requirements:
    def __init__(self, currently_due):
        self.currently_due = currently_due
        self.disabled_reason = 'none'


class StripeConnectedAccountMock(StripeMock):

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.details_submitted = False
        self.charges_enabled = False
        self.payouts_enabled = False
        self.default_currency = 'EUR'
        self.requirements = Requirements([])


def create_customer(instance):
    return StripeCustomerMock(instance.name, instance.email)


def create_customer_fail(instance):
    raise InvalidRequestError('invalid request', 'param')


def create_subscription(customer_id):
    return StripeSubscriptionMock(customer_id)


def create_account(company):
    return StripeConnectedAccountMock()


StripePaymentIntent = namedtuple('MyStruct', 'stripe_id  client_secret amount application_fee_amount')


def create_payment_intent(request):
    return StripePaymentIntent(stripe_id='test_id', client_secret='', amount=request.total_int,
                               application_fee_amount=request.fee_int)


def generate_account_link(account_id, refresh_url, return_url):
    return 'account_link.url_'
