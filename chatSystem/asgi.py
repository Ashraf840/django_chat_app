"""
ASGI config for chatSystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatSystem.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
# Import the routing file(s)
import roomApp.routing

# application = get_asgi_application()

"""
If you are here due to error while trying to run daphne on server then here is the answer for you.
[STackoverflow Ref]: https://stackoverflow.com/a/67636724
"""

application = ProtocolTypeRouter(
    {
        # Just HTTP for now. (We can add other protocols later.)
        # "http": get_asgi_application(),
        "http": django_asgi_app,     # TESTING
        'websocket': AuthMiddlewareStack(
            URLRouter(
                roomApp.routing.websocket_urlpatterns,
            ),
        ),
    }
)

