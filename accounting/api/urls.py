from rest_framework.routers import DefaultRouter
from .views import FeeViewSet, DiscountViewSet, FeeAssignmentViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'fees', FeeViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'fee-assignments', FeeAssignmentViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls
