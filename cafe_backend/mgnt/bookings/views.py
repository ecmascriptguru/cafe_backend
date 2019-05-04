from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import viewsets
from . import serializers
from .models import Booking, BookingMessage, BOOKING_TYPE
from .tables import BookingTable
from .filters import BookingFilter


class BookingListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Booking
    template_name = 'bookings/booking_listview.html'
    # queryset = Booking.table_bookings()
    table_class = BookingTable
    filterset_class = BookingFilter
    strict = False

    flag = BOOKING_TYPE.exchange
    table_booking_template = 'bookings/table_listview.html'

    def __init__(self, *args, **kwargs):
        super(BookingListView, self).__init__(*args, **kwargs)


class BookingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Booking
    template_name = 'bookings/contact_detailview.html'

    def get_template_names(self):
        return self.template_name


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.BookingSerializer
    queryset = Booking.objects.all()


class BookingMessageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.BookingMessageSerializer
    queryset = BookingMessage.objects.all()

    def get_queryset(self, **kwargs):
        if self.kwargs.get('booking_pk'):
            return self.queryset.filter(
                booking_id=self.kwargs.get('booking_pk'))
        else:
            return self.queryset
