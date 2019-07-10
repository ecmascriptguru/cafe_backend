from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CallsConfig(AppConfig):
    name = 'cafe_backend.mgnt.calls'
    verbose_name = _('calls')

    def ready(self):
        from . import signals
