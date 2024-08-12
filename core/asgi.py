"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# application = get_asgi_application()




import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from echo import routing as echo_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            echo_routing.websocket_urlpatterns
        )
    ),
})
