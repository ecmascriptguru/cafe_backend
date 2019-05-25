import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from .models import Advertisement, ADS_TYPE


class AdvertisementTable(tables.Table):
    number = tables.Column(
        empty_values=(), verbose_name=_('Ads #'))
    image = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Image'))
    actions = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Actions'))
    image_template = 'ads/_ads_table_image_column.html'
    actions_template = 'ads/_ads_table_actions_column.html'

    class Meta:
        model = Advertisement
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('created', 'modified', 'id', 'file', )
        sequence = (
            'number', 'image', 'name', 'type', 'is_active', 'actions', )

    def __init__(self, *args, **kwargs):
        super(AdvertisementTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_number(self):
        return next(self.counter)

    def render_image(self, record):
        return render_to_string(
            self.image_template, context={'record': record})

    def render_actions(self, record):
        return render_to_string(
            self.actions_template, context={'record': record})
