from django.urls import path, include
from . import views


app_name = 'cafe_backend.settings.events'

urlpatterns = [
    path(
        '', views.EventListView.as_view(), name='event_listview'),
    path(
        'new', views.EventCreateView.as_view(), name='event_createview'),
    path(
        '<int:pk>', views.EventDetailView.as_view(), name='event_detailview'),
    path(
        '<int:pk>/edit', views.EventUpdateView.as_view(),
        name='event_updateview'),
    path(
        '<int:pk>/delete', views.EventDeleteView.as_view(),
        name='event_deleteview'),
]
