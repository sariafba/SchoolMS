from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Post
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sections', 'sections__grade',]


    def get_queryset(self):
        user = self.request.user

        qs = Post.objects.all()

        if hasattr(user, "student"):
            # Student: add posts from their single section
            student_section = user.student.section
            qs = Post.objects.filter(
                Q(is_public=True) | Q(sections=student_section)
            ).distinct()

        return qs

    def create(self, request, *args, **kwargs):
        # Create post normally
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            # Broadcast to WebSocket group
            self.broadcast_new_post(response.data)
            
        return response

    def broadcast_new_post(self, post_data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all_posts",
            {
                "type": "new_post",
                "post": post_data
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Double-check permission (redundant but safe)
        if not request.user == instance.user:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response(
                {"detail": "You may only delete your own comments."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


