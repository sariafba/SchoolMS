from rest_framework.permissions import BasePermission

class IsAdminCooperatorPublicGET(BasePermission):
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
        if employee and employee.role in ['admin', 'cooperator']:
            return True

        return False
    
class IsAdminCooperatorPublicPOST(BasePermission):


    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and employee.role in ['admin', 'cooperator']:
            return True

        return False