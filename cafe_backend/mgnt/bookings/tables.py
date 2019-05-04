import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Booking, BookingMessage, BOOKING_TYPE, BOOKING_STATE


class BookingTable(tables.Table):
    number = tables.Column(empty_values=(), verbose_name='Contact #')
    actions = tables.Column(empty_values=(), orderable=False)
    actions_template = 'bookings/_booking_table_actions_column.html'

    class Meta:
        model = Booking
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('created', 'modified', 'id', 'details', )
        sequence = (
            'number', 'requester', 'receiver', 'booking_type',
            'state', 'actions', )

    def __init__(self, *args, **kwargs):
        super(BookingTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_actions(self, record):
        return render_to_string(
            self.actions_template, context={'record': record})
