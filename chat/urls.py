from django.urls import path

from .views import Index, RoomView, StartChat, VideoChat

app_name = 'chat'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<str:room_name>/', RoomView.as_view(), name='room'),
    path('start/<str:username>/', StartChat.as_view(), name='start'),
    path('video/<str:room_name>/', VideoChat.as_view(), name='video'),
]
