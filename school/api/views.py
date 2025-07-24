from rest_framework.viewsets import ModelViewSet
from .serializers import *
from school.models import *
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter
from school.permissions import IsSuperAdminAdminReceptionist
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

class SubjectView(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StudyYearView(ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer

class StudyStageView(ModelViewSet):
    queryset = StudyStage.objects.all()
    serializer_class = StudyStageSerializer

class GradeView(ModelViewSet):
    queryset = Grade.objects.select_related('study_stage', 'study_year').all()
    serializer_class = GradeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'study_stage',
        'study_year',
        # 'study_stage__name': ['exact', 'icontains'],
        # 'study_year__name': ['exact'],
          ]
    # filter_backends = [SearchFilter]
    # search_fields = ['name']

class SectionView(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grade']

class ScheduleView(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'section', 'day']
    
class PlacementDateView(ModelViewSet):
    queryset = PlacementDate.objects.all()
    serializer_class = PlacementDateSerializer
    permission_classes = [IsSuperAdminAdminReceptionist]

    def get_queryset(self):
        queryset = PlacementDate.objects.all()
        future_param = self.request.query_params.get('future')

        if future_param and future_param.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(date__gt=timezone.now())

        return queryset

class PlacementView(ModelViewSet):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer
    permission_classes = [IsAuthenticated]