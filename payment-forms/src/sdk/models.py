from django.db import models
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)


class TimeStampedModelMixin(models.Model):
    """Абстрактная модель, добавляющая дату создания и дату изменения."""

    created_at = CreationDateTimeField(verbose_name="дата создания")
    updated_at = ModificationDateTimeField(verbose_name="дата изменения")

    class Meta:
        abstract = True

