from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VersionsConfig(AppConfig):
    name = 'cafe_backend.apps.versions'
    verbose_name = _('versions')

    def ready(self):
        from . import signals
