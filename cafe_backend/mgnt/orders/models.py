from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel):
    class Meta:
        ordering = ('-created', )

    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='orders', null=True)
    is_complete = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)


class OrderItem(TimeStampedModel):
    class Meta:
        ordering = ('-created', )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(
        'dishes.Dish', on_delete=models.CASCADE, related_name='order_items')
    to_table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='received_order_items', null=True)
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)])
    discount_rate = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_canceled = models.BooleanField(default=False)
