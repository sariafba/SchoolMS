from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Notification



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if await self.is_student(user):
            self.group_name = f"student_{await self._get_student_id(user)}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

            # Send all unread notifications
            unread = await self.get_unread_notifications(user)
            for notif in unread:
                await self.send(text_data=json.dumps({
                    "type": notif["notification_type"],
                    "message": notif["message"],
                    # "created_at": notif["created_at"].isoformat(), 
                }, ensure_ascii=False))

            #Mark all notifications as read
            await self.mark_all_as_read(user)

        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self.scope["user"], "student"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": event["notification_type"],
            "message": event["message"],
            # "created_at": event["created_at"].isoformat()
        }, ensure_ascii=False))
        await self.mark_as_read(event["id"])

    @database_sync_to_async
    def is_student(self, user):
        return hasattr(user, 'student')
    
    @database_sync_to_async
    def _get_student_id(self, user):
        return user.student.id

    @database_sync_to_async
    def get_unread_notifications(self, user):
        return list(
            Notification.objects.filter(student=user.student, is_read=False)
            .values("notification_type", "message", "created_at")
        )
    
    @database_sync_to_async
    def mark_all_as_read(self, user):
        Notification.objects.filter(student=user.student, is_read=False).update(is_read=True)

    @database_sync_to_async
    def mark_as_read(self, notification_id):
        Notification.objects.filter(id=notification_id).update(is_read=True)