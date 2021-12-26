from django.urls import path

from .views import Index, RoomView, StartChat

app_name = 'chat'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<str:room_name>/', RoomView.as_view(), name='room'),
    path('start/<str:username>/', StartChat.as_view(), name='start'),
]
