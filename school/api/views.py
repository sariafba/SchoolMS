from rest_framework.viewsets import ModelViewSet
from .serializers import *
from school.models import *

class SubjectView(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StudyYearView(ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer

class StudyStageView(ModelViewSet):
    queryset = StudyStage.objects.all()
    serializer_class = StudyStageSerializer