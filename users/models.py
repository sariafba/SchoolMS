from django.contrib.auth.models import AbstractUser
from django.db import models
from school.models import Subject


class User(AbstractUser):
    phone = models.CharField(max_length=13, unique=True, blank=True, null=True)

class Employee(models.Model):
                
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('cooperator', 'Cooperator'),
        ('teacher', 'Teacher'),
        ('receptionist', 'Receptionist',),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    salary = models.DecimalField(max_digits=10, decimal_places=2)
    contract_start = models.DateField()
    contract_end = models.DateField()
    day_start = models.TimeField()
    day_end = models.TimeField()

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='teacher')
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return self.employee.user.username
