from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('ads/', include((
        'cafe_backend.apps.advertisements.urls',
        'cafe_backend.apps.advertisements'), namespace='ads')),
    path('events/', include((
        'cafe_backend.apps.events.urls',
        'cafe_backend.apps.events'), namespace='events')),
    path('tables/', include((
        'cafe_backend.apps.users.urls', 'cafe_backend.apps.users'),
        namespace='tables')),
    path('emoticons/', include((
        'cafe_backend.apps.emoticons.urls', 'cafe_backend.apps.emoticons'),
        namespace='emoticons')),
    path('videos/', include((
        'cafe_backend.apps.videos.urls', 'cafe_backend.apps.videos'),
        namespace='videos')),
    path('', include((
        'cafe_backend.apps.dishes.urls', 'cafe_backend.apps.dishes'),
        namespace='dishes')),
]
