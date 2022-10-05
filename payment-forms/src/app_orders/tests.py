from django.test import TestCase, Client
from django import test

from app_orders.models import Order, Item, OrderItems
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status

class OrdersTests(TestCase):
    def setUp(self) -> None:
        test.TestCase = ''
        self.item1 = Item.objects.create(name='notebook1_usd',
                                         price=1025,
                                         description='notebook1_usd',
                                         currency=Item.Currency.USD)
        self.item2 = Item.objects.create(name='notebook2_usd',
                                         description='notebook2_usd',
                                         price=1000,
                                         currency=Item.Currency.USD)
        self.order1 = Order.objects.create()
        self.orderitems1 = OrderItems.objects.create(total_amount=2050,
                                                     quantity=2,
                                                     item=self.item1,
                                                     order=self.order1)
        self.orderitems2 = OrderItems.objects.create(total_amount=1000,
                                                     quantity=1,
                                                     item=self.item2,
                                                     order=self.order1)
        self.order1.refresh_from_db()

    def test_recalculate_and_save_total_count(self):
        self.assertEqual(self.order1.total_amount, 3050)
        self.orderitems3 = OrderItems.objects.create(total_amount=1000,
                                                     quantity=1,
                                                     item=self.item2,
                                                     order=self.order1)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.total_amount, 4050)
        self.orderitems3.delete()
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.total_amount, 3050)

    def test_difference_currency(self):
        item3 = Item.objects.create(name='notebook3_ru',
                                    description='notebook3_ru',
                                    price=100000,
                                    currency=Item.Currency.RUB)
        with self.assertRaisesMessage(ValidationError, "Currencies must be the same!"):
            OrderItems.objects.create(total_amount=100000,
                                      quantity=1,
                                      item=item3,
                                      order=self.order1)

    def test_success_cancel_url(self):
        client = Client()
        response = client.get(reverse("api:app_orders:success"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(reverse("api:app_orders:cancel"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)