from celery import shared_task
from ...core.channels.sockets import broadcast_video_event


@shared_task(bind=True)
def send_video_notification_to_tables(self, video_pk):
    broadcast_video_event(video_pk)
