from django.urls import path, include
from . import views


app_name = 'cafe_backend.settings.events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_listview'),
    path('<int:pk>', views.EventUpdateView.as_view(), name='event_updateview'),
]
