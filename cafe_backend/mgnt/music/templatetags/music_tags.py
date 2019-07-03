from django import template
from ..models import (
    MUSIC_PROVIDER, MUSIC_STATE, Playlist, MUSIC_PLAYLIST_STATE)


register = template.Library()


@register.filter('pending_playlist_length')
def pending_playlist_length(temp):
    if len(Playlist.pendings()) > 0:
        return len(Playlist.pendings())
    else:
        return ''
