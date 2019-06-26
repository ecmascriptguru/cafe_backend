from django.urls import path, include
from . import views


app_name = 'cafe_backend.mgnt.orders'

urlpatterns = [
    path(
        '', views.TableGridView.as_view(),
        name='table_gridview'),
    path(
        'print', views.OrdersPrintView.as_view(),
        name='orders_printview'),
    path(
        '<int:pk>/', views.OrderDetailView.as_view(),
        name='order_detailview'),
    path(
        '<int:pk>/edit', views.OrderUpdateView.as_view(),
        name='order_updateview'),
    path(
        '<int:pk>/print', views.OrderPrintView.as_view(),
        name='order_printview'),
    path(
        '<int:pk>/print_callback', views.OrderPrintCallbackView.as_view(),
        name='order_print_callbackview'),
    path(
        'items/<int:pk>/print', views.OrderItemPrintView.as_view(),
        name='order_item_printview'),
    path(
        '<int:order_pk>/items/new', views.FreeItemCreateView.as_view(),
        name='order_free_createview'),
]
