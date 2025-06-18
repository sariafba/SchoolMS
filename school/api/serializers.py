from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from school.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'