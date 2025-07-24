from rest_framework import serializers
from posts.models import *
from school.models import Section
from school.api.serializers import SectionSerializer



class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)  # This is the key change
    class Meta:
        model = Attachment
        fields = ['file', 'file_type']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    attachments = AttachmentSerializer(many=True, required=False)
    sections = SectionSerializer(many=True, read_only=True)
    section_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Section.objects.all(),
        write_only=True,
        required=True,
        source='sections',
        allow_empty=False
    )

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'text', 'sections', 'section_ids',
            'created_at', 'updated_at', 'attachments'
        ]

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        sections_data = validated_data.pop('sections', [])
        request = self.context.get('request')
        
        # Get user from the request (via token)
        user = request.user
        
        # Create post
        post = Post.objects.create(user=user, **validated_data)
        
        # Add sections
        post.sections.set(sections_data)
        
        # Create attachments
        for attachment_data in attachments_data:
            Attachment.objects.create(post=post, **attachment_data)

        return post
    
    def update(self, instance, validated_data):
        
        # Check if the requesting user is the post owner
        if self.context['request'].user != instance.user:
            raise serializers.ValidationError({
                "detail": "You do not have permission to update this post."
            })
        
        # Handle text update
        instance.text = validated_data.get('text', instance.text)
        
        # Handle sections update
        if 'sections' in validated_data:
            sections_data = validated_data.pop('sections')
            instance.sections.set(sections_data)
        
        # Handle attachments
        attachments_data = validated_data.pop('attachments', None)
        
        # If new attachments are provided, clear old ones and add new
        if attachments_data is not None:
            # Delete existing attachments if you want to replace them
            instance.attachments.all().delete()
            
            # Create new attachments
            for attachment_data in attachments_data:
                Attachment.objects.create(post=instance, **attachment_data)
        
        # Save the updated post instance
        instance.save()
        
        return instance
    