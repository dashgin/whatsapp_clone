from django.contrib import admin

from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('first_user', 'second_user', 'created_at',)
    fields = ('first_user', 'second_user', 'id', "created_at",)
    readonly_fields = ('id', "created_at",)
    list_filter = ('created_at',)
    search_fields = ('first_user', 'second_user',)
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'text_content', 'audio_content', 'image_content', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('text_content',)
    ordering = ('-created_at',)
