from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from .serializers import EventSerializer
from .models import Event, EVENT_TYPE
from .forms import EventForm


class EventViewSet(CafeModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.active_events()


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'events/event_listview.html'


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    template_name = 'events/event_updateview.html'
    form_class = EventForm


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = 'events/event_deleteview.html'
