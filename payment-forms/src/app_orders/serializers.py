from rest_framework import serializers

from app_orders.models import Item


class SessionResponseSerializer(serializers.Serializer):
    session_id = serializers.CharField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
