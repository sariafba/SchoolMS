# views.py
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from users.models import Employee, Role
from .serializers import EmployeeSerializer, RoleSerializer, RoleQuerySerializer


class EmployeeView(APIView):

    # permission_classes=[IsAdminUser]

    def get(self, request, pk=None):

        # Validate query params
        query_serializer = RoleQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        role_name = query_serializer.validated_data.get('role_name')

        # Build dynamic filter
        filters = {}
        if pk:
            filters['pk'] = pk
        if role_name:
            filters['role__name'] = role_name

        # Single object or list
        queryset = Employee.objects.filter(**filters)

        if pk:
            employee = get_object_or_404(queryset)
            serializer = EmployeeSerializer(employee)
        else:
            serializer = EmployeeSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            employee = serializer.save()
            return Response({
                "message": "Employee created successfully",
                "employee": EmployeeSerializer(employee).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Employee updated successfully", "employee": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.user.delete()  # delete user and cascade to employee
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RoleView(ReadOnlyModelViewSet):

    # permission_classes=[IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
        

    