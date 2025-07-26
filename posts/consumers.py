import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async



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

    @database_sync_to_async
    def _get_student_section_id(self, user):
        if not hasattr(user, 'student'):
            return None        
        return user.student.section.id

    @database_sync_to_async
    def _is_employee(self):
        return hasattr(self.scope['user'], 'employee')

    async def new_post(self, event):
        post = event['post']
        user = self.scope['user']

        # Public posts go to everyone in this group
        if post.get('is_public') or self._is_employee():
            await self.send(text_data=json.dumps(post))
            return

        # Private posts → check student’s section
        section_id = await self._get_student_section_id(user)
        # raise Exception(post.get('sections', []))
        if section_id and any(section['id'] == section_id for section in post.get('sections', [])):
                await self.send(text_data=json.dumps(post))