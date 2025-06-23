# views.py
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Employee, Role
from .serializers import EmployeeSerializer, RoleSerializer



class EmployeeView(ModelViewSet):

    # permission_classes = [IsAdminUser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']


class RoleView(ReadOnlyModelViewSet):

    # permission_classes=[IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
        

    