# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import *
from django.db import transaction
from school.models import Subject, Placement, Section
from school.api.serializers import SubjectSerializer, SectionSerializer
from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'first_name', 'last_name']

class CustomUserDetailsSerializer(BaseUserDetailsSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        if hasattr(obj, 'employee'):
            return obj.employee.role
        return None

    class Meta(BaseUserDetailsSerializer.Meta):
        fields = BaseUserDetailsSerializer.Meta.fields + ('role',)

class EmployeeSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    role = serializers.ChoiceField(choices=Employee.ROLE_CHOICES)
    subjects = serializers.SerializerMethodField()
    subjectIDs = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subjects',
        write_only=True,
        many=True,
        required=False
    )


    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'role',
            'father_name',
            'mother_name',
            'nationality',
            'gender',
            'address',
            'birth_date',
            'family_status',
            'national_no',
            'subjects',
            'subjectIDs',
            'salary',
            'contract_start',
            'contract_end',
            'day_start',
            'day_end'
        ]


    def validate(self, attrs):

        request = self.context.get('request')
        role = attrs.get('role') or getattr(self.instance, 'role', None)

        if role == 'teacher':
            if request.method == 'POST' or request.method == 'PATCH':
                if not attrs.get('subjects'):
                    raise serializers.ValidationError({
                        'subjectIDs': 'This field is required when role is teacher.'
                    })
                
        return attrs


    @transaction.atomic
    def create(self, validated_data):

        # user creating
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        user.save()
        
        # employee creating
        subjects = validated_data.pop('subjects', None)
        employee = Employee.objects.create(user=user, **validated_data)

        # teacher creating
        if validated_data['role'] == 'teacher':
            teacher = Teacher.objects.create(employee=employee)
            teacher.subjects.set(subjects)
            

        return employee

            
    @transaction.atomic
    def update(self, instance, validated_data):

        # user updating
        user_data = validated_data.pop('user', None)
        if user_data:
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            if password:
                instance.user.set_password(password)
            instance.user.save()
        
        # employee updating
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # teacher updating
        subjects = validated_data.pop('subjects', None)
        if validated_data.get('role') and validated_data.get('role') == 'teacher':        
            teacher, _ = Teacher.objects.update_or_create(employee=instance)
            if subjects:
                teacher.subjects.set(subjects)
        else:
            Teacher.objects.filter(employee=instance).delete()

        return instance


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not hasattr(instance, 'teacher'):
            data.pop('subjects', None)
        return data
    

    def get_subjects(self, obj):
        # Ensure the employee has a teacher relationship
        if hasattr(obj, 'teacher'):
            return SubjectSerializer(obj.teacher.subjects.all(), many=True).data
        return []

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # Only include username

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = Parent
        fields = ['job', 'card']

class StudentSerializer(serializers.ModelSerializer):

    username  = serializers.CharField(write_only=True, required=True)
    password  = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    placement = serializers.PrimaryKeyRelatedField(
        queryset=Placement.objects.all(),
        write_only=True,
        required = True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        source='section',
        queryset=Section.objects.all(),
        write_only=True,
        required=True
    )
    religion = serializers.ChoiceField(
        choices=Student.RELIGION_CHOICES,  # Assuming you have this in your model
        required=True
    )
    student_card = CardSerializer(write_only=True, required=False)

    parent1_card = CardSerializer(write_only=True, required=False)
    parent2_card = CardSerializer(write_only=True, required=False)

    parent1_job = serializers.CharField(write_only=True, required=False)
    parent2_job = serializers.CharField(write_only=True, required=False)

    # read-only fields
    user = SimpleUserSerializer(read_only=True)
    card = CardSerializer(read_only=True)
    parent1 = ParentSerializer(read_only=True)
    parent2 = ParentSerializer(read_only=True)
    section = SectionSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'username', 'password',
            'placement',
            'register_date',
            'religion',
            'student_card',
            'parent1_card', 'parent2_card',
            'parent1_job', 'parent2_job',
            'card', 'parent1', 'parent2',
            'section', 'section_id'
        ]

    def validate_placement(self, placement):
        if placement.placement_result is not True:
            raise serializers.ValidationError("Placement is not approved.")
        return placement
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        placement = validated_data.pop('placement')
        section   = validated_data.pop('section')
        username  = validated_data.pop('username')
        password  = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password)

        parent1 = Parent.objects.create(job=placement.parent1_job, card=placement.parent1_card)
        parent2 = Parent.objects.create(job=placement.parent2_job, card=placement.parent2_card)

        student = Student.objects.create(
            user=user,
            card=placement.student_card,
            religion=placement.student_religion,
            parent1=parent1,
            parent2=parent2,
            section=section
        )

        placement.delete()  # optional
        return student

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. Update User
        user = instance.user
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if username:
            user.username = username
        if password:
            user.set_password(password)
        user.save()

        # 2. Update Student.religion
        if 'religion' in validated_data:
            instance.religion = validated_data.pop('religion')
            instance.save(update_fields=['religion'])

        # Update Student.section
        if 'section' in validated_data:
            instance.section = validated_data.pop('section')
            instance.save(update_fields=['section'])

        # 3. Update student card
        student_card_data = validated_data.pop('student_card', None)
        if student_card_data:
            for field, value in student_card_data.items():
                setattr(instance.card, field, value)
            instance.card.save()

        # 4. Update parent1 job & card
        parent1_job = validated_data.pop('parent1_job', None)
        if parent1_job:
            instance.parent1.job = parent1_job
        parent1_card_data = validated_data.pop('parent1_card', None)
        if parent1_card_data:
            for field, value in parent1_card_data.items():
                setattr(instance.parent1.card, field, value)
            instance.parent1.card.save()
        instance.parent1.save()

        # 5. Update parent2 job & card
        parent2_job = validated_data.pop('parent2_job', None)
        if parent2_job:
            instance.parent2.job = parent2_job
        parent2_card_data = validated_data.pop('parent2_card', None)
        if parent2_card_data:
            for field, value in parent2_card_data.items():
                setattr(instance.parent2.card, field, value)
            instance.parent2.card.save()
        instance.parent2.save()

        return instance
    
class CreateStudentSerializer(serializers.ModelSerializer):
    # User creation fields (nested)
    user = serializers.SerializerMethodField(read_only=True)  # For response
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    # Student card (nested)
    card = CardSerializer()
    
    # Parents data (flat structure for job + nested cards)
    parent1_job = serializers.CharField(write_only=True)
    parent1_card = CardSerializer(write_only=True)
    parent2_job = serializers.CharField(write_only=True)
    parent2_card = CardSerializer(write_only=True)
    
    # Section (ID only)
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), 
        write_only=True,
        source='section',
        required=True
    )
    section = SectionSerializer(read_only=True)  # For response
    
    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'username',
            'password',
            'register_date',
            'religion',
            'card',
            'section_id',
            'section',
            'parent1_job',
            'parent1_card',
            'parent2_job',
            'parent2_card',
        ]
        read_only_fields = ['id', 'user', 'register_date', 'section']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        # Create User
        user = User.objects.create_user(
            username=validated_data.pop('username'),
            password=validated_data.pop('password')
        )
        
        # Create Student Card
        card_data = validated_data.pop('card')
        student_card = Card.objects.create(**card_data)
        
        # Create Parent 1
        parent1_job = validated_data.pop('parent1_job')
        parent1_card_data = validated_data.pop('parent1_card')
        parent1_card = Card.objects.create(**parent1_card_data)
        parent1 = Parent.objects.create(job=parent1_job, card=parent1_card)
        
        # Create Parent 2
        parent2_job = validated_data.pop('parent2_job')
        parent2_card_data = validated_data.pop('parent2_card')
        parent2_card = Card.objects.create(**parent2_card_data)
        parent2 = Parent.objects.create(job=parent2_job, card=parent2_card)
        
        # Create Student
        student = Student.objects.create(
            user=user,
            card=student_card,
            parent1=parent1,
            parent2=parent2,
            **validated_data  # religion + section
        )
        
        return student