from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from django_fsm import FSMField
from django_fsm import transition
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import (
    DEFAULT_STATE, ORDER_STATE)


ORDER_STATE_CHOICES = (
    (ORDER_STATE.default, 'Requested'),
    (ORDER_STATE.canceled, 'Canceled'),
    (ORDER_STATE.delivered, 'Delivered'),
    (ORDER_STATE.archived, 'Archived'),
)


class Order(TimeStampedModel):
    class Meta:
        ordering = ('-created', )

    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='orders', null=True)
    state = FSMField(choices=ORDER_STATE_CHOICES, default=ORDER_STATE.default)

    def to_json(self):
        return {
            "table": self.table.pk,
            "user": self.table.user.pk,
            "state": self.state,
            "items": [item.to_json() for item in self.order_items.all()]
        }

    @property
    def items(self):
        return self.order_items.filter(is_canceled=False)

    @property
    def completed(self):
        return self.items.filter(is_delivered=True)

    @property
    def progress(self):
        if len(self.items) > 0:
            return "%d/%d" % (len(self.completed), len(self.items))
        else:
            return "N/A"

    @property
    def is_delivered(self):
        return len(self.completed) == len(self.items)

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
            ORDER_STATE.canceled, ORDER_STATE.archived])

    @transition(
        field='state',
        source=ORDER_STATE.default, target=ORDER_STATE.canceled)
    def cancel(self):
        pass

    @transition(
        field='state',
        source=ORDER_STATE.default, target=ORDER_STATE.delivered)
    def deliver(self):
        pass

    @transition(
        field='state',
        source=ORDER_STATE.delivered, target=ORDER_STATE.archived)
    def archive(self):
        pass


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
    state = FSMField(
        choices=ORDER_STATE_CHOICES, default=ORDER_STATE.default)

    @property
    def is_canceled(self):
        return self.state == ORDER_STATE.canceled

    @property
    def is_delivered(self):
        return self.state == ORDER_STATE.delivered

    def save(self, **kwargs):
        if not self.to_table:
            self.to_table = self.order.table
        self.price = self.dish.price
        return super(OrderItem, self).save(**kwargs)

    def to_json(self):
        return {
            "order": self.order.pk,
            "dish": self.dish.pk,
            "to_table": self.to_table.pk,
            "price": self.price,
            "amount": self.amount,
            "state": self.state,
            "is_canceled": self.is_canceled,
            "is_delivered": self.is_delivered
        }
