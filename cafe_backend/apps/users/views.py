from django.views import generic


class UserListView(generic.TemplateView):
    template_name = 'users/user_listview'
