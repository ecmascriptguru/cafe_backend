from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from rest_framework import permissions
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from .serializers import EventSerializer
from .models import Event, EVENT_TYPE
from .forms import EventForm
from .filters import EventFilter
from .tables import EventTable


class EventViewSet(CafeModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    http_method_names = ('get', )

    def get_queryset(self):
        return Event.today_events()


class EventListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Event
    template_name = 'events/event_listview.html'
    filterset_class = EventFilter
    table_class = EventTable


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    template_name = 'events/event_formview.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event_listview')


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'events/event_detailview.html'


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    template_name = 'events/event_updateview.html'
    form_class = EventForm


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = 'events/event_deleteview.html'
