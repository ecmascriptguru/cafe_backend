from django.contrib import admin
from .models import Event
from .forms import EventAdminForm


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    fields = (
        'name', 'event_type', 'file', 'from_date', 'to_date',
        'at', 'event_date', 'is_active', 'details', 'repeat', (
            'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'))

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
