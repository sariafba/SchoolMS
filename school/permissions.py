from rest_framework.permissions import BasePermission

class IsAdminCooperatorReceptionist(BasePermission):
    """
    Allow access for all if method GET 
    Allow access only to superuser or employees with role:
    - admin
    - receptionist
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
