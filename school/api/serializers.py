from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from school.models import *




class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class StudyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = '__all__'

    def validate_name(self, value):
        # Check if the study year is valid e.g. 2020/2022 is wrong
        start, end = map(int, value.split('/'))
        if end != start + 1:
            raise serializers.ValidationError("End year must be exactly one year after the start year.")
        return value