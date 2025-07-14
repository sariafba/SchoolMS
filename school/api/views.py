from rest_framework.viewsets import ModelViewSet
from .serializers import *
from school.models import *
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


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

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sections', 'sections__grade',]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Double-check permission (redundant but safe)
        if not request.user == instance.user:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)