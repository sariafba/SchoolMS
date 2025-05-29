# serializers.py
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import JWTSerializer as DefaultJWTSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomJWTSerializer(DefaultJWTSerializer):
    access = serializers.CharField()
    refresh = serializers.CharField(required=False)  # Make refresh optional
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj['user']
        return {
            'pk': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }