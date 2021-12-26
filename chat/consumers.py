import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        try:
            image_content = text_data_json['image_content']
        except KeyError:
            image_content = None
        try:
            audio_content = text_data_json['audio_content']
        except KeyError:
            audio_content = None
        user = self.scope['user']

        m = await sync_to_async(Message.objects.create)(
            room_id=self.room_name,
            user=user,
            text_content=message,
            image_content=image_content,
            audio_content=audio_content,
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': m.text_content,
                'image': m.image_content,
                'audio': m.audio_content,
                'user': user.username,
                'timestamp': m.get_short_date()
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        image = event['image']
        audio = event['audio']
        user = event['user']
        timestamp = event['timestamp']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'timestamp': timestamp,
            'image': image,
            'audio': audio
        }))
