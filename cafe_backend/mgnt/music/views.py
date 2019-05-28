from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from cafe_backend.core.apis.viewsets import CafeModelViewSet, viewsets
from cafe_backend.core.constants.states import MUSIC_STATE
from . import serializers
from .models import Music, Playlist


class MusicDemoView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'music/music_demoview.html'


class MusicPlayerView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/music_player.html'
    model = Playlist

    def get_queryset(self, *args, **kwargs):
        return Playlist.objects.filter(is_active=True)


class MusicViewSet(CafeModelViewSet):
    serializer_class = serializers.MusicSerializer
    queryset = Music.objects.all()

    @action(detail=False, methods=['get'], url_name='music_search')
    def search(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        if not keyword or keyword == '':
            return Response([])

        songs = Music.external_search(keyword)
        return Response(songs)

    def get_object(self, *args, **kwargs):
        return Music.objects.filter(external_id=self.kwargs.get('pk'))

    @action(detail=False, methods=['post'], url_name='music_subscribe')
    def subscribe(self, request, *args, **kwargs):
        self.serializer_class = serializers.MusicSubscribeSerializer
        return super(MusicViewSet, self).create(request, *args, **kwargs)


class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlaylistSerializer
    queryset = Playlist.objects.filter(
        is_active=True, music__state=MUSIC_STATE.ready)
    pagination_class = None
    http_method_names = ('get', 'post')

    @action(detail=True, methods=['get'], url_name='playlist_archive')
    def archive(self, request, *args, **kwargs):
        item = self.get_object()
        item.is_active = False
        item.save()
        return Response({'status': True})
