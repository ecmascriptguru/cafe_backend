from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.advertisements'

urlpatterns = [
    path(
        '', views.AdsListView.as_view(),
        name='ads_listview'),
    path(
        'new', views.AdsCreateView.as_view(),
        name='ads_createview'),
    path(
        '<int:pk>', views.AdsDetailView.as_view(),
        name='ads_detailview'),
    path(
        '<int:pk>/edit', views.AdsUpdateView.as_view(),
        name='ads_updateview'),
    path(
        '<int:pk>/delete', views.AdsDeleteView.as_view(),
        name='ads_deleteview'),
]
