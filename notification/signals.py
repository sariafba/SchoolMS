from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from school.models import Attendance, Mark, Event 

def send_ws_notification(student_id, notification_id, message, notif_type):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"student_{student_id}",
        {
            "type": "send_notification",
            
            "id": notification_id,
            "message": message,
            "notification_type": notif_type,
        },
    )

@receiver(post_save, sender=Attendance)
def attendance_created(sender, instance, created, **kwargs):
    if created:
        message = f"Attendance recorded for {instance.date}"
        notification = Notification.objects.create(student=instance.student, message=message, notification_type="attendance")
        send_ws_notification(instance.student.id, notification.id, message, "attendance")

@receiver(post_save, sender=Mark)
def mark_created(sender, instance, created, **kwargs):
    if created:
        message = f"New mark in {instance.subject.name}: {instance.mark}"
        notification = Notification.objects.create(student=instance.student, message=message, notification_type="mark")
        send_ws_notification(instance.student.id, notification.id, message, "mark")

@receiver(m2m_changed, sender=Event.students.through)
def event_students_added(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for student_id in pk_set:
            message = f"New event: {instance.title}"
            notification = Notification.objects.create(student_id=student_id, message=message, notification_type="event")
            send_ws_notification(student_id, notification.id, message, "event")
