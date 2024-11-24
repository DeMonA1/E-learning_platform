import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Accepts any WebSocket connection and echoes to the
    WebSocket client every message it receives.
    (like view in WSGI)
    """
    async def connect(self):
        # every consumer has a scope
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group; use asy...sync() wrapper to use the channel
        # layer async method in sync code
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json: dict = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # send message to room group
        await self.channel_layer.group_send(
            # type - method that should be invoked on consumers that
            # receives the event
            self.room_group_name, {'type': 'chat_message',
                                   'message': message,
                                   'user': self.user.username,
                                   'datetime': now.isoformat()}
        )
        
    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))