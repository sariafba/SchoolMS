# filters.py (inside your app)
import django_filters
from .models import Placement

class PlacementFilter(django_filters.FilterSet):
    placement_result = django_filters.BooleanFilter()
    student_card__first_name = django_filters.CharFilter(field_name='student_card__first_name', lookup_expr='icontains')
    student_card__last_name = django_filters.CharFilter(field_name='student_card__last_name', lookup_expr='icontains')

    class Meta:
        model = Placement
        fields = ['placement_result', 'student_card__first_name', 'student_card__last_name']
