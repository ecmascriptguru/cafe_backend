from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VideosConfig(AppConfig):
    name = 'cafe_backend.apps.videos'
    verbose_name = _('videos')

    def ready(self):
        from . import signals
