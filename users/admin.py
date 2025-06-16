from django.contrib import admin

from .models import User, Role, Employee, Teacher

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'phone', 'first_name', 'last_name']
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__username', 'salary', 'contract_start', 'contract_end', 'day_start', 'day_end']
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee__user__username']