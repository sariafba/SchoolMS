from rest_framework import serializers
from landingpage.models import *

class ProgramSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_null=False, use_url=False)

    class Meta:
        model = Program
        fields = ['id', 'title', 'description', 'image', 'details']

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=False)
    class Meta:
        model = Video
        fields = ['video']

class ActivitySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_null=False, use_url=False)
    videos = VideoSerializer(many=True, required=False)

    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'image', 'details', 'videos']

    def create(self, validated_data):
        videos_data = validated_data.pop('videos', [])
        activity = Activity.objects.create(**validated_data)

        for video_data in videos_data:
            video = Video.objects.create(**video_data)
            activity.videos.add(video)

        return activity
    
    def update(self, instance, validated_data):
        videos_data = validated_data.pop('videos', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if videos_data is not None:
            instance.videos.clear()
            for video_data in videos_data:
                video = Video.objects.create(**video_data)
                instance.videos.add(video)

        return instance

class VisitDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitDate
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
