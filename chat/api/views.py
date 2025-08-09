from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from chat.models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from django.db.models import Max

class ChatRoomView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student__section', 'student__section__grade']

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'student'):
            # Return only the student's own room
            return ChatRoom.objects.filter(student=user.student)

        if hasattr(user, 'employee'):
            # Return all rooms where the employee is assigned
            return ChatRoom.objects.filter(employees=user.employee)
        
class MessageView(ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        room_id = self.request.query_params.get('room_id')

        if not room_id:
            raise ValidationError({"room_id": "This query parameter is required."})

        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            raise NotFound(detail="Room not found.")

        # Check if user is a participant in the room
        if hasattr(user, 'student') and room.student == user.student:
            return Message.objects.filter(room=room)
        elif hasattr(user, 'employee') and user.employee in room.employees.all():
            return Message.objects.filter(room=room)

        raise PermissionDenied("You are not a participant in this room.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to delete this message.")
        
class GroupRoomView(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = GroupRoomSerializer
    queryset = GroupRoom.objects.all()

    def get_queryset(self):
        user = self.request.user

        queryset = GroupRoom.objects.all()

        if hasattr(user, 'student'):
            queryset = queryset.filter(students=user.student)

        elif hasattr(user, 'employee'):
            queryset = queryset.filter(employees=user.employee)

        # Annotate with latest message timestamp
        queryset = queryset.annotate(
            last_message_time=Max('group_messages__created_at')
        ).order_by('-last_message_time', '-id')  # fallback to id if no messages

        return queryset
        
    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'employee'):
            raise PermissionDenied("Only employees can create a group room.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == request.user.employee:
            return super().update(request, *args, **kwargs)
        elif hasattr(request.user, 'employee') and request.user.employee.role == 'admin':
            return super().update(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to update this group room.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == request.user.employee:
            return super().destroy(request, *args, **kwargs)
        elif hasattr(request.user, 'employee') and request.user.employee.role == 'admin':
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to delete this group room.")
        
class GroupMessageView(ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        room_id = self.request.query_params.get('room_id')

        if not room_id:
            raise ValidationError({"room_id": "This query parameter is required."})

        try:
            room = GroupRoom.objects.get(id=room_id)
        except GroupRoom.DoesNotExist:
            raise NotFound(detail="Room not found.")

        # Check if user is a participant in the room
        if hasattr(user, 'student') and user.student in room.students.all():
            return GroupMessage.objects.filter(room=room)
        elif hasattr(user, 'employee') and user.employee in room.employees.all():
            return GroupMessage.objects.filter(room=room)

        raise PermissionDenied("You are not a participant in this room.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to delete this message.")
