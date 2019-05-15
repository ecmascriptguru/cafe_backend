from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(
        r'^ws/chat/(?P<user_pk>[^/]+)/(?P<channel_pk>[^/]+)/$',
        consumers.ChatConsumer),
]
