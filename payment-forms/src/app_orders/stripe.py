import stripe
from django.conf import settings
from urllib.parse import urljoin

stripe.api_key = settings.STRIPE_API_KEY


class StripeAPI:
    @staticmethod
    def create_checkout_session(line_items: list[dict]):
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=urljoin(settings.FRONTEND_BASE_URL,
                                settings.STATIC_URL + 'success.html'),
            cancel_url=urljoin(settings.FRONTEND_BASE_URL,
                               settings.STATIC_URL + 'cancel.html'),
        )
        return session
