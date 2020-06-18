from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.versions'

urlpatterns = [
    path(
        '/', views.AppDownloadView.as_view(), name='app_downloadview'),
    path(
        '', views.AppDownloadView.as_view(), name='app_downloadview_1'),
]
