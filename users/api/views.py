# views.py
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Employee, Student
from .serializers import EmployeeSerializer, StudentSerializer, CreateStudentSerializer
from users.permissions import *
from rest_framework.response import Response
from rest_framework import status
from school.permissions import IsAdminCooperatorReceptionist
from rest_framework.generics import CreateAPIView


class EmployeeView(ModelViewSet):

    permission_classes = [EmployeePermission]
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']

    def get_queryset(self):

        allowed_roles = {
            'admin': ['cooperator', 'teacher', 'receptionist'],
            'cooperator': ['teacher', 'receptionist'],
            'teacher': [],
            'receptionist': [],
        
        }
        if self.request.user.is_superuser:
            return self.queryset
        
        employee_role = self.request.user.employee.role
        allowed_roles = allowed_roles.get(employee_role, [])
        return self.queryset.filter(role__in=allowed_roles)

    def destroy(self, request, *args, **kwargs):
        self.get_object().user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section', 'section__grade']

    permission_classes = [IsAdminCooperatorReceptionistTeacher]
    
class CreateStudentView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer

    permission_classes = [IsAdminCooperatorReceptionist]

    