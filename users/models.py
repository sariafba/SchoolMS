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
    day_start = models.TimeField(null=True, blank=True)
    day_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='teacher')
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return self.employee.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    section = models.ForeignKey('school.Section', on_delete=models.CASCADE)
    card = models.OneToOneField('Card', on_delete=models.CASCADE)  # permanent student card
    religion = models.CharField(max_length=20, choices=[('islam', 'Islam'), ('christianity', 'Christianity'), ('other', 'Other')])
    parent1 = models.OneToOneField('Parent', on_delete=models.CASCADE, related_name='parent1')
    parent2 = models.OneToOneField('Parent', on_delete=models.CASCADE, related_name='parent2')

    def delete(self, *args, **kwargs):
        self.parent1.delete()
        self.parent2.delete()
        self.card.delete()
        super().delete(*args, **kwargs)

    RELIGION_CHOICES = [
        ('islam', 'Islam'),
        ('christianity', 'Christianity'),
        ('other', 'Other'),
    ]

class Parent(models.Model):
    job = models.CharField(max_length=100)
    card = models.OneToOneField('Card', on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.card.delete()
        super().delete(*args, **kwargs)

class Card(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    nationality = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = models.DateField()
    birth_city = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    place_of_register = models.CharField(max_length=100)
    national_no = models.CharField(max_length=100)

