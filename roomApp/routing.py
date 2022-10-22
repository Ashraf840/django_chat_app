from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi()),
]

"""
[NB]: Modify the "chatSystem/asgi.py" file.
"""
