from django.contrib.auth.models import AbstractUser
from django.db import models
from school.models import Subject


class User(AbstractUser):
    phone = models.CharField(max_length=13, unique=True, blank=True, null=True)


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

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
