from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BookingsConfig(AppConfig):
    name = 'cafe_backend.mgnt.bookings'
    verbose_name = _('bookings')

    def ready(self):
        from . import signals
