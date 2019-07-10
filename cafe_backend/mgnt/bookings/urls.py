from django.urls import path, include
from . import views


app_name = 'cafe_backend.mgnt.bookings'

urlpatterns = [
    path(
        '', views.BookingListView.as_view(),
        name='booking_listview'),
    path(
        '<int:pk>', views.BookingDetailView.as_view(),
        name='booking_detailview'),
]
