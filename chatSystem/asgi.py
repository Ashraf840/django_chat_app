"""
ASGI config for chatSystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Import the routing file(s)
import roomApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatSystem.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # Just HTTP for now. (We can add other protocols later.)
        "http": get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                roomApp.routing.websocket_urlpatterns,
            ),
        ),
    }
)

