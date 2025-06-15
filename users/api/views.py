# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Employee, Role as R
from .serializers import CooperatorSerializer,RoleSerializer
from django.shortcuts import get_object_or_404


class Cooperator(APIView):
    def get(self, request, pk=None):
        if pk:
            employee = get_object_or_404(Employee, pk=pk, role__name="cooperator")
            serializer = CooperatorSerializer(employee)
            return Response(serializer.data)
        else:
            employees = Employee.objects.filter(role__name="cooperator")
            serializer = CooperatorSerializer(employees, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CooperatorSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response({
                "message": "Cooperator created successfully",
                "cooperator": CooperatorSerializer(employee).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk, role__name="cooperator")
        serializer = CooperatorSerializer(employee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cooperator updated successfully", "cooperator": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk, role__name="cooperator")
        employee.user.delete()  # delete user and cascade to employee
        return Response({"message": "Cooperator deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class Role(APIView):
    def get(self, request, pk=None):

        if pk:
            role = get_object_or_404(R, pk=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        else:
            roles = R.objects.all()
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data)