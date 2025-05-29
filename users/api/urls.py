from django.urls import path, include
from .views import CustomLoginView

urlpatterns = [
    path('auth/login/', CustomLoginView.as_view(), name='rest_login'),
    path('auth/', include('dj_rest_auth.urls')),
]
