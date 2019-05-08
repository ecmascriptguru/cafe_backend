from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Table
from .forms import TableForm


class TablesListView(LoginRequiredMixin, generic.ListView):
    model = Table
    template_name = 'tables/table_listview.html'


class TableUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Table
    template_name = 'tables/table_updateview.html'
    form_class = TableForm
    success_url = reverse_lazy('tables:table_listview')
