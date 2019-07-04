from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.landing'

urlpatterns = [
    path(
        '', views.DashboardView.as_view(), name='dashboard'
    ),
    path(
        'customers', views.CustomerReportView.as_view(),
        name='customer_reportview'
    ),
    path(
        'orders', views.OrderReportView.as_view(),
        name='order_reportview'
    ),
    path(
        'dishes', views.DishReportView.as_view(),
        name='dish_reportview'
    ),
    path(
        'sales/print', views.SalesReportPrintView.as_view(),
        name='sales_printview'
    ),
    path(
        'print', views.DashboardPrintView.as_view(),
        name='dashboard_printview'
    ),
]
