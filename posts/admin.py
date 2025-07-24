from django.contrib import admin
from .models import Post, Attachment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__username', 'text', 'created_at', 'updated_at']
    ordering = ['id']

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'file', 'file_type']