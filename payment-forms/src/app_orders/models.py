from django.db import models
from django.db.models import enums

from sdk.models import TimeStampedModelMixin


class Item(models.Model):
    """Товар"""

    class Currency(enums.TextChoices):
        """Валюта"""
        RUB = "rub", "Russian Ruble"
        USD = "usd", "US Dollar"

    name = models.CharField(max_length=50
                            ,
                            verbose_name='название товара')
    description = models.CharField(max_length=200,
                                   verbose_name='описание товара')
    price = models.DecimalField(max_digits=15,
                                decimal_places=2,
                                verbose_name='стоимость товара')
    currency = models.CharField(max_length=3,
                                choices=Currency.choices,
                                default=Currency.RUB,
                                verbose_name='валюта товара')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class Order(TimeStampedModelMixin):
    """Заказ"""
    total_amount = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       verbose_name='общая сумма заказа')
    order_items = models.ManyToManyField(Item,
                                         related_name='orders',
                                         through='OrderItems')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Заказ №' + str(self.id)


class OrderItems(TimeStampedModelMixin):
    """Товары в заказе"""
    price = models.DecimalField(max_digits=15,
                                decimal_places=2,
                                verbose_name='стоимость товара')
    quantity = models.PositiveIntegerField(verbose_name='количество товара')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказе'
