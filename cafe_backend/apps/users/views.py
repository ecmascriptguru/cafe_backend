from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Table


class UserListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/user_listview.html'


class TablesListView(generic.ListView):
    model = Table
    template_name = 'tables/table_listview.html'
