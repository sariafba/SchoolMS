from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('employees', EmployeeView)
router.register('students', StudentView)

urlpatterns = [

    # dj_rest_auth
    path('auth/', include('dj_rest_auth.urls')),

    # router
    path('', include(router.urls)),
    
]