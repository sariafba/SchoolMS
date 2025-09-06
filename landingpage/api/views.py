from rest_framework.viewsets import ModelViewSet
from .serializers import *
from landingpage.models import Program
from landingpage.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from school.permissions import IsEmployee
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Student, Employee
from school.models import Event, Attendance
from accounting.models import Fee, Discount

from school.api.serializers import EventSerializer
from accounting.api.serializers import FeeSerializer, DiscountSerializer


class ProgramView(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminCooperatorPublicGET]

class ActivityView(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminCooperatorPublicGET]

class VisitDateView(ModelViewSet):
    queryset = VisitDate.objects.all()
    serializer_class = VisitDateSerializer
    permission_classes = [IsAdminCooperatorPublicGET]

class VisitView(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAdminCooperatorPublicPOST]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['visit_date']

class DashboardView(APIView):
    permission_classes = [IsEmployee]

    def get(self, request):
        today = timezone.now().date()

        data = {
            "total_students": Student.objects.count(),
            "total_employees": Employee.objects.count(),
            "latest_events": EventSerializer(Event.objects.order_by('-date')[:3], many=True).data,
            "today_attendance_count": Attendance.objects.filter(date=today).count(),
            "latest_fee": FeeSerializer(Fee.objects.order_by('-id').first()).data if Fee.objects.exists() else None,
            "latest_discount": DiscountSerializer(Discount.objects.order_by('-id').first()).data if Discount.objects.exists() else None,
        }

        return Response(data)
