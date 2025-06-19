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