# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Employee, Role, Teacher
from django.db import transaction

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

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'role',
            'roleID',
            'salary',
            'contract_start',
            'contract_end',
            'day_start',
            'day_end'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method == 'PUT':
            # Proper way to handle nested serializer context
            self.fields['user'] = UserSerializer(context=self.context)
            self.fields['user'].required = False
            self.fields['roleID'].required = False
            self.fields['salary'].required = False
            self.fields['contract_start'].required = False
            self.fields['contract_end'].required = False
            self.fields['day_start'].required = False
            self.fields['day_end'].required = False

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        user.save()
        
        employee = Employee.objects.create(user=user, **validated_data)

        if validated_data['role'] == Role.objects.get(name='teacher'):
            Teacher.objects.create(employee=employee)

        return employee

            
    @transaction.atomic
    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', None)
        if user_data:
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            if password:
                instance.user.set_password(password)
            instance.user.save()

        if validated_data['role'] == Role.objects.get(name='teacher'):
            Teacher.objects.update_or_create(employee=instance)
        else:
            Teacher.objects.filter(employee=instance).delete()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance