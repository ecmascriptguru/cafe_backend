from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_listview'),
]
