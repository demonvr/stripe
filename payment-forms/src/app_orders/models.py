from django.db import models
from django.db.models import enums, Sum
from django.core.exceptions import ValidationError

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
    total_amount = models.DecimalField(blank=True,
                                       null=True,
                                       max_digits=15,
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

    def save(self, *args, **kwargs):
        if self.pk:
            order_items = OrderItems.objects.filter(
                order_id=self.id
            )
            # пересчет общей суммы заказа
            self.total_amount = order_items.aggregate(
                total=Sum('total_amount')
            )['total']

            # проверка на одинаковые валюты
            if len(order_items.distinct('item__currency')) > 1:
                raise ValidationError("Currencies must be the same!")
        super().save(*args, **kwargs)


class OrderItems(TimeStampedModelMixin):
    """Товары в заказе"""
    total_amount = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       verbose_name='общая стоимость товара')
    quantity = models.PositiveIntegerField(verbose_name='количество товара')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказе'

    def __str__(self):
        return self.item.name

    def recalculate_and_save_total_count(self, order: Order):
        order.total_amount = OrderItems.objects.filter(
            order_id=self.order.id
        ).aggregate(
            total=Sum('total_amount')
        )['total']
        order.save()

    def save(self, *args, **kwargs):
        self.total_amount = self.item.price * self.quantity
        super().save(*args, **kwargs)
        self.recalculate_and_save_total_count(
            Order.objects.get(id=self.order.id)
        )

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.recalculate_and_save_total_count(
            Order.objects.get(id=self.order.id)
        )
