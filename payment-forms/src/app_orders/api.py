from app_orders.models import Order


class OrdersAPI:
    @staticmethod
    def update_order_status(order_id: int, status: Order.Status):
        """Обновление статуса заказа"""
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save(update_fields=['status', 'updated_at'])
