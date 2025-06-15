from django.contrib import admin

from .models import User, Role, Employee

# Register your models here.
# admin.site.register(User)
# admin.site.register(Role)
# admin.site.register(Employee)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name','phone']
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user_id','salary','contract_start','contract_end','day_start','day_end']
