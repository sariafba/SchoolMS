from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path('posts/', consumers.PostConsumer.as_asgi())
]