from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('categories/', include(('cafe_backend.apps.dishes.urls_api', 'cafe_backend.apps.dishes'),
        namespace='api:caregories')),
]