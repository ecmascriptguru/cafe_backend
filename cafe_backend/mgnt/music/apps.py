from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MusicConfig(AppConfig):
    name = 'cafe_backend.mgnt.music'
    verbose_name = _('music')

    def ready(self):
        from . import signals
