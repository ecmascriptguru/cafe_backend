from django.db import models
from model_utils.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"


class Dish(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='dishes',
        null=True)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
