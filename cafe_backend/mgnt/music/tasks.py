from celery import shared_task
from ...libs.spotify.browser import SpotifyBrowser
from .models import Music, Playlist
from ...core.channels.sockets import broadcast_music_event


@shared_task
def grab_music_to_s3(music_ids):
    total = len(music_ids)
    count = 0
    for pk in music_ids:
        music = Music.objects.get(pk=pk)
        try:
            music.process()
            count += 1
        except Exception as e:
            pass
    return total, count


@shared_task(bind=True)
def check_invalid_musics(self):
    musics = [item['pk'] for item in Music.get_invalid_musics().values('pk')]
    return grab_music_to_s3(musics)


@shared_task(bind=True)
def spotify_add_music_to_playlist(self, ids=[]):
    browser = SpotifyBrowser()
    try:
        for playlist_id in ids:
            playlist = Playlist.objects.get(pk=playlist_id)
            music = playlist.music
            browser.add_music_to_playlist(music.url)
    except Exception as e:
        print(str(e))
    finally:
        browser.close()


@shared_task
def send_music_notification_via_socket():
    broadcast_music_event()
