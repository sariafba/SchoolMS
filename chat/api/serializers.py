from rest_framework import serializers
from chat.models import *

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