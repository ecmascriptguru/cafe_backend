from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Music, MUSIC_PROVIDER, Playlist
from .tasks import (
    grab_music_to_s3, spotify_add_music_to_playlist,
    send_music_notification_via_socket)


@receiver(post_save, sender=Music)
def copy_music_to_s3(sender, instance, created, **kwargs):
    if created and instance.provider == MUSIC_PROVIDER.ting:
        grab_music_to_s3.delay([instance.pk])


@receiver(post_save, sender=Playlist)
def add_to_playlist_on_spotify(sender, instance, created, **kwargs):
    send_music_notification_via_socket.delay()
    if created and instance.music.provider == MUSIC_PROVIDER.spotify:
        pass
        # spotify_add_music_to_playlist.delay([instance.pk])
