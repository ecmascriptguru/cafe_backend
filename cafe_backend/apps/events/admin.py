from django.contrib import admin
from cafe_backend.apps.users.admin import admin_site
from .models import Event
from .forms import EventForm


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    fields = (
        'name', 'event_type', 'file', 'from_date', 'to_date',
        'at', 'event_date', 'is_active', 'details', 'repeat', (
            'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'))

    class Meta:
        model = Event


admin_site.register(Event, EventAdmin)
