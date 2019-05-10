from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventsConfig(AppConfig):
    name = 'cafe_backend.apps.events'
    verbose_name = _('events')

    def ready(self):
        from . import signals
