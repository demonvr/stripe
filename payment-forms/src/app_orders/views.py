from django.shortcuts import render
from django.conf import settings
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from app_orders.builders import build_checkout
from app_orders.models import Item, Order, OrderItems
from app_orders.serializers import SessionResponseSerializer, ItemSerializer, OrderSerializer
from app_orders.stripe import StripeAPI


class ItemCheckoutView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @extend_schema(
        summary="Получение session_id для товара",
        description="Получение session_id для товара",
        responses={200: SessionResponseSerializer},
    )
    def get(self, request, pk):
        item = self.get_object()
        line_items = build_checkout([item])
        session = StripeAPI.create_checkout_session(
            item.currency,
            line_items
        )
        return Response({"session_id": session.id})


class ItemView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @extend_schema(
        summary="Получение страницы продажи товара по номеру товара",
        description="Получение html страницы продажи по номеру товара",
    )
    def get(self, request, *args, **kwargs):
        item = self.get_object()
        stripe_publish_key = settings.STRIPE_API_KEY[item.currency]['publish']
        return render(
            request,
            'buy_item.html',
            {'item': self.get_object(),
             'stripe_publish_key': stripe_publish_key}
        )


class OrderCheckoutView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @extend_schema(
        summary="Получение session_id для заказа",
        description="Получение session_id для заказа",
        responses={200: SessionResponseSerializer},
    )
    def get(self, request, pk):
        order = self.get_object()
        order_items = OrderItems.objects.filter(order=order).all()
        items = [order_item.item for order_item in order_items]
        line_items = build_checkout(items)
        session = StripeAPI.create_checkout_session(
            items[0].currency,
            line_items
        )
        return Response({"session_id": session.id})


class OrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @extend_schema(
        summary="Получение страницы продажи товара по номеру заказа",
        description="Получение html страницы продажи товара по номеру заказа",
    )
    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order_items = OrderItems.objects.filter(order=order).all()
        items = [order_item.item for order_item in order_items]
        stripe_publish_key = settings.STRIPE_API_KEY[
            items[0].currency
        ]['publish']
        return render(
            request,
            'buy_items.html',
            {'items': items,
             'order': order,
             'stripe_publish_key': stripe_publish_key}
        )