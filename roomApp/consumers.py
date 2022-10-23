import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync


# Following my university-final-proj
# Instead of using AsyncWebsockerConsumer, using only WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    # Create an asynchronous connection-function
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']     # fetch the room-name from the request that's being hit from the frontend-page-load through the asgi-request-routing
        self.room_group_name = 'chat_%s' % self.room_name
        print(f'Room name: {self.room_name}')
        print(f'Room gorup name: {self.room_group_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name    # channels automatically fixes room-name?
        )
        print('Backend Consumer (Websocket): Connected!')

        async_to_sync(self.accept())

    # Receive the msg from frontend & broadcast it to the entire channel
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)    # decode json-stringified data into python-dict
        # print(data)
        message = data['message']
        username = data['username']
        room = data['room']
        # send the data to channel-group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            # pass a dictionary with custom key-value pairs
            {
                'type': 'chat_message',  # will be used to call as a method
                'message': message,
                'username': username,
                'room': room,
            }
        )

    # This method will be called in the receive-method while sending msg to channel-group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        # Send to the room in the frontend; send in a json-format
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    def disconnect(self, *args, **kwargs):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('Backend Consumer (Websocket): Disconnected!')


"""
[NB]: Create a routing file for the consumer, like urls for each views.
"""
