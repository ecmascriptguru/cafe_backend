from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from cafe_backend.mgnt.chat.routing import chat_socket_urlpatterns
from cafe_backend.apps.users.routing import monitor_socket_urlpatterns

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_socket_urlpatterns + monitor_socket_urlpatterns
        )
    ),
})
