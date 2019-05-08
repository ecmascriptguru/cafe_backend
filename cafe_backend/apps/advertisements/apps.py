from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AdvertisementsConfig(AppConfig):
    name = 'cafe_backend.apps.advertisements'
    verbose_name = 'advertisements'

    def ready(self):
        from . import signals
