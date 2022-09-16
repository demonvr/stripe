from django.contrib import admin

from app_orders.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'price',
        'currency'
    ]

    ordering = ('name',)


admin.site.register(Item, ItemAdmin)
