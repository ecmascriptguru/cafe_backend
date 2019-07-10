import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from ...mgnt.orders.models import Order, ORDER_STATE


class CustomerTable(tables.Table):
    number = tables.Column(
        empty_values=(), verbose_name='#', orderable=False)
    male = tables.Column(
        empty_values=(), verbose_name=_('Male'))
    female = tables.Column(
        empty_values=(), verbose_name=_('Female'))
    customers = tables.Column(
        empty_values=(), verbose_name=_('Customers'))
    started = tables.Column(
        empty_values=(), verbose_name=_('Order Creation Time'))
    ended = tables.Column(
        empty_values=(), verbose_name=_('Order Checkout Time'))

    class Meta:
        model = Order
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'table', 'male', 'female', 'customers', 'started', 'ended',)
        sequence = ('number', 'table', )

    def __init__(self, *args, **kwargs):
        super(CustomerTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_male(self, record):
        return record.details.get('customers', {}).get('male', 0)

    def render_female(self, record):
        return record.details.get('customers', {}).get('female', 0)

    def render_started(self, record):
        return record.created

    def render_ended(self, record):
        return record.checkout_at

    def render_customers(self, record):
        return record.details.get('customers', {}).get('male', 0)\
            + record.details.get('customers', {}).get('female', 0)

    def render_actions(self, record):
        return render_to_string(
            self.actions_template, context={'record': record})


class OrderTable(tables.Table):
    number = tables.Column(
        empty_values=(), verbose_name='#', orderable=False)
    total = tables.Column(
        empty_values=(), verbose_name=_('Total Price'))
    free = tables.Column(
        empty_values=(), verbose_name=_('Free Price'))
    canceled = tables.Column(
        empty_values=(), verbose_name=_('Canceled Price'))
    billed = tables.Column(
        empty_values=(), verbose_name=_('Billed Price'))
    started = tables.Column(
        empty_values=(), verbose_name=_('Order Creation Time'))
    ended = tables.Column(
        empty_values=(), verbose_name=_('Order Checkout Time'))
    actions = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Actions'))
    actions_template = 'landing/_order_table_actions_column.html'

    class Meta:
        model = Order
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'table', 'total', 'free', 'canceled', 'billed',
            'started', 'ended',)
        sequence = ('number', 'table', )

    def __init__(self, *args, **kwargs):
        super(OrderTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_total(self, record):
        return record.sum

    def render_free(self, record):
        return record.free_sum

    def render_canceled(self, record):
        return record.canceled_sum

    def render_billed(self, record):
        return record.total_billing_price

    def render_started(self, record):
        return record.created

    def render_ended(self, record):
        return record.checkout_at

    def render_actions(self, record):
        return render_to_string(
            self.actions_template, context={'record': record})
