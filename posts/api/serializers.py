from rest_framework import serializers
from posts.models import *
from school.models import Section

class SectionSerializer(serializers.ModelSerializer):
    grade = serializers.ReadOnlyField(source='grade.name')
    class Meta:
        model = Section
        fields = ['id', 'name', 'grade']

class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)  # This is the key change
    class Meta:
        model = Attachment
        fields = ['file', 'file_type']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_public = serializers.BooleanField()
    attachments = AttachmentSerializer(many=True, required=False)
    sections = SectionSerializer(many=True, read_only=True)
    section_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Section.objects.all(),
        write_only=True,
        required=True,
        source='sections',
        # allow_empty=False
    )

    comments = serializers.SerializerMethodField(read_only=True)  # <-- here

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'is_public', 'title', 'text', 'sections', 'section_ids',
            'created_at', 'updated_at', 'attachments', 'comments'
        ]

    def get_comments(self, obj):
        # Only top-level comments; each will serialize its own replies
        qs = (obj.comments
                .filter(comment__isnull=True)
                .select_related('user')
                .prefetch_related('replies__user'))
        return CommentSerializer(qs, many=True, context=self.context).data

  

    def validate(self, attrs):
        is_public = attrs.get('is_public', True)
        sections = attrs.get('sections', [])
        
        if not is_public and not sections:
            raise serializers.ValidationError({
                'section_ids': 'This field is required when the post is not public.'
            })
        
        return attrs

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        sections_data = validated_data.pop('sections', [])
        
        # Get user from the request (via token)
        user = self.context.get('request').user
        
        # Create post
        post = Post.objects.create(user=user, **validated_data)
        
        # Add sections
        if validated_data['is_public']:
            post.sections.set([])
        else :
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
        instance.is_public = validated_data.get('is_public', instance.is_public)

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
    
class CommentSerializer(serializers.ModelSerializer):
    # Hide the user field on write, auto‑assign from request.user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'comment',   # parent comment (for replies)
            'text',
            'user',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'post': {'write_only': True},
            'comment': {'write_only': True},
        }

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Comments cannot be updated.")

    def to_representation(self, instance):
        # On read, include nested user and replies if you like:
        ret = super().to_representation(instance)
        ret['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
        }
        # Optionally include replies:
        ret['replies'] = CommentSerializer(
            instance.replies.all(), many=True, context=self.context
        ).data
        return ret