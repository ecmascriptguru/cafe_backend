from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.users'

urlpatterns = [
    path('', views.TablesListView.as_view(), name='table_listview'),
    path('<int:pk>', views.TableUpdateView.as_view(), name='table_updateview'),
    path(
        '<int:pk>/clear', views.TableUpdateView.as_view(),
        name='table_clearview'),
    path(
        '<int:pk>/control', views.TableControlView.as_view(),
        name='table_controlview'),
]
