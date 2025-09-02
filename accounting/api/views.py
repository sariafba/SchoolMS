from rest_framework import viewsets, permissions
from accounting.models import Fee, Discount, FeeAssignment, Payment
from .serializers import (
    FeeSerializer,
    DiscountSerializer,
    FeeAssignmentSerializer,
    PaymentSerializer,
)
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend


class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [IsReceptionistPermission]


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsReceptionistPermission]


class FeeAssignmentViewSet(viewsets.ModelViewSet):
    queryset = FeeAssignment.objects.all()
    serializer_class = FeeAssignmentSerializer
    permission_classes = [AccountingPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student", "fee", "student__section__grade", "student__section"]

    def get_queryset(self):
        if hasattr(self.request.user, "student"):
            return self.queryset.filter(student=self.request.user.student)
        return self.queryset


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AccountingPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student", "fee_assignment"]

    def get_queryset(self):
        if hasattr(self.request.user, "student"):
            return self.queryset.filter(student=self.request.user.student)
        return self.queryset
