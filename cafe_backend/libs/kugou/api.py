import requests
from .settings import (
    SONG_RETRIEVE_API_BASE_URL, SONG_SEARCH_API_BASE_URL)


class KugouMusicAPI:
    @classmethod
    def build_search_url(cls, keyword, page, per_page, **kwargs):
        return SONG_SEARCH_API_BASE_URL.format(
            keyword=keyword, page=page, per_page=per_page)

    @classmethod
    def search(cls, keyword, page=1, per_page=20, **kwargs):
        resposne = requests.get(cls.build_search_url(keyword, page, per_page))
        try:
            json_response = resposne.json().get('data', {}).get('lists', [])
            songs = list()
            for item in json_response:
                songs.append({
                    'title': item['SongName'],
                    'file_hash': item['FileHash'],
                    'album_id': item['AlbumID']
                })
            return songs
        except Exception as e:
            print(str(e))
            return []

    @classmethod
    def build_retrieve_url(cls, file_hash, album_id, **kwargs):
        return SONG_RETRIEVE_API_BASE_URL.format(
            file_hash=file_hash, album_id=album_id)

    @classmethod
    def retrieve(cls, file_hash, album_id, **kwargs):
        response = requests.get(cls.build_retrieve_url(file_hash, album_id))
        return json_data
