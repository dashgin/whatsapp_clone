from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .models import Room


class Index(View):
    def get(self, request):
        users = User.objects.exclude(id=self.request.user.id)
        context = {
            'users': users
        }
        return render(self.request, 'index.html', context)


class RoomView(View):
    def get(self, request, room_name):
        room = Room.objects.filter(id=room_name).first()
        messages = room.messages.all()
        print(messages)
        context = {
            'room': room,
            'messages': messages
        }
        return render(self.request, 'chat/room.html', context)


class StartChat(View):
    """
    take username and start chat with request user and him/her
    """

    def get(self, request, username):
        # username = request.POST.get('username')
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
