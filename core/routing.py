# from channels.routing import ProtocolTypeRouter , URLRouter
# from channels.auth import AuthMiddlewareStack

# from echo import routing as echo_routing

# application = ProtocolTypeRouter({
#     'websocket' : AuthMiddlewareStack(
#         URLRouter(
#             echo_routing.websocket_urlpatterns
#         )
#     )

# })



from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from echo import routing as echo_routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            echo_routing.websocket_urlpatterns
        )
    ),
})