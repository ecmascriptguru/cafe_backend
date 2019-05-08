from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from .models import Advertisement
from .tables import AdvertisementTable
from .filters import AdvertisementFilter
from .forms import AdsForm


class AdsListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Advertisement
    template_name = 'ads/ads_listview.html'
    table_class = AdvertisementTable
    filterset_class = AdvertisementFilter
    strict = False


class AdsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Advertisement
    template_name = 'ads/ads_formview.html'
    form_class = AdsForm
    success_url = reverse_lazy('ads:ads_listview')


class AdsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Advertisement
    template_name = 'ads/ads_formview.html'
    success_url = reverse_lazy('ads:ads_listview')


class AdsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Advertisement
    template_name = 'ads/ads_formview.html'
    form_class = AdsForm
    success_url = reverse_lazy('ads:ads_listview')


class AdsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = AdsCreateView
    success_url = reverse_lazy('ads:ads_listview')
