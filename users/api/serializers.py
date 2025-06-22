# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Employee, Role, Teacher
from django.db import transaction
from school.models import Subject
from school.api.serializers import SubjectSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request'):
            if self.context['request'].method == 'PUT':
                self.fields['username'].required = False
                self.fields['password'].required = False
                self.fields['phone'].required = False


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class RoleQuerySerializer(serializers.Serializer):
    role_name = serializers.CharField(required=False)

    def validate_role_name(self, value):
        if not Role.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"Role '{value}' does not exist.")
        return value


class EmployeeSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    role = RoleSerializer(read_only=True)
    roleID = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        write_only=True,
    )

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
            'roleID',
            'subjects',
            'subjectIDs',
            'salary',
            'contract_start',
            'contract_end',
            'day_start',
            'day_end'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.method == 'PUT':
            # Proper way to handle nested serializer context
            self.fields['user'] = UserSerializer(context=self.context, required=False)
            for field in ['roleID', 'salary', 'contract_start', 'contract_end', 'day_start', 'day_end']:
                self.fields[field].required = False


    def validate(self, attrs):
        request = self.context.get('request')
        role = attrs.get('role') or getattr(self.instance, 'role', None)
        if request and request.method == 'POST':
            if role and role.id == 2:  # Role ID 2 is 'teacher'
                if not attrs.get('subjects'):
                    raise serializers.ValidationError({
                        'subjectIDs': 'This field is required when role is teacher.'
                    })
        return attrs


    def get_subjects(self, obj):
        # Ensure the employee has a teacher relationship
        if hasattr(obj, 'teacher'):
            return SubjectSerializer(obj.teacher.subjects.all(), many=True).data
        return []


    @transaction.atomic
    def create(self, validated_data):

        # user creating
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        user.save()
        
        # employee creating
        subjectIDs = validated_data.pop('subjects', None)
        employee = Employee.objects.create(user=user, **validated_data)

        # if teacher creating
        if validated_data['role'] == Role.objects.get(name='teacher'):
            teacher = Teacher.objects.create(employee=employee)
            teacher.subjects.set(subjectIDs)


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
        subjectIDs = validated_data.pop('subjectIDs', None)

        if validated_data['role'] == Role.objects.get(name='teacher'):
            teacher, _ = Teacher.objects.update_or_create(employee=instance)
            if subjectIDs:
                teacher.subjects.set(subjectIDs)
        else:
            Teacher.objects.filter(employee=instance).delete()

        return instance






    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not hasattr(instance, 'teacher'):
            data.pop('subjects', None)
        return data