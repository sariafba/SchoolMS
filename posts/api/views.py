from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Post
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sections', 'sections__grade',]


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