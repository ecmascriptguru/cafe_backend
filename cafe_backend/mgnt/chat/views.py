import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.views import generic
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from .serializers import ChannelSerializer
from .models import Channel


class ChatListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'chat/chat_list.html'

    def get_context_data(self, *args, **kwargs):
        data = super(ChatListView, self).get_context_data(*args, **kwargs)
        data['channels'] = self.request.user.get_active_channels()
        return data


class ChannelViewSet(CafeModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def get_queryset(self):
        return self.request.user.get_active_channels()
