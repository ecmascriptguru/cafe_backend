from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from ...core.apis.viewsets import CafeModelViewSet
from . import tables, filters, models, forms, serializers


class VideoListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = tables.VideoTable
    filterset_class = filters.VideoFilter
    strict = False
    template_name = 'videos/video_listview.html'


class VideoCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Video
    template_name = 'videos/video_formview.html'
    form_class = forms.VideoForm
    success_url = reverse_lazy('videos:video_listview')


class VideoUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Video
    template_name = 'videos/video_formview.html'
    form_class = forms.VideoForm
    success_url = reverse_lazy('videos:video_listview')


class VideoDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Video
    template_name = 'videos/video_detailview.html'


class VideoDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Video
    template_name = 'videos/video_deleteview.html'
    success_url = reverse_lazy('videos:video_listview')


class VideoViewSet(CafeModelViewSet):
    serializer_class = serializers.VideoSerializer
    queryset = models.Video.objects.all()
    http_method_names = ('get', )
