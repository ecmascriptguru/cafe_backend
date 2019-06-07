from datetime import timedelta, datetime
from django.db import models
from django.db.models.functions import Cast, TruncDate
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db.models import (
    F, IntegerField, Sum, ExpressionWrapper, Count)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import make_aware
from django.apps import apps
from django_fsm import FSMField
from django_fsm import transition
from model_utils.models import TimeStampedModel
from cafe_backend.core.constants.states import (
    DEFAULT_STATE, ORDER_STATE)
from cafe_backend.core.constants.types import PAYMENT_METHOD


ORDER_STATE_CHOICES = (
    (ORDER_STATE.default, _('Requested')),
    (ORDER_STATE.delivered, _('Delivered')),
    (ORDER_STATE.archived, _('Archived')),
)


PAYMENT_METHOD_CHOICES = (
    (PAYMENT_METHOD.cash, _('Cash')),
    (PAYMENT_METHOD.wechat, _('WeChat')),
    (PAYMENT_METHOD.alipay, _('AliPay'))
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
    payment_method = FSMField(
        choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD.wechat,
        verbose_name=_('Payment Method'))
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

    @classmethod
    def get_report(cls, start_date, end_date, tables=[]):
        if isinstance(start_date, str):
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d') +\
                timedelta(days=1)
            end_date = make_aware(end_date)

        Table = apps.get_model('users', 'Table')
        if len(tables) == 0:
            tables = [table.pk for table in Table.objects.all()]

        orders = cls.objects.filter(
            created__gte=start_date, created__lt=end_date,
            table__in=tables).all()

        customers = Order.objects.annotate(
            male=Cast(
                KeyTextTransform(
                    'male', KeyTextTransform(
                        'customers', 'details')),
                    IntegerField()),
            female=Cast(
                KeyTextTransform(
                    'female', KeyTextTransform(
                        'customers', 'details')),
                    IntegerField())).values('male', 'female').aggregate(
                        total_male=Sum('male'),
                        total_female=Sum('female'))
        OrderItem = apps.get_model('orders', 'OrderItem')
        items = OrderItem.objects.filter(
            order__in=orders).all().exclude(
                state=ORDER_STATE.canceled)
        return {
            'orders': {'count': len(orders)},
            'customers': {
                'count': customers['total_male'] + customers['total_female']
            },
            'sales': {
                'items': len(items),
                'earning': items.aggregate(
                    total=ExpressionWrapper(
                        Sum(F('price') * F('amount')),
                        output_field=models.FloatField()))['total']},
            # 'chart': {
            #     'earning_by_date': items.annotate(
            #         date=TruncDate('created')).values('date').aggregate(
            #             sub_total=Sum(
            #                 F('price') * F('amount')),
            #             output_field=models.FloatField())
            # }
        }


class OrderItem(TimeStampedModel):
    ORDER_ITEM_STATE_CHOICES = (
        (ORDER_STATE.default, _('Requested')),
        (ORDER_STATE.canceled, _('Canceled')),
        (ORDER_STATE.delivered, _('Delivered')),
    )

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
        choices=ORDER_ITEM_STATE_CHOICES, default=ORDER_STATE.default,
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
            "dish_img": self.dish.img.file.url,
            "to_table": self.to_table.pk,
            "to_table_name": self.to_table.name,
            "price": self.price,
            "amount": self.amount,
            "state": self.state,
            "is_canceled": self.is_canceled,
            "is_delivered": self.is_delivered
        }

    def is_booking_order_item(self):
        return self.order.table != self.to_table
