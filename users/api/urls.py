from django.urls import path, include
from .views import Cooperator, Role

urlpatterns = [

    # dj_rest_auth
    path('auth/', include('dj_rest_auth.urls')),

    # Cooperator
    path('cooperators/', Cooperator.as_view()),         # GET all, POST
    path('cooperators/<int:pk>', Cooperator.as_view()), # GET one, PUT, DELETE    

    # Role
    path('roles/', Role.as_view()),
    path('roles/<int:pk>', Role.as_view()),
]