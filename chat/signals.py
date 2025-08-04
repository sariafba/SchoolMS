from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Student
from .models import ChatRoom
from  users.models import Employee

@receiver(post_save, sender=Student)
def create_student_room(sender, instance, created, **kwargs):
    if created:
        room = ChatRoom.objects.create(student=instance)

        employees = Employee.objects.filter(role__in=['admin', 'cooperator', 'teacher'])
        room.employees.set(employees)