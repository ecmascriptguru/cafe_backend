import requests
from .settings import TING_API_METHOD


BASE_URL = 'http://tingapi.ting.baidu.com/v1/restserver/ting'


class TingMusicAPI:
    DEFAULT_FIELDS = ('songid', 'songname', 'artistname',)

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def search_music(cls, keyword, fields=None):
        if not fields:
            fields = cls.DEFAULT_FIELDS

        if not keyword or keyword == '':
            raise Exception('Keyword parameter is required')

        data = {
            'method': TING_API_METHOD.search,
            'query': keyword}

        response = requests.get(BASE_URL, params=data)
        try:
            songs = response.json().get('song', [])
            result = list()
            for song in songs:
                temp = dict()
                for field in fields:
                    temp[field] = song.get(field)
                result.append(temp)

            return result

        except Exception as e:
            print(str(e))
            return None

    @classmethod
    def retrieve_music(cls, song_id):
        data = {
            'method': TING_API_METHOD.retrieve,
            'songid': song_id}

        response = requests.get(BASE_URL, params=data)

        try:
            return response.json()
        except Exception as e:
            return None
