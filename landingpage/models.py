from django.db import models
from django.utils import timezone
import os

def upload_to(instance, filename):
    return os.path.join(
        'landingpage',
        str(int(timezone.now().timestamp())),
        filename
    )

class Program(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to)
    details = models.CharField(max_length=100, blank=True, null=True)

class Activity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to)
    videos = models.ManyToManyField('Video', related_name='activities')
    details = models.CharField(max_length=100, blank=True, null=True)

class Video(models.Model):
    video = models.FileField(upload_to=upload_to)

class VisitDate(models.Model):
    date = models.DateTimeField()

class Visit(models.Model):
    visit_date = models.ForeignKey(VisitDate, on_delete=models.CASCADE, related_name='visits')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)