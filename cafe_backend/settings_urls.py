from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('ads/', include((
        'cafe_backend.apps.advertisements.urls',
        'cafe_backend.apps.advertisements'), namespace='ads')),
    path('tables/', include((
        'cafe_backend.apps.users.urls', 'cafe_backend.apps.users'),
        namespace='tables')),
    path('', include((
        'cafe_backend.apps.dishes.urls', 'cafe_backend.apps.dishes'),
        namespace='dishes')),
]
