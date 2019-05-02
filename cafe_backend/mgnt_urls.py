from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('orders/', include((
            'cafe_backend.mgnt.orders.urls', 'cafe_backend.mgnt.orders'
        ), namespace='orders')),
]
