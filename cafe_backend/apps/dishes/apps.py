from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DishesConfig(AppConfig):
    name = 'cafe_backend.apps.dishes'
    verbose_name = _('dishes')

    def ready(self):
        from . import signals
