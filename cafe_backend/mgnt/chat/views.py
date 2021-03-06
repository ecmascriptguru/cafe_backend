import json
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.views import generic
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from cafe_backend.core.apis.viewsets import CafeModelViewSet, viewsets
from .serializers import ChannelSerializer
from .models import Channel


class ChatListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'chat/chat_list.html'

    def get_context_data(self, *args, **kwargs):
        data = super(ChatListView, self).get_context_data(*args, **kwargs)
        if settings.DEBUG:
            data['channels'] = Channel.objects.all()
        else:
            data['channels'] = [Channel.get_public_channel()]
        return data


class ChannelViewSet(CafeModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Channel.objects.all()
        else:
            return self.request.user.get_active_channels()

    @action(detail=True, methods=['post'], url_name='channel_clear')
    def clear(self, request, **kwargs):
        channel = self.get_object()
        channel.messages.all().delete()
        return Response({'status': True})
