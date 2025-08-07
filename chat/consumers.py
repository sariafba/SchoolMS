import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        self.user = self.scope['user']

        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)
            return

        # Check if the user belongs to the room
        is_member = await self.user_belongs_to_room(self.room_id, self.user)

        if not is_member:
            await self.close(code=4003)  # Forbidden
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id

        msg = await self.save_message(self.room_id, sender_id, message)
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                'sender': msg.sender.username,
                'created_at': str(msg.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'created_at': event['created_at'],
        }, ensure_ascii=False))

    @database_sync_to_async
    def save_message(self, room_id, sender_id, content):
        sender = User.objects.get(id=sender_id)
        room = ChatRoom.objects.get(id=room_id)
        return Message.objects.create(room=room, sender=sender, content=content)

    @database_sync_to_async
    def user_belongs_to_room(self, room_id, user):
        try:
            room = ChatRoom.objects.get(id=room_id)
            if hasattr(user, 'student') and room.student == user.student:
                return True
            if hasattr(user, 'employee') and room.employees.filter(id=user.employee.id).exists():
                return True
        except ChatRoom.DoesNotExist:
            return False
        return False
    


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        self.user = self.scope['user']

        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)
            return

        # Check if the user belongs to the room
        is_member = await self.user_belongs_to_room(self.room_id, self.user)
        if not is_member:
            await self.close(code=4003)  # Forbidden
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id

        msg = await self.save_message(self.room_id, sender_id, message)        
        sender_full_name = await self.get_sender_full_name(msg.sender) 

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                # 'sender': msg.sender.username,
                'sender': sender_full_name,
                'created_at': str(msg.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'created_at': event['created_at'],
        }, ensure_ascii=False))

    @database_sync_to_async
    def save_message(self, room_id, sender_id, content):
        sender = User.objects.get(id=sender_id)
        room = GroupRoom.objects.get(id=room_id)
        return GroupMessage.objects.create(room=room, sender=sender, content=content)

    @database_sync_to_async
    def user_belongs_to_room(self, room_id, user):
            try:
                room = GroupRoom.objects.get(id=room_id)
                if hasattr(user, 'student') and room.students.filter(id=user.student.id).exists():
                    return True
                if hasattr(user, 'employee') and room.employees.filter(id=user.employee.id).exists():
                    return True
            except ChatRoom.DoesNotExist:
                return False
            return False

    @database_sync_to_async
    def get_sender_full_name(self, sender):
        if hasattr(sender, 'employee'):
            return f"{sender.employee.user.first_name} {sender.employee.user.last_name}"
        else:
            return f"{sender.student.card.first_name} {sender.student.card.last_name}"
