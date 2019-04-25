from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.users'

urlpatterns = [
    path('', views.TablesListView.as_view(), name='table_listview'),
    path('<int:pk>', views.TableUpdateView.as_view(), name='table_updateview'),
]
