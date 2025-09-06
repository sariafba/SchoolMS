from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
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
    filterset_fields = ['grade', 'teachers']

class StudyYearView(ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer
    permission_classes = [IsEmployee]

class StudyStageView(ModelViewSet):
    queryset = StudyStage.objects.all()
    serializer_class = StudyStageSerializer
    permission_classes = [IsEmployee]

class GradeView(ModelViewSet):
    queryset = Grade.objects.select_related('study_stage', 'study_year').all()
    serializer_class = GradeSerializer
    permission_classes = [IsEmployee]

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
    permission_classes = [IsAuthenticated]

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
    
class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student__section', 'student', 'date']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def post(self, request, *args, **kwargs):
        user = request.user
        if not (
                user.is_superuser or
                (hasattr(user, 'employee') and user.employee.role in ['admin', 'cooperator'])
        ):
            return Response({"detail": "You do not have permission to perform this action."}, status=403)

        serializer = AttendanceSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, 'employee') and user.employee.role in ['admin', 'cooperator']:
            attendances = Attendance.objects.all()
        else:
            attendances = Attendance.objects.filter(student__user=user)

        attendances = self.filter_queryset(attendances)

        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk, *args, **kwargs):
        try:
            attendance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response({"detail": "Attendance not found."}, status=404)

        # Check object-level permission
        self.check_object_permissions(request, attendance)

        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            attendance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response({"detail": "Attendance not found."}, status=404)

        # Check object-level permission
        self.check_object_permissions(request, attendance)

        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EventView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['students__id', 'students__section', 'date']

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, "employee"):
            return Event.objects.all()

        if hasattr(user, "student"):
            return Event.objects.filter(students=user.student)
        
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()

class MarkView(APIView):
    permission_classes = [MarkPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'subject', 'mark_type', 'student__section', 'date']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def post(self, request, *args, **kwargs):
        user = request.user
        if not (
                user.is_superuser or
                (hasattr(user, 'employee') and user.employee.role in ['teacher', 'cooperator'])
        ):
            return Response({"detail": "You do not have permission to perform this action."}, status=403)

        serializer = MarkSerializer(data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, 'employee') and user.employee.role in ['admin', 'cooperator']:
            marks = Mark.objects.all()
        elif hasattr(user, 'employee') and user.employee.role in ['teacher']:
            teacher = user.employee.teacher
            marks = Mark.objects.filter(subject__in=teacher.subjects.all())
        else:
            marks = Mark.objects.filter(student__user=user)

        marks = self.filter_queryset(marks)

        serializer = MarkSerializer(marks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        try:
            mark = Mark.objects.get(pk=pk)
        except Mark.DoesNotExist:
            return Response({"detail": "Mark not found."}, status=404)

        # Check object-level permission
        self.check_object_permissions(request, mark)

        serializer = MarkSerializer(mark, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        try:
            mark = Mark.objects.get(pk=pk)
        except Mark.DoesNotExist:
            return Response({"detail": "Mark not found."}, status=404)

        # Check object-level permission
        self.check_object_permissions(request, mark)

        mark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




    