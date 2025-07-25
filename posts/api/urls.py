from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)

router.register('posts', PostView)
router.register('comments', CommentView)

urlpatterns = [
    path('', include(router.urls)),
]
