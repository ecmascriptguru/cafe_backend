from django.db import models
from model_utils.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"
