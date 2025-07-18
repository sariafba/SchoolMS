from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('subjects', SubjectView)
router.register('study-years', StudyYearView)
router.register('study-stages', StudyStageView)
router.register('grades', GradeView)
router.register('sections', SectionView)
router.register('schedules', ScheduleView)
router.register('posts', PostView)

urlpatterns = [
    path('', include(router.urls)),
]
