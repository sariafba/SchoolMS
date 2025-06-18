from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from .serializers import *
from school.models import *

class SubjectView(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
