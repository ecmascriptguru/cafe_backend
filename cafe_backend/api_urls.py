from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('', include((
        'cafe_backend.apps.dishes.urls_api',
        'cafe_backend.apps.dishes'), namespace='api:caregories')),

    path('', include((
        'cafe_backend.mgnt.orders.urls_api',
        'cafe_backend.mgnt.orders'), namespace='api:orders')),
]
