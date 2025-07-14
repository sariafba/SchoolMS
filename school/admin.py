from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']

@admin.register(StudyYear)
class StudyYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']

@admin.register(StudyStage)
class StudyStageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'study_stage', 'study_year']
    ordering = ['id']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade']
    ordering = ['id']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'section__name', 'day', 'start_time', 'end_time']
    ordering = ['id']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__username', 'text', 'created_at', 'updated_at']
    ordering = ['id']

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'file', 'file_type']