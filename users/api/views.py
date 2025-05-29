# views.py
from dj_rest_auth.views import LoginView as DefaultLoginView
from .serializers import CustomJWTSerializer
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class CustomLoginView(DefaultLoginView):
    serializer_class = CustomJWTSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'access': self.access_token,
                'refresh': self.refresh_token if self.refresh_token else "",
                'user': self.user
            }
            serializer = serializer_class(instance=data, context=self.get_serializer_context())
        else:
            serializer = serializer_class(instance=self.token, context=self.get_serializer_context())

        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
