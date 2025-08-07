from django.db import models
from django.contrib.auth import get_user_model
from users.models import Student, Employee
User = get_user_model()


class ChatRoom(models.Model):
    """
    One room per student; all employees in the school participate.
    """
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='chat_room'
    )
    employees = models.ManyToManyField(
        Employee,
        related_name='chat_rooms'
    )

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
    
class GroupRoom(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Employee, related_name='group_owner', on_delete=models.CASCADE)
    students = models.ManyToManyField(
        Student,
        related_name='group_room'
    )
    employees = models.ManyToManyField(
        Employee,
        related_name='group_rooms'
    )

class GroupMessage(models.Model):
    room = models.ForeignKey(GroupRoom, related_name='group_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_group_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"