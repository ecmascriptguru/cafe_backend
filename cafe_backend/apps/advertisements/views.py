from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from .models import Advertisement
from .tables import AdvertisementTable
from .filters import AdvertisementFilter
from .forms import AdsForm
from .serializers import AdsSerializer


class AdsListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Advertisement
    template_name = 'ads/ads_listview.html'
    table_class = AdvertisementTable
    filterset_class = AdvertisementFilter
    strict = False


class AdsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Advertisement
    template_name = 'ads/ads_createview.html'
    form_class = AdsForm
    success_url = reverse_lazy('ads:ads_listview')


class AdsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Advertisement
    template_name = 'ads/ads_detailview.html'
    success_url = reverse_lazy('ads:ads_listview')


class AdsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Advertisement
    template_name = 'ads/ads_updateview.html'
    form_class = AdsForm
    success_url = reverse_lazy('ads:ads_listview')


class AdsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Advertisement
    template_name = 'ads/ads_deleteview.html'
    success_url = reverse_lazy('ads:ads_listview')


class AdsViewSet(CafeModelViewSet):
    serializer_class = AdsSerializer
    http_method_names = ('get', )
    pagination_class = None
    queryset = Advertisement.objects.filter(is_active=True)
