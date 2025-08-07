from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)

router.register('chat-rooms', ChatRoomView)
router.register('messages', MessageView)
router.register('group-rooms', GroupRoomView)
router.register('group-messages', GroupMessageView, basename='group-message')


urlpatterns = [
    path('', include(router.urls)),
]
