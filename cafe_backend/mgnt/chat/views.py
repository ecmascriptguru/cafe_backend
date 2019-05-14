import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.views import generic
from cafe_backend.core.apis.viewsets import CafeModelViewSet
from .serializers import ChannelSerializer
from .models import Channel


class ChatListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'chat/chat_listview.html'


def room(request, room_name):
    return render(request, 'chat/chat_room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


class ChannelViewSet(CafeModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def get_queryset(self):
        return self.request.user.get_active_channels()
