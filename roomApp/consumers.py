import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync


# Following my university-final-proj
# Instead of using AsyncWebsockerConsumer, using only WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    # Create an asynchronous connection-function
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(f'Room name: {self.room_name}')
        print(f'Room gorup name: {self.room_group_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name    # channels automatically fixes room-name?
        )
        print('Backend Consumer (Websocket): Connected!')

        async_to_sync(self.accept())

    def disconnect(self, *args, **kwargs):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('Backend Consumer (Websocket): Disconnected!')


"""
[NB]: Create a routing file for the consumer, like urls for each views.
"""
