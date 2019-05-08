from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .models import Advertisement
from .tables import AdvertisementTable
from .filters import AdvertisementFilter


class AdsListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Advertisement
    template_name = 'ads/ads_listview.html'
    table_class = AdvertisementTable
    filterset_class = AdvertisementFilter
    strict = False
