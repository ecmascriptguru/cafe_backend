import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from .models import Emoticon


class EmoticonTable(tables.Table):
    number = tables.Column(
        empty_values=(), verbose_name='#', orderable=False)
    file = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('File'))
    actions = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Actions'))
    file_template = 'emoticons/_emoticon_table_file_column.html'
    actions_template = 'emoticons/_emoticon_table_actions_column.html'

    class Meta:
        model = Emoticon
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'name', 'file', 'modified')
        sequence = (
            'number', 'name', 'file', 'modified', 'actions')

    def __init__(self, *args, **kwargs):
        super(EmoticonTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_file(self, record):
        return render_to_string(
            self.file_template, context={'record': record})

    def render_actions(self, record):
        return render_to_string(
            self.actions_template, context={'record': record})
