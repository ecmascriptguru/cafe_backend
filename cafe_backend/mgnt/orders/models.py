from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from django_fsm import FSMField
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import (
    DEFAULT_STATE, ORDER_STATE)


ORDER_STATE_CHOICES = (
    (ORDER_STATE.draft, 'Draft'),
    (ORDER_STATE.default, 'Requested'),
    (ORDER_STATE.in_progress, 'Processing'),
    (ORDER_STATE.canceled, 'Canceled'),
    (ORDER_STATE.delivered, 'Delivered'),
    (ORDER_STATE.archieved, 'Archived'),
)


class Order(TimeStampedModel):
    class Meta:
        ordering = ('-created', )

    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='orders', null=True)
    state = FSMField(choices=ORDER_STATE_CHOICES, default=ORDER_STATE.draft)

    @property
    def items(self):
        return self.order_items.filter(is_canceled=False)

    @property
    def completed(self):
        return self.items.filter(is_complete=True)

    @property
    def progress(self):
        if len(self.items) > 0:
            return "%d/%d" % (len(self.completed), len(self.items))
        else:
            return "N/A"

    @property
    def total_sum(self):
        if len(self.order_items.all()) > 0:
            return self.order_items.filter(
                is_canceled=False).values('price', 'amount').aggregate(
                    total_price=models.Sum(
                        F('price') * F("amount"),
                        output_field=models.FloatField()
                    )
                ).get('total_price', 0.0)
        else:
            return 0.0

    @classmethod
    def all(cls):
        return cls.objects.all().exclude(state__in=[
            ORDER_STATE.canceled, ORDER_STATE.archieved])


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
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)])
    discount_rate = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_canceled = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def save(self, **kwargs):
        if not self.to_table:
            self.to_table = self.order.table
        self.price = self.dish.price
        return super(OrderItem, self).save(**kwargs)
