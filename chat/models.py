import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_user.username + ' ' + self.second_user.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text_content = models.CharField(max_length=255)
    # file_content = models.FileField(upload_to='files/', blank=True, null=True)
    # image_content = models.ImageField(upload_to='images/', blank=True, null=True)
    image_content = models.TextField(blank=True, null=True)
    audio_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + self.room.first_user.username + self.room.second_user.username

    def get_short_date(self):
        return self.created_at.strftime("%H:%M")

    def get_img_tag(self):
        if self.image_content:
            return f'<img src="{self.image_content}" width="150" height="150">'
        else:
            pass

    def get_audio_tag(self):
        if self.audio_content:
            return f'<audio controls controlslist="nodownload"><source src="{self.audio_content}" type="audio/ogg"></audio>'
        else:
            pass
       