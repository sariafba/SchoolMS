# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Employee, Teacher
from django.db import transaction
from school.models import Subject
from school.api.serializers import SubjectSerializer
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