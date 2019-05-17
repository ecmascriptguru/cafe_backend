from __future__ import absolute_import, unicode_literals

from celery import task, shared_task
from cafe_backend.core.channels.sockets import broadcast_events
from .models import Event


@shared_task(bind=True)
def check_valid_events(self):
    events = Event.active_events()
    if len(events) > 0:
        count = broadcast_events(events)
        return "%d event(s) notified to clients." % count
    else:
        return "No active event. Skipping..."
