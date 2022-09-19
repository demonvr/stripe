from django.contrib import admin

from app_orders.models import Item, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'price',
        'currency'
    ]

    ordering = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'total_amount',
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
