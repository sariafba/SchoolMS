import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        # Reject connection if not authenticated
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close(code=4001)  # Custom close code for unauthorized
            return

        # Group name for all posts
        self.group_name = "all_posts"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def new_post(self, event):
        await self.send(text_data=json.dumps(event['post']))