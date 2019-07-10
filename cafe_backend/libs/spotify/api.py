import asyncio
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings


client_credentials_manager = SpotifyClientCredentials(
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Spotify:
    @classmethod
    def search(cls, keyword, types=['artist', 'track'], **kwargs):
        response = sp.search(keyword, **kwargs)
        result = list()
        for item in response['tracks']['items']:
            result.append({
                'songid': item['id'], 'songname': item['name'],
                'artistname': item['artists'][0]['name']
            })
        return result

    @classmethod
    def get_playlists(cls, limit=50, offset=0):
        username = settings.SPOTIFY_USERNAME
        response = sp.user_playlists(username, limit=limit, offset=offset)
        return response['items']

    @classmethod
    def create_playlist(cls, name):
        if len(cls.get_playlists()) == 0:
            response = sp.user_playlist_create(
                settings.SPOTIFY_USERNAME, settings.SPOTIFY_PLAYLIST_NAME,
                public=False)
            return response
        else:
            return None

    @classmethod
    def get_auth_token(cls, scope='playlist-modify-private'):
        util.get_auth_token

    @classmethod
    def retrieve_music(cls, external_id, **kwargs):
        response = sp.track(external_id)
        return {
            'name': response['name'],
            'author': response['artists'][0]['name'],
            'url': response['external_urls']['spotify'],
            'pic_url': response['album']['images'][0]['url']}
