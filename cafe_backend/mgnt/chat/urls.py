from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'cafe_backend.mgnt.orders'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='chat_listview'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    # path(
    # '<int:pk>', views.OrderUpdateView.as_view(), name='order_updateview'),
]
