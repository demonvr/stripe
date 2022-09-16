from django.db import models
from django.db.models import enums


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
