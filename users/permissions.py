from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class EmployeePermission(BasePermission):

    allowed_roles = {
        'admin': ['cooperator', 'teacher', 'receptionist'],
        'cooperator': ['teacher', 'receptionist'],
        'teacher': [],
        'receptionist': [],
    }

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if not hasattr(request.user, 'employee'):
            return False

        employee_role = request.user.employee.role

        if employee_role in ['teacher', 'receptionist']:
            return False
        
        if request.method == 'GET':
            return True

        if request.method == 'POST':
            input_role = request.data.get('role')

            if not input_role or input_role not in self.allowed_roles:
                return True # serializer will validate

            if input_role in self.allowed_roles.get(employee_role, []):
                return True
            else:
                raise PermissionDenied(f"You are not allowed to assign role '{input_role}'.")

        # Allow PATCH/DELETE conditionally via has_object_permission
        if request.method in ['PATCH', 'DELETE']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.method == 'GET':
            return True
        
        employee_role = request.user.employee.role
        allowed_roles = self.allowed_roles.get(employee_role, [])
        target_role = obj.role

        if request.method == 'DELETE':
            if target_role in allowed_roles:
                return True
            raise PermissionDenied(
                f"You are not allowed to delete an employee with role '{target_role}'."
            )

        if request.method == 'PATCH':

            # Also make sure the original role was allowed to be edited
            if target_role not in allowed_roles:
                raise PermissionDenied(
                    f"You are not allowed to modify an employee with role '{target_role}'."
                )
            
            new_role = request.data.get('role')

            # If no role is changing or role stays the same, allow
            if not new_role or new_role not in self.allowed_roles:
                return True # serializer will validate

            # If trying to change to an unassignable role
            if new_role not in allowed_roles:
                raise PermissionDenied(
                    f"You are not allowed to change role to '{new_role}'."
                )
            return True
        
class IsAdminCooperatorReceptionistTeacher(BasePermission):

    def has_permission(self, request, view):        
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and employee.role in ['admin', 'cooperator', 'receptionist', 'teacher']:
            return True

        return False        