from django.db import models
from django.utils import timezone
import os
from mimetypes import guess_type



class Post(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    text = models.TextField()
    is_public = models.BooleanField(default=True)
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
    
# class Comment(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    # text = models.TextField()
    # created_at = models.DateTimeField(default=timezone.now)
    # updated_at = models.DateTimeField(auto_now=True)