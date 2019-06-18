from django.conf.urls import url

from . import consumers

monitor_socket_urlpatterns = [
    url(
        r'^ws/monitor/(?P<user_pk>[^/]+)/$', consumers.MonitorConsumer),
]
