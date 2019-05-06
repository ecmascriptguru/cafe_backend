from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.http.request import QueryDict
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
    dish_booking_template_name = 'bookings/dish_booking_detailview.html'

    def get_template_names(self):
        if self.object.booking_type == BOOKING_TYPE.dish:
            return self.dish_booking_template_name
        return self.template_name


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.BookingSerializer
    queryset = Booking.objects.all()

    @action(detail=False, methods=['get', 'post'], url_name='send_contact')
    def contacts(self, request):
        if hasattr(request.data, 'dict'):
            params = request.data.dict()
        else:
            params = request.data

        params['requester'] = self.request.user.table

        serializer = serializers.ContactSerializer(data=params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get_serializer_class(self):
        if self.action == 'contacts':
            return serializers.ContactSerializer
        return super().get_serializer_class()


class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.ContactSerializer
    queryset = Booking.contacts

    def get_serializer_context(self, request, *args, **kwargs):
        params = super(ContactViewSet, self).get_serializer_context(
            request, *args, **kwargs)
        return params


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
