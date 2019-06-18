import requests
from django.conf import settings


class EYPrint(object):
    base_url = 'http://www.eyprint.com/public/'

    @classmethod
    def print(cls, url_58=None, url_80=None, **kwargs):
        cls.print_58(url_58, **kwargs)
        if url_80 is not None:
            cls.print_80(url_80)

    @classmethod
    def print_58(cls, url, **kwargs):
        if settings.DEBUG:
            url = 'http://www.eyprint.com/apiDemo/index.html'
        data = {
            'key': settings.EYPRINT_58_API_KEY,
            'sourceFile': url,
            'paperWidth': 58,
            'Scaling': False,
            'Type': kwargs.get('Type', 'html'),
        }
        return requests.post(cls.base_url, data=data)

    @classmethod
    def print_80(cls, url, **kwargs):
        if settings.DEBUG:
            url = 'http://www.eyprint.com/apiDemo/index.html'
        data = {
            'key': settings.EYPRINT_80_API_KEY,
            'sourceFile': url,
            'Type': kwargs.get('Type', 'html'),
            'paperWidth': 80,
            'Scaling': False,
        }
        return requests.post(cls.base_url, data=data)
