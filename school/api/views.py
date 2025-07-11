from rest_framework.viewsets import ModelViewSet
from .serializers import *
from school.models import *
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter



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

