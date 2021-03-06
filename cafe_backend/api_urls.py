from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('', include((
        'cafe_backend.apps.dishes.urls_api',
        'cafe_backend.apps.dishes'), namespace='api:caregories')),

    path('', include((
        'cafe_backend.mgnt.orders.urls_api',
        'cafe_backend.mgnt.orders'), namespace='api:orders')),

    path('', include((
        'cafe_backend.mgnt.bookings.urls_api',
        'cafe_backend.mgnt.bookings'), namespace='api:bookings')),

    path('', include((
        'cafe_backend.apps.users.urls_api',
        'cafe_backend.apps.users'), namespace='api:tables')),

    path('', include((
        'cafe_backend.apps.advertisements.urls_api',
        'cafe_backend.apps.advertisements'), namespace='api:ads')),

    path('', include((
        'cafe_backend.apps.events.urls_api',
        'cafe_backend.apps.events'), namespace='api:events')),

    path('', include((
        'cafe_backend.apps.emoticons.urls_api',
        'cafe_backend.apps.emoticons'), namespace='api:emoticons')),

    path('', include((
        'cafe_backend.mgnt.chat.urls_api',
        'cafe_backend.mgnt.chat'), namespace='api:chat')),

    path('', include((
        'cafe_backend.mgnt.music.urls_api',
        'cafe_backend.mgnt.music'), namespace='api:music')),

    path('', include((
        'cafe_backend.apps.versions.urls_api',
        'cafe_backend.apps.versions'), namespace='api:versions')),
]
