from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'cafe_backend.mgnt.chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='chat_listview'),
]
