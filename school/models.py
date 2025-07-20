from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import os
from mimetypes import guess_type

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

class StudyYear(models.Model):
    name = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}/\d{4}$',
                message='Format must be YYYY/YYYY (e.g., 2020/2021)'
            )
        ]
    )

    def __str__(self):
        return self.name

class StudyStage(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=100)
    study_stage = models.ForeignKey(StudyStage, on_delete=models.CASCADE)
    study_year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'study_year'], name='unique_grade_name_per_study_year')
        ]

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'grade'], name='unique_section_name_per_grade')
        ]

class Schedule(models.Model):
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    # class Meta:
    #     unique_together = ['teacher', 'day', 'start_time']

class Post(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    sections = models.ManyToManyField('school.Section', related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at}"
    
"""Attachments"""                                                                        
def attachment_upload_to(instance, filename):
    """Generate upload path for attachments: attachments/user_id/timestamp/filename"""
    return os.path.join(
        'post-attachments',
        str(instance.post.user.id),
        str(int(timezone.now().timestamp())),
        filename
    )
class Attachment(models.Model):    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=attachment_upload_to)
    file_type = models.CharField(max_length=10, choices=(
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
    ), blank=True)

    def save(self, *args, **kwargs):
        """Auto-detect file type before saving"""
        if not self.file_type and self.file:
            self.detect_file_type()
        super().save(*args, **kwargs)

    def detect_file_type(self):
        """Determine file type based on extension"""
        mime_type, _ = guess_type(self.file.name)
        if mime_type:
            if mime_type.startswith('image/'):
                self.file_type = 'image'
            elif mime_type.startswith('video/'):
                self.file_type = 'video'
            else:
                self.file_type = 'file'
        else:
            self.file_type = 'file'
    
    def __str__(self):
        return f"{self.file_type} attachment for post {self.post.id}"

class PlacementDate(models.Model):
    date = models.DateTimeField()
    