from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Table
from .forms import TableForm


class TablesListView(generic.ListView):
    model = Table
    template_name = 'tables/table_listview.html'


class TableUpdateView(generic.UpdateView):
    model = Table
    template_name = 'tables/table_updateview.html'
    form_class = TableForm
