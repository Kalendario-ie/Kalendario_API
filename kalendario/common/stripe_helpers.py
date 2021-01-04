import stripe
from django.conf import settings
from . import stripe_mock

stripe.api_key = getattr(settings, 'STRIPE_API_KEY', '')
stripe.api_version = getattr(settings, 'STRIPE_API_VERSION', '')
publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
price_id = getattr(settings, 'STRIPE_SUBSCRIPTION_PRICE_ID', '')
env = getattr(settings, 'ENVIRONMENT', '')


def create_account(**kwargs):
    if env == 'TEST':
        return stripe_mock.create_account_mock(**kwargs)
    account = stripe.Account.create(type='express', **kwargs)
    return account


def retrieve_account(sid):
    return stripe.Account.retrieve(sid)


def generate_account_link(account_id, refresh_url, return_url):
    if env == 'TEST':
        return 'mock-link'

    account_link = stripe.AccountLink.create(
        type='account_onboarding',
        account=account_id,
        refresh_url=refresh_url,
        return_url=return_url,
    )
    return account_link.url


def create_payment_intent(account, currency, amount, fee, metadata):
    return stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        transfer_data={'destination': account},
        application_fee_amount=fee,
        metadata=metadata
    )


def update_payment_intent(sid, amount, fee, metadata):
    return stripe.PaymentIntent.modify(
        sid,
        amount=amount,
        application_fee_amount=fee,
        metadata=metadata
    )


def create_customer(name, email, metadata=None):
    if env == 'TEST':
        return stripe_mock.create_customer_mock(name, email)

    return stripe.Customer.create(email=email, name=name, metadata=metadata)


def create_subscription(customer_id):
    if env == 'TEST':
        return stripe_mock.create_subscription_mock(customer_id)

    return stripe.Subscription.create(
        customer=customer_id,
        items=[
            {
                'price': price_id,
            },
        ],
        trial_period_days=30,
    )
