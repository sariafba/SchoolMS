from django.urls import path, include
from .views import EmployeeView, RoleView

urlpatterns = [

    # dj_rest_auth
    path('auth/', include('dj_rest_auth.urls')),

    # Cooperator
    path('employees/', EmployeeView.as_view()),         # GET all, POST
    path('employees/<int:pk>', EmployeeView.as_view()), # GET one, PUT, DELETE    

    # Role
    path('roles/', RoleView.as_view()),
    path('roles/<int:pk>', RoleView.as_view()),
]