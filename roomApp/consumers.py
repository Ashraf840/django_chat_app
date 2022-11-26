import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Message, Room, UserOnline, UserConnectedChannels
from django.contrib.auth.models import User

# Following my university-final-proj + The YT Video
# Instead of using AsyncWebsocketConsumer, using only WebsocketConsumer


# [Static Method] Used to create multiple user channels; Used in 'current_user_existence()'
def create_channel_conn(userOnlineObj, channelName):
    channelName = channelName.replace('specific.', '')  # remove prefix from each channel-name; mitigate db-storage
    UserConnectedChannels.objects.create(
        user_online=userOnlineObj,
        channel_value=channelName
    )


# [Static Method] Used to remove same users multiple connected channels; Used in 'deactive_user_online_conn_db()'
def remove_channel_conn(userOnlineObj, channelName):
    try:
        channelName = channelName.replace('specific.', '')
        UserConnectedChannels.objects.get(
            user_online=userOnlineObj,
            channel_value=channelName
        ).delete()
    except UserConnectedChannels.DoesNotExist:
        print("No such active channel exists!")


# [Static Method] Return all the active users of current room
def existing_users(room):
    room_obj = Room.objects.get(slug=room)
    # room_obj = Room.objects.get(slug=self.room_name)
    print(f"Room obj (from 'existing_users()' func): {room_obj}")
    users_obj = UserOnline.objects.filter(room=room_obj, is_active=True)
    print(f"Existing active users (from 'existing_users()' func): {users_obj}")
    return users_obj


# [Static Method] Used in 'current_user_existence()'
def make_user_online(user):
    # Check if the user's online; otherwise change it to True
    if not user.is_active:
        print("User wasn't active until now!")
        user.is_active = True
        user.save()


# [Static Method] Used in 'deactive_user_online_conn_db()'
def make_user_offline(user):
    # Check if the user's offline; otherwise change it to False
    if user.is_active:
        print("User was active until now!")
        user.is_active = False
        user.save()


# [Static Method] Check currently connected user does exist in db "UserOnline" table; otherwise create record
def current_user_existence(user, room, channelName):
    user_obj = User.objects.get(id=user.id)
    room_obj = Room.objects.get(slug=room)
    # print(f'Channel Name from current_user_existence(): {channelName}')
    try:
        user_online_obj = UserOnline.objects.get(user=user_obj, room=room_obj)
        print("Try-block; User exists! from 'current_user_existence()' func!")
        # Check if the user's online; otherwise change it to True
        make_user_online(user=user_online_obj)
        # Create multiple channels for same user; since multiple channels for the same user is not constrained.
        create_channel_conn(userOnlineObj=user_online_obj, channelName=channelName)
    except UserOnline.DoesNotExist:
        print("Except-block; User doesn't exist! from 'current_user_existence()' func!")
        # Create user online record
        user_online_obj = UserOnline.objects.create(user=user_obj, room=room_obj)
        create_channel_conn(userOnlineObj=user_online_obj, channelName=channelName)


# [Static Method] Count total connected channels of a user in the db
def count_active_channels(user_online_obj):
    # [Mitigating bug: Same user opening multiple duplicate tabs of the same chat room;
    # then closing them make the user offline to other users of the channels
    # as well as his/her own other duplicate tabs.]
    user_activated_channels = UserConnectedChannels.objects.filter(user_online=user_online_obj)
    print(f'Active channels: {user_activated_channels}')
    print(f'Active channels queryset-length: {len(user_activated_channels)}')
    return user_activated_channels


# Change existing user online status to offline
# MIRROR METHOD of "current_user_existence"; Require REFACTOR TO MAKE THE CODE DRY;
# (NB: put a logic for routing these functions into a single function.)
def deactive_user_online_conn_db(user, room, channelName):
    user_obj = User.objects.get(id=user.id)
    room_obj = Room.objects.get(slug=room)
    try:
        user_online_obj = UserOnline.objects.get(user=user_obj, room=room_obj)
        # Remove active user channels from db
        remove_channel_conn(userOnlineObj=user_online_obj, channelName=channelName)
        # Check how many active channels exist in the db for a specific user before making the user offline.
        user_activated_channels = count_active_channels(user_online_obj=user_online_obj)
        # Make the user offline only if the filter-queryset of that users active_channels is empty
        if len(user_activated_channels) == 0:
            # Check if the user's offline; otherwise change it to False
            make_user_offline(user=user_online_obj)
    except UserOnline.DoesNotExist:
        print("User doesn't exist to make status offline!")


# [Static Method]: Store chat msg into DB
def save_message(message, username, room):
    user = User.objects.get(username=username)
    room = Room.objects.get(slug=room)
    Message.objects.create(room=room, user=user, content=message)


# Consumer Class
class ChatConsumer(WebsocketConsumer):
    # Constructor / Initializer
    def __init__(self, *args, **kwargs):
        super(ChatConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user_obj = None

    # Default method of "WebsocketConsumer" class
    # Create an asynchronous connection-function
    def connect(self):
        # fetch the room-name from the request that's being hit from the frontend-page-load through the asgi-request-routing
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_obj = self.scope['user']
        print(f"Newly Connected (username): {self.user_obj.username}")
        # print(f"Scope['user']: {self.user_obj}")
        # print(f'Room name: {self.room_name}')
        # print(f'Room group name: {self.room_group_name}')
        print(f'Channel name: {self.channel_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # channels automatically fixes room-name?
        )
        print('Backend Consumer (Websocket): Connected!')

        async_to_sync(self.accept())

        # Get all the ACTIVE USERS OF THE CURRENT ROOM by asynchronously querying the db
        active_users = async_to_sync(existing_users(room=self.room_name))
        # print(dir(active_users))  # Checking the "AsyncToSync" object
        # print("Active users (queried from the db):", active_users.__dict__)
        print("Active users (queried from the db):", list(active_users.awaitable))
        user_names = [u.user.username for u in list(active_users.awaitable) if u.user.username != self.user_obj.username]    # Ignore the current user's username by adding a condition into this list-comprehension
        print(f"Active users (usernames only; except current user's username): {user_names}")

        # Send the query object only to the newly connected user's web-socket; NOT TO ALL THE CHANNELS OF THIS GROUP (Room)
        self.send(text_data=json.dumps({
            'existing_users_list': 'Existing Users List in the Room',
            'user_names': user_names,
        }))

        # Check if the user already exist, check if the user already has "is_active=True", otherwise change that to "True".
        # If the user doesn't exist, add newly connected user into the DB.
        async_to_sync(current_user_existence(user=self.user_obj, room=self.room_name, channelName=self.channel_name))

        # Group send about active users (Including newly connected)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            # pass a dictionary with custom key-value pairs
            {
                'type': 'active_users',
                'user_conn_status_msg': f'New user connected: {self.user_obj.username}',
                'user_name': self.user_obj.username,
            }
        )

    # Default method of "WebsocketConsumer" class
    # Receive the msg from frontend & broadcast it to the entire channel
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)  # decode json-stringified data into python-dict
        # print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        # before sending the msg to the channel-group, store the msg into db
        async_to_sync(save_message(
            room=room,
            username=username,
            message=message
        ))

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

    # This method will be called in the receive-method while sending msg to channel-group.
    # [Sends to own Websocket; also used while sending into group channel] "event" param contains other keys (except 'type' key) from inside the dictionary passed as param in "channel_layer.group_send"
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        # Send to the room in the frontend; send in a json-format; send func responsible for sending data to frontend
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    # [Sends to own Websocket; also used while sending into group channel] Passing data to websocket (new user connection; this method is used to send msg into the group)
    def active_users(self, event):
        user_conn_msg = event['user_conn_status_msg']
        active_username = event['user_name']
        self.send(text_data=json.dumps({
            'user_conn_msg': user_conn_msg,
            'active_username': active_username,
        }))

    # [Sends to own Websocket; also used while sending into group channel] Passing data to websocket (existing user disconnection; this method is used to send msg into the group)
    def deactive_user(self, event):
        user_disconn_msg = event['user_conn_status_msg']
        deactive_username = event['user_name']

        self.send(text_data=json.dumps({
            'user_disconn_msg': user_disconn_msg,
            'deactive_username': deactive_username,
        }))

    # Default method of "WebsocketConsumer" class
    def disconnect(self, *args, **kwargs):
        # Change the "is_active" status of the exiting user
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_obj = self.scope['user']
        # print(f"Room: {self.room_name};  User: {self.user_obj}")
        # print(f'Channel name (from "disconnect()" func): {self.channel_name}')

        async_to_sync(deactive_user_online_conn_db(user=self.user_obj, room=self.room_name, channelName=self.channel_name))

        # [start/hits in the frontend of own+other connected users' browser]
        # if-condition: check if no channel connected to the User/UserOnline
        user_obj = User.objects.get(id=self.user_obj.id)
        room_obj = Room.objects.get(slug=self.room_name)
        user_online_obj = UserOnline.objects.get(user=user_obj, room=room_obj)
        # Check how many active channels exist in the db for a specific user before making the user offline.
        user_activated_channels = count_active_channels(user_online_obj=user_online_obj)
        # Make the user offline only if the filter-queryset of that users active_channels is empty
        if len(user_activated_channels) == 0:
            # Group send about disconnecting users
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                # pass a dictionary with custom key-value pairs
                {
                    'type': 'deactive_user',
                    'user_conn_status_msg': f'User disconnected: {self.user_obj.username}',
                    'user_name': self.user_obj.username,
                }
            )

            # Remove the currently attempted user-channel from the Channel Group (Room)
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        # [end] if-condition: check if no channel connected to the User/UserOnline
        print('Backend Consumer (Websocket): Disconnected!')


"""
[NB]: Create a routing file for the consumer, like urls for each views.
"""
