from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'phone', 'first_name', 'last_name']
    ordering = ['id']
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__username', 'role', 'salary', 'user__phone', 'contract_start', 'contract_end', 'day_start', 'day_end']
    ordering = ['id']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee__user__username', 'get_subjects']
    ordering = ['id']

    def get_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
    get_subjects.short_description = 'Subjects'

@admin.register(Card)
class Card(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'nationality', 'gender', 'birth_date', 'birth_city', 'address', 'place_of_register', 'national_no']
    ordering = ['id']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','user__username', 'section__grade__name', 'section__name', 'register_date']
    ordering = ['id']