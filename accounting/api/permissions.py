from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReceptionistPermission(BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        
        if hasattr(request.user, 'employee') and request.user.employee.role == 'receptionist':
            return True

        return False
    

class AccountingPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Reception عنده كل الصلاحيات
        if hasattr(user, "employee") and user.employee.role == "receptionist":
            return True

        # الطالب يقدر يستخدم GET, HEAD, OPTIONS فقط
        if hasattr(user, "student") and request.method in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Reception عنده صلاحية كاملة
        if hasattr(user, "employee") and user.employee.role == "receptionist":
            return True

        # الطالب يقدر يشوف بياناته فقط
        if hasattr(user, "student") and request.method in SAFE_METHODS:
            # إذا الـ obj له علاقة بالطالب نفسه
            if hasattr(obj, "student"):
                return obj.student == user.student

        return False

    