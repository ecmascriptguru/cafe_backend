from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from ...core.apis.viewsets import CafeModelViewSet
from . import tables, filters, models, forms, serializers


class EmojiListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = tables.EmoticonTable
    filterset_class = filters.EmoticonFilter
    strict = False
    template_name = 'emoticons/emoticon_listview.html'


class EmoticonCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Emoticon
    template_name = 'emoticons/emoticon_formview.html'
    form_class = forms.EmoticonForm
    success_url = reverse_lazy('emoticons:emoticon_listview')


class EmoticonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Emoticon
    template_name = 'emoticons/emoticon_formview.html'
    form_class = forms.EmoticonForm
    success_url = reverse_lazy('emoticons:emoticon_listview')


class EmoticonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Emoticon
    template_name = 'emoticons/emoticon_deleteview.html'
    success_url = reverse_lazy('emoticons:emoticon_listview')


class EmoticonViewSet(CafeModelViewSet):
    serializer_class = serializers.EmoticonSerializer
    queryset = models.Emoticon.objects.all()
    http_method_names = ('get', )
