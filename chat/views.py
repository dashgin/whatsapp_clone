from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .models import Room

User = get_user_model()


class Index(View):
    def get(self, request):
        users = User.objects.exclude(id=self.request.user.id)
        context = {
            'users': users
        }
        return render(self.request, 'index.html', context)


class RoomView(LoginRequiredMixin, View):

    def get(self, request, room_name):
        room = Room.objects.filter(id=room_name).first()
        if (self.request.user == room.first_user) or (self.request.user == room.second_user):
            messages = room.messages.all()

            context = {
                'room': room,
                'messages': messages
            }
            return render(self.request, 'chat/room.html', context)
        return redirect('chat:index')


class StartChat(LoginRequiredMixin, View):
    """
    take username and start chat with request user and him/her
    """

    def get(self, request, username):
        second_user = User.objects.get(username=username)
        room = Room.objects.filter(
            first_user=self.request.user,
            second_user=second_user).first() or Room.objects.filter(
            second_user=self.request.user, first_user=second_user).first()
        if room:
            return redirect('chat:room', room_name=room.id)
        else:
            room, _ = Room.objects.get_or_create(first_user=self.request.user, second_user=second_user)
        return redirect('chat:room', room_name=room.id)


class VideoChat(LoginRequiredMixin, View):

    def get(self, request, room_name):
        room = Room.objects.filter(id=room_name).first()
        if (self.request.user == room.first_user) or (self.request.user == room.second_user):
            context = {
                'room': room
            }
            return render(self.request, 'chat/video_chat.html', context)
        return redirect('chat:index')
