import itertools
import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from .models import Playlist, Music


class PlaylistTable(tables.Table):
    number = tables.Column(
        empty_values=(), verbose_name='#', orderable=False)
    title = tables.Column(accessor='music.title')
    author = tables.Column(accessor='music.author')
    actions = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Actions'))
    actions_template = 'music/_playlist_table_actions_column.html'

    index = 0

    class Meta:
        model = Playlist
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('created', 'modified', 'id', 'music', 'is_active', )
        sequence = (
            'number', 'title', 'author', 'table', )

    def __init__(self, *args, **kwargs):
        super(PlaylistTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_actions(self, record):
        self.index += 1
        return render_to_string(
            self.actions_template, context={
                'record': record, 'is_start': self.index == 1,
                'is_end': self.index == len(self.rows)})
