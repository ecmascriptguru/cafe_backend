from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'cafe_backend.mgnt.music'

urlpatterns = [
    path('demo', views.MusicDemoView.as_view(), name='music_demoview'),
    path('player', views.MusicPlayerView.as_view(), name='music_player'),
    path(
        'playlist', views.PlaylistView.as_view(),
        name='music_playlist_view'),
]
