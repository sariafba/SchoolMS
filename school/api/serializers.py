from rest_framework import serializers
from school.models import *
from users.models import Teacher, Employee, Card



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

class PlacementDateSerializer(serializers.ModelSerializer):

    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PlacementDate
        fields = ['id', 'date', 'limit', 'day_name']

    def get_day_name(self, obj):
        return obj.date.strftime('%A')
    
class CardNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'first_name',
            'last_name',
            'phone',
            'nationality',
            'gender',
            'birth_date',
            'birth_city',
            'address',
            'place_of_register',
            'national_no',
        ]

class PlacementSerializer(serializers.ModelSerializer):
    # nested card serializers
    student_card = CardNestedSerializer()
    parent1_card = CardNestedSerializer()
    parent2_card = CardNestedSerializer()

    class Meta:
        model = Placement
        fields = [
            'id',
            'placement_date',
            'placement_result',

            'student_religion',
            'student_card',

            'parent1_job',
            'parent1_card',

            'parent2_job',
            'parent2_card'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # Pop out nested card data
        student_card_data    = validated_data.pop('student_card')
        parent1_card_data      = validated_data.pop('parent1_card')
        parent2_card_data      = validated_data.pop('parent2_card')

        # Create Card instances
        student_card_obj   = Card.objects.create(**student_card_data)
        parent1_card_obj     = Card.objects.create(**parent1_card_data)
        parent2_card_obj     = Card.objects.create(**parent2_card_data)

        # Create Placement linking cards
        placement = Placement.objects.create(
            student_card=student_card_obj,
            parent1_card=parent1_card_obj,
            parent2_card=parent2_card_obj,
            **validated_data
        )
        return placement

    def update(self, instance, validated_data):
        # Update simple fields
        for attr in ['placement_date', 'placement_result', 'student_religion', 'parent1_job', 'parent2_job']:
            if attr in validated_data:
                setattr(instance, attr, validated_data.pop(attr))

        # Helper to update nested card
        def _update_card(field_name, card_instance):
            card_data = validated_data.pop(field_name, None)
            if card_data:
                for key, val in card_data.items():
                    setattr(card_instance, key, val)
                card_instance.save()

        _update_card('student_card', instance.student_card)
        _update_card('parent1_card', instance.parent1_card)
        _update_card('parent2_card', instance.parent2_card)

        instance.save()
        return instance