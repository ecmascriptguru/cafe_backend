from django.conf.urls import url

from . import consumers

chat_socket_urlpatterns = [
    url(
        r'^ws/chat/(?P<user_pk>[^/]+)/$', consumers.ChatConsumer),
]
