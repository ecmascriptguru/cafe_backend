from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('tables/', include(('cafe_backend.apps.users.urls', 'cafe_backend.apps.users'),
        namespace='settings:users')),
]