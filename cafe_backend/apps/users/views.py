from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/user_listview.html'
