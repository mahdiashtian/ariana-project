from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from core.consumers import OnlineUserConsumer
from library.security.ws_auth import jwt_auth_middleware_stack

websocket_urlpatterns = [
    path("ws/online/", OnlineUserConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": jwt_auth_middleware_stack(URLRouter(websocket_urlpatterns)),
    }
)
