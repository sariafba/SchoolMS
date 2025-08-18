from rest_framework.viewsets import ModelViewSet
from .serializers import *
from school.models import *
from django_filters.rest_framework import DjangoFilterBackend
from school.permissions import *
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from school.filters import PlacementFilter
from django.db.models import Count, F


class SubjectView(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminCooperator]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grade']

class StudyYearView(ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer
    permission_classes = [IsAdminCooperator]

class StudyStageView(ModelViewSet):
    queryset = StudyStage.objects.all()
    serializer_class = StudyStageSerializer
    permission_classes = [IsAdminCooperator]

class GradeView(ModelViewSet):
    queryset = Grade.objects.select_related('study_stage', 'study_year').all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminCooperator]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'study_stage',
        'study_year',
          ]

class SectionView(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsEmployee]


    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grade']

class ScheduleView(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsEmployee]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'section', 'day']
    
class PlacementDateView(ModelViewSet):
    queryset = PlacementDate.objects.all()
    serializer_class = PlacementDateSerializer

    permission_classes = [PlacementDatePermission]

    def get_queryset(self):
        queryset = PlacementDate.objects.all()
        future_param = self.request.query_params.get('future')
        limit_reached_param = self.request.query_params.get('limit_reached')

    # Exclude future placement dates if ?future=false
        if future_param and future_param.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(date__gt=timezone.now())

    # Exclude placement dates that have reached their limit if ?limit_reached=false
        if limit_reached_param:
            queryset = queryset.annotate(
                placement_count=Count('placement')
            )

            if limit_reached_param.lower() in ['false', '0', 'no']:
                queryset = queryset.filter(placement_count__lt=F('limit'))
            elif limit_reached_param.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(placement_count__gte=F('limit'))

        return queryset

class PlacementView(ModelViewSet):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = PlacementFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAdminCooperatorReceptionist()]
    
    def create(self, request, *args, **kwargs):
        placement_date_id = request.data.get('placement_date')

        if not placement_date_id:
            return Response({"placement_date": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            placement_date = PlacementDate.objects.get(id=placement_date_id)
        except PlacementDate.DoesNotExist:
            return Response({"placement_date": "Invalid placement_date ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        if placement_date.date < timezone.now():
            return Response({"detail": "Cannot create placements for a past date."}, status=status.HTTP_400_BAD_REQUEST)

        current_count = Placement.objects.filter(placement_date=placement_date).count()
        if current_count >= placement_date.limit:
            return Response({"detail": "Placement limit reached for this date."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
    
class AttendanceView(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = BulkAttendanceSerializer
    permission_classes = [AttendancePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'student__section', 'date']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'student'):
            return Attendance.objects.filter(student=user.student)
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BulkAttendanceSerializer
        return AttendanceReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        attendances = serializer.save()
        return Response(
            {"message": "Attendance recorded", "count": len(attendances)},
            status=status.HTTP_201_CREATED,
        )
    