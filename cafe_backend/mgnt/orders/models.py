from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField
from django_fsm import transition
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import (
    DEFAULT_STATE, ORDER_STATE)


ORDER_STATE_CHOICES = (
    (ORDER_STATE.default, _('Requested')),
    (ORDER_STATE.canceled, _('Canceled')),
    (ORDER_STATE.delivered, _('Delivered')),
    (ORDER_STATE.archived, _('Archived')),
)


class Order(TimeStampedModel):
    class Meta:
        ordering = ('-created', )
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='orders', null=True, verbose_name=_('Customer'))
    state = FSMField(
        choices=ORDER_STATE_CHOICES, default=ORDER_STATE.default,
        verbose_name=_('State'))
    details = JSONField(
        default={'customers': {'male': 1, 'female': 0}},
        verbose_name=_('Details'))

    def to_json(self):
        return {
            "table": self.table.pk,
            "user": self.table.user.pk,
            "state": self.state,
            "items": [item.to_json() for item in self.order_items.all()]
        }

    def __str__(self):
        return "<%s (%d)|(%s)>" % (
            _('Order'), self.pk, self.state)

    @property
    def items(self):
        return self.order_items.exclude(state=ORDER_STATE.canceled)

    @property
    def pending_items(self):
        return self.order_items.filter(state=ORDER_STATE.default)

    @property
    def completed(self):
        return self.items.filter(state=ORDER_STATE.delivered)

    @property
    def progress(self):
        if len(self.items) > 0:
            return "%d / %d" % (len(self.completed), len(self.items))
        else:
            return "N / A"

    @property
    def is_delivered(self):
        return len(self.completed) == len(self.items)

    @property
    def total_sum(self):
        if len(self.order_items.all()) > 0:
            return self.items.values('price', 'amount').aggregate(
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
        source=(
            ORDER_STATE.default, ORDER_STATE.canceled, ORDER_STATE.delivered),
        target=ORDER_STATE.archived)
    def archive(self):
        self.details['customers'] = {
            'male': self.table.male,
            'female': self.table.female}


class OrderItem(TimeStampedModel):
    class Meta:
        ordering = ('-created', )
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items',
        verbose_name=_('Order'))
    dish = models.ForeignKey(
        'dishes.Dish', on_delete=models.CASCADE, related_name='order_items',
        verbose_name=_('Dish'))
    to_table = models.ForeignKey(
        'users.Table', on_delete=models.SET_NULL,
        related_name='received_order_items', null=True,
        verbose_name=_('Target Table'))
    price = models.FloatField(
        validators=[MinValueValidator(0)], verbose_name=('Price'))
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name=_('Amount'))
    discount_rate = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Discount Rate'))
    state = FSMField(
        choices=ORDER_STATE_CHOICES, default=ORDER_STATE.default,
        verbose_name=_('State'))

    @property
    def subtotal(self):
        return self.price * self.amount

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
            "id": self.pk,
            "order": self.order.pk,
            "dish": self.dish.pk,
            "to_table": self.to_table.pk,
            "price": self.price,
            "amount": self.amount,
            "state": self.state,
            "is_canceled": self.is_canceled,
            "is_delivered": self.is_delivered
        }

    def is_booking_order_item(self):
        return self.order.table != self.to_table
