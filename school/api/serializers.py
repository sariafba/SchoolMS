from rest_framework import serializers
from school.models import *
from users.models import Teacher
from users.models import Employee

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

class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'username', 'subjects']

    def get_username(self, obj):
        return obj.employee.user.username
    
    def get_subjects(self, obj):
        return SubjectSerializer(obj.subjects.all(), many=True).data

class ScheduleSerializer(serializers.ModelSerializer):

    teacher = EmployeeSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), write_only=True, source='teacher')

    section = SectionSerializer(read_only=True)
    section_id = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), write_only=True, source='section')

    class Meta:
        model = Schedule
        fields = ['id', 'day', 'start_time', 'end_time', 'teacher', 'teacher_id', 'section', 'section_id']

    def validate(self, data):
        instance = self.instance

        teacher = data.get('teacher', getattr(instance, 'teacher', None))
        section = data.get('section', getattr(instance, 'section', None))
        start_time = data.get('start_time', getattr(instance, 'start_time', None))
        end_time = data.get('end_time', getattr(instance, 'end_time', None))
        day = data.get('day', getattr(instance, 'day', None))

        if not all([teacher, section, start_time, end_time, day]):
            raise serializers.ValidationError("Missing required fields for validation.")

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        teacher_conflicts = Schedule.objects.filter(
            teacher=teacher,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        section_conflicts = Schedule.objects.filter(
            section=section,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )

        if instance:
            teacher_conflicts = teacher_conflicts.exclude(id=instance.id)
            section_conflicts = section_conflicts.exclude(id=instance.id)

        if teacher_conflicts.exists():
            raise serializers.ValidationError("Teacher is already scheduled during this time.")

        if section_conflicts.exists():
            raise serializers.ValidationError("This section already has a teacher scheduled during this time.")

        return data





