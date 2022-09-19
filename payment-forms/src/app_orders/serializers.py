from rest_framework import serializers

from app_orders.models import Item, Order


class SessionResponseSerializer(serializers.Serializer):
    session_id = serializers.CharField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
