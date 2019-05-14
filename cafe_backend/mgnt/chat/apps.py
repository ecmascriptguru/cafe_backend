from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ChatConfig(AppConfig):
    name = 'cafe_backend.mgnt.chat'
    verbose_name = _('chat')

    def ready(self):
        from . import signals
