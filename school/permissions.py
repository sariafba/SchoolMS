from rest_framework.permissions import BasePermission

class IsAdminCooperatorReceptionist(BasePermission):

    def has_permission(self, request, view):        
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and employee.role in ['admin', 'cooperator', 'receptionist']:
            return True

        return False

class IsAdminCooperator(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and employee.role in ['admin', 'cooperator']:
            return True

        return False
    
class IsEmployee(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee:
            return True

        return False

class PlacementDatePermission(BasePermission):
    """
    Allow access for all if method GET 
    Allow access only to superuser or employees with role:
    - admin
    - receptionist
    - cooperator
    """

    def has_permission(self, request, view):
        # Allow any GET request
        if request.method == 'GET':
            return True
        
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and employee.role in ['admin', 'cooperator', 'receptionist']:
            return True

        return False
    
class AttendancePermission(BasePermission):

    def has_permission(self, request, view):
       
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True
        
        if request.method in ['put', 'patch', 'delete']:
            return False

        if hasattr(request.user, 'student') and request.method == 'post':
            return False
        
        if hasattr(request.user, 'employee'):
            if request.user.employee.role in ['admin', 'cooperator']:
                return True
             
        return True

from rest_framework.permissions import BasePermission, SAFE_METHODS

class EventPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if hasattr(user, "employee"): 
            if request.user.employee.role in ['admin', 'cooperator', 'teacher']:
             return True

        if hasattr(user, "student") and request.method in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(user, "employee"): 
            if request.user.employee.role in ['admin', 'cooperator', 'teacher']:
                return True

        if hasattr(user, "student") and request.method in SAFE_METHODS:
            return obj.student == user.student

        return False

class MarkPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        # Admin: read-only
        if hasattr(user, "employee") and user.employee.role == "admin":
            return request.method in SAFE_METHODS

        # Cooperator: full access
        if hasattr(user, "employee") and user.employee.role == "cooperator":
            return True

        # Teacher: full access (object-level will restrict subjects)
        if hasattr(user, "employee") and user.employee.role == "teacher":
            return True

        # Student: read-only
        if hasattr(user, "student"):
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin: read-only
        if hasattr(user, "employee") and user.employee.role == "admin":
            return request.method in SAFE_METHODS

        # Cooperator: full access
        if hasattr(user, "employee") and user.employee.role == "cooperator":
            return True

        # Teacher: only if subject in teacher's subjects
        if hasattr(user, "employee") and user.employee.role == "teacher":
            teacher = user.employee.teacher
            return obj.subject in teacher.subjects.all()

        # Student: only their own marks (read-only)
        if hasattr(user, "student") and request.method in SAFE_METHODS:
            return obj.student == user.student

        return False

