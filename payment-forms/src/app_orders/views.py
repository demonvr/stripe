from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from app_orders.builders import build_product_data, build_price_data, build_line_items
from app_orders.models import Item
from app_orders.serializers import SessionResponseSerializer, ItemSerializer
from app_orders.stripe import StripeAPI


class ItemCheckoutView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @extend_schema(
        summary="Получение session_id",
        description="Получение session_id",
        responses={200: SessionResponseSerializer},
    )
    def get(self, request, pk):
        item = self.get_object()
        price_data = build_price_data(item,
                                      build_product_data(item))
        line_items = build_line_items(price_data)
        session = StripeAPI.create_checkout_session([line_items.dict()])

        return Response({"session_id": session.id})


class ItemView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @extend_schema(
        summary="Получение страницы продажи товара",
        description="Получение html страницы продажи товара",
        responses={200: SessionResponseSerializer},
    )
    def get(self, request, *args, **kwargs):
        return render(request,
                      'buy_item.html',
                      {'item': self.get_object()})
