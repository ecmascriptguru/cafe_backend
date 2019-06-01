from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LandingConfig(AppConfig):
    name = 'cafe_backend.apps.landing'
    verbose_name = _('landing')
