from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrdersConfig(AppConfig):
    name = 'cafe_backend.mgnt.orders'
    verbose_name = _('orders')

    def ready(self):
        from . import signals
