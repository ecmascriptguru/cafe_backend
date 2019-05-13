from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('orders/', include((
            'cafe_backend.mgnt.orders.urls', 'cafe_backend.mgnt.orders'
        ), namespace='orders')),

    path('chat/', include((
            'cafe_backend.mgnt.chat.urls', 'cafe_backend.mgnt.chat'
        ), namespace='chat')),

    path('bookings/', include((
            'cafe_backend.mgnt.bookings.urls', 'cafe_backend.mgnt.bookings'
        ), namespace='bookings')),
]
