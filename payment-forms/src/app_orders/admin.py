from django.contrib import admin

from app_orders.models import Item, Order, OrderItems


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'price',
        'currency'
    ]

    ordering = ('name',)


class OrderItemsInline(admin.StackedInline):
    model = OrderItems

    fields = ('item', 'quantity', 'total_amount',)
    readonly_fields = ('total_amount',)

    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'created_at',
        'total_amount',
    ]

    readonly_fields = (
        'total_amount',
    )
    filter_horizontal = ('order_items', )
    ordering = ('-created_at', )
    inlines = [OrderItemsInline]


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
