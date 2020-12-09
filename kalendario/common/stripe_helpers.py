import stripe
from django.conf import settings

stripe.api_key = getattr(settings, 'STRIPE_API_KEY', '')
stripe.api_version = getattr(settings, 'STRIPE_API_VERSION', '')
publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')


def create_account():
    account = stripe.Account.create(type='express')
    return account


def retrieve_account(sid):
    return stripe.Account.retrieve(sid)


def generate_account_link(account_id, refresh_url, return_url):
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
