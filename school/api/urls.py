from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectView

router = DefaultRouter(trailing_slash=False)
router.register('subjects', SubjectView)

urlpatterns = [
    path('', include(router.urls)),
]
