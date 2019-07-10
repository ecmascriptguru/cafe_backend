from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmoticonsConfig(AppConfig):
    name = 'cafe_backend.apps.emoticons'
    verbose_name = _('emoticons')

    def ready(self):
        from . import signals
