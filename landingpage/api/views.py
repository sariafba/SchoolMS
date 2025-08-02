from rest_framework.viewsets import ModelViewSet
from .serializers import *
from landingpage.models import Program
from landingpage.permissions import *
from django_filters.rest_framework import DjangoFilterBackend

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
