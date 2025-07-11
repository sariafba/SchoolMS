from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'phone', 'first_name', 'last_name']
    ordering = ['id']
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__username', 'role', 'salary', 'contract_start', 'contract_end', 'day_start', 'day_end']
    ordering = ['id']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee__user__username', 'get_subjects']
    ordering = ['id']

    def get_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
    get_subjects.short_description = 'Subjects'
