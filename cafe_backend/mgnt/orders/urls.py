from django.urls import path, include
from . import views


app_name = 'cafe_backend.mgnt.orders'

urlpatterns = [
    path('', views.TableGridView.as_view(), name='table_gridview'),
    path('<int:pk>', views.OrderUpdateView.as_view(), name='order_updateview'),
]