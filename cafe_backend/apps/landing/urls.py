from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.landing'

urlpatterns = [
    path(
        '', views.DashboardView.as_view(), name='dashboard'),
]
