"""
ASGI config for schoolms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django

# Set default settings module BEFORE importing anything that might use settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolms.settings')
django.setup()  # Initialize Django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels_auth_token_middlewares.middleware import (
    SimpleJWTAuthTokenMiddleware,
    QueryStringSimpleJWTAuthTokenMiddleware,
)
import posts.routing as PostRouter
import chat.routing as ChatRouter
import notification.routing as NotificationRouter

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryStringSimpleJWTAuthTokenMiddleware(  # Outer: gets token from query
        SimpleJWTAuthTokenMiddleware(  # Inner: validates JWT
            URLRouter(
                PostRouter.websocket_urlpatterns +
                ChatRouter.websocket_urlpatterns +
                NotificationRouter.websocket_urlpatterns
            )
        )
    ),
})
