from rest_framework.permissions import BasePermission

class IsSuperAdminAdminReceptionist(BasePermission):
    """
    Allow access only to superuser or employees with role:
    - admin
    - receptionist
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and employee.role in ['admin', 'receptionist']:
            return True

        return False
