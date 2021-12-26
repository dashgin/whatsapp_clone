from django.urls import path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
]
