import stripe
from django.conf import settings
from urllib.parse import urljoin

from app_orders.models import Item


class StripeAPI:
    @staticmethod
    def set_stripe(currency: str):
        stripe.api_key = settings.STRIPE_API_KEY[currency]['secret']

    @staticmethod
    def create_checkout_session(currency: str,
                                line_items: list[dict]):
        StripeAPI.set_stripe(currency)
        session = stripe.checkout.Session.create(
            line_items=line_items,
            currency=currency,
            mode='payment',
            success_url=urljoin(settings.FRONTEND_BASE_URL,
                                settings.STATIC_URL + 'success.html'),
            cancel_url=urljoin(settings.FRONTEND_BASE_URL,
                               settings.STATIC_URL + 'cancel.html'),
        )
        return session
