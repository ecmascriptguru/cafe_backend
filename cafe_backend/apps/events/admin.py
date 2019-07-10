from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Event
from .forms import EventAdminForm


class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    form = EventAdminForm
    fields = (
        'name', 'event_type', 'file', 'from_date', 'to_date',
        'at', 'event_date', 'is_active', 'details', 'repeat', (
            'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'))

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
