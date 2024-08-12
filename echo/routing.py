# from django.urls import path

# from echo import consumers

# websocket_urlpatterns = [
#     path('ws/', consumers.EchoConsumer)
# ]



# echo/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/', consumers.EchoConsumer.as_asgi()),  # Make sure you are using as_asgi() method
    path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),
]
