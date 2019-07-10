import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from .models import Event


class EventTable(tables.Table):
    number = tables.Column(
        empty_values=(), verbose_name='#', orderable=False)
    image = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('image'))
    actions = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Actions'))
    is_active = tables.BooleanColumn(verbose_name=_('Active Now?'))
    image_template = 'events/_event_table_image_column.html'
    actions_template = 'events/_event_table_actions_column.html'

    class Meta:
        model = Event
        template_name = 'django_tables2/bootstrap.html'
        exclude = (
            'id', 'created', 'modified', 'file', 'details', 'event_type',)
        sequence = (
            'number', 'image', 'name', 'from_date', 'to_date',
            'at', 'repeat', 'event_date', 'is_active', 'actions', )

    def __init__(self, *args, **kwargs):
        super(EventTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_image(self, record):
        return render_to_string(
            self.image_template, context={'record': record})

    def render_actions(self, record):
        return render_to_string(
            self.actions_template, context={'record': record})
