from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)

router.register('programs', ProgramView)
router.register('activities', ActivityView)
router.register('visits-dates', VisitDateView)
router.register('visits', VisitView)


urlpatterns = [
    path('', include(router.urls)),
]
