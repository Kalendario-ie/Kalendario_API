import stripe
from django.conf import settings
from stripe.error import SignatureVerificationError

stripe.api_key = getattr(settings, 'STRIPE_API_KEY', '')
stripe.api_version = getattr(settings, 'STRIPE_API_VERSION', '')
publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
price_id = getattr(settings, 'STRIPE_SUBSCRIPTION_PRICE_ID', '')
STRIPE_WEBHOOK_SECRET = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')


def create_account(company):
    account = stripe.Account.create(type='express',
                                    email=company.email,
                                    metadata={'company': company.id},
                                    capabilities={
                                        'card_payments': {'requested': True},
                                        'transfers': {'requested': True}
                                    }
                                    )
    return account


def retrieve_account(sid):
    return stripe.Account.retrieve(sid)


def generate_account_link(account_id, refresh_url, return_url):
    account_link = stripe.AccountLink.create(
        type='account_onboarding',
        account=account_id,
        refresh_url=refresh_url,
        return_url=return_url,
        collect='eventually_due'
    )
    return account_link.url


def create_payment_intent(request):
    account = request.owner.account

    return stripe.PaymentIntent.create(
        amount=request.total_int,
        currency=account.default_currency,
        transfer_data={'destination': account.stripe_id},
        application_fee_amount=request.fee_int,
        customer=request.user.billingusercustomer,
        metadata={'request_id': request.id}
    )


def update_payment_intent(intent):
    return stripe.PaymentIntent.modify(
        intent.stripe_id,
        amount=intent.request.total_int,
        application_fee_amount=intent.request.fee_int,
    )


def create_customer(instance):
    """
    :param instance: User or Customer
    :return: return a Stripe Customer Object based on the instance provided
    """
    metadata = {'class': instance.__class__, 'instance_id': instance.id}
    return stripe.Customer.create(email=instance.email, name=instance.name, metadata=metadata)


def create_subscription(customer_id):
    return stripe.Subscription.create(
        customer=customer_id,
        items=[
            {
                'price': price_id,
            },
        ],
        trial_period_days=30,
    )


def construct_event(payload, sig_header):
    return stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)