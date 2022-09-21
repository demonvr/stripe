import stripe
from django.conf import settings
from urllib.parse import urljoin
from django.urls import reverse

from app_orders.api import OrdersAPI
from app_orders.models import Order


class StripeAPI:
    @staticmethod
    def set_stripe(currency: str):
        stripe.api_key = settings.STRIPE_API_KEY[currency]['secret']

    @staticmethod
    def create_checkout_session(currency: str,
                                line_items: list[dict],
                                order_id: str = ''):
        StripeAPI.set_stripe(currency)
        session = stripe.checkout.Session.create(
            line_items=line_items,
            currency=currency,
            mode='payment',
            metadata={'order_id': order_id},
            payment_intent_data={'metadata': {'order_id': order_id}},
            success_url=urljoin(settings.FRONTEND_BASE_URL,
                                reverse('api:app_orders:success')),
            cancel_url=urljoin(settings.FRONTEND_BASE_URL,
                               reverse('api:app_orders:cancel')),
        )
        return session

    @staticmethod
    def construct_event(payload, sig_header):
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return event

    @staticmethod
    def handle_event(event):
        order_id = event.data.object.metadata['order_id']
        if event.type == 'checkout.session.completed':
            if order_id:
                OrdersAPI.update_order_status(order_id, Order.Status.COMPLETED)
        elif event.type == 'charge.failed':
            if order_id:
                OrdersAPI.update_order_status(order_id, Order.Status.FAILED)
