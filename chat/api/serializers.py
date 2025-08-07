from rest_framework import serializers
from chat.models import *
from django.db import transaction

class ChatRoomSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'student_name',
            'last_message',
        ]

    def get_student_name(self, obj):
        return f"{obj.student.card.first_name} {obj.student.card.last_name}"
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            
            if last_msg.sender == self.context['request'].user:
                sender = 'You'
            elif hasattr(last_msg.sender, 'student'):
                sender = 'Student'
            else: 
                sender = 'School'

            # sender = 'You' if last_msg.sender == self.context['request'].user else last_msg.sender

            return {
                'content': last_msg.content,
                'created_at': last_msg.created_at,
                'sender': sender
            }
        return None

class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()

    def get_sender(self, obj):
        if obj.sender == self.context['request'].user:
            return 'You'
        elif hasattr(obj.sender, 'student'):
            return 'Student'
        else: 
            return 'School'

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'content',
            'created_at',
        ]

class GroupRoomSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField(read_only=True)
    employees = serializers.SerializerMethodField(read_only=True)

    student_ids = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        many=True,
        write_only=True,
        source='student'
    )
    employee_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        write_only=True,
        source='employees'
    )

    class Meta:
        model = GroupRoom
        fields = [
            'id',
            'name',
            'owner',
            'student_ids',
            'employee_ids',
            'students',
            'employees',
        ]
        read_only_fields = ['owner']

    @transaction.atomic
    def create(self, validated_data):
        students = validated_data.pop('student', [])
        employees = validated_data.pop('employees', [])

        owner = self.context['request'].user.employee

        # Add owner
        employees.append(owner)

        # Add all admins
        admins = Employee.objects.filter(role='admin')
        employees.extend(admins)

        # Remove duplicates using a set of IDs
        unique_employees = {e.id: e for e in employees}.values()

        # Create the group room
        group_room = GroupRoom.objects.create(owner=owner, **validated_data)
        group_room.student.set(students)
        group_room.employees.set(unique_employees)

        return group_room

    @transaction.atomic
    def update(self, instance, validated_data):
        students = validated_data.pop('student', None)
        employees = validated_data.pop('employees', None)

        if students is not None:
            instance.student.set(students)

        if employees is not None:
            owner = instance.owner  # Keep the original owner
            admins = Employee.objects.filter(role='admin')

            # Add owner and admins to the updated list
            employees.append(owner)
            employees.extend(admins)

            # Remove duplicates
            unique_employees = {e.id: e for e in employees}.values()
            instance.employees.set(unique_employees)

        # Update other fields (e.g., name)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_students(self, obj):
        return [{
            "id": student.id,
            "name": f"{student.card.first_name} {student.card.last_name}",
            # "grade": student.section.grade.name,
            # "section": student.section.name
        } for student in obj.students.all()]
    
    def get_employees(self, obj):
        return [{
            "id": employee.id,
            "name": f"{employee.user.first_name} {employee.user.last_name}",
            "role": employee.role
        } for employee in obj.employees.all()]

class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    def get_sender(self, obj):
        if obj.sender == self.context['request'].user:
            return 'You'
        elif hasattr(obj.sender, 'student'):
            return {
                'id': obj.sender.student.id,
                'name': f"{obj.sender.card.first_name} {obj.sender.card.last_name}"
            }
        else: 
            return {
                'id': obj.sender.employee.id,
                'name': f"{obj.sender.first_name} {obj.sender.last_name}"
            }

    class Meta:
        model = GroupMessage
        fields = [
            'id',
            'sender',
            'content',
            'created_at',
        ]
