from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from .models import Table
from .forms import TableForm
from .serializers import TableSerializer


class TablesListView(LoginRequiredMixin, generic.ListView):
    model = Table
    template_name = 'tables/table_listview.html'


class TableUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Table
    template_name = 'tables/table_updateview.html'
    form_class = TableForm
    success_url = reverse_lazy('tables:table_listview')


class TableViewSet(CafeModelViewSet):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    pagination_class = None
    http_method_names = ['get', ]
