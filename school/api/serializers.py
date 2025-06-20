from rest_framework import serializers
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
    

class StudyStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyStage
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    
    study_stage = StudyStageSerializer(read_only=True)
    study_stage_id = serializers.PrimaryKeyRelatedField(
        queryset=StudyStage.objects.all(),
          write_only=True,
            source='study_stage'
    )

    study_year = StudyYearSerializer(read_only=True)
    study_year_id = serializers.PrimaryKeyRelatedField(
        queryset=StudyYear.objects.all(),
          write_only=True,
            source='study_year'
    )
    
    class Meta:
        model = Grade
        fields = ['id', 'name', 'study_stage_id', 'study_stage', 'study_year_id', 'study_year']


class SectionSerializer(serializers.ModelSerializer):
    
    grade = GradeSerializer(read_only=True)
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(), write_only=True, source='grade'
    )

    class Meta:
        model = Section
        fields = ['id', 'name', 'grade_id', 'grade']





