from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Fee(models.Model):
    symbol = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    value = models.DecimalField(max_digits=10, decimal_places=2)

    is_chosen = models.BooleanField(default=False)
    is_installment_available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.value})"

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("percent", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    symbol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()

    value = models.DecimalField(max_digits=10, decimal_places=2)

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.value}{'%' if self.discount_type == 'percent' else ''})"


class FeeAssignment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name="fee_assignments")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name="fee_assignments")

    @property
    def amount(self):
        return self.fee.value

    @property
    def final_amount(self):
        """after discount"""
        amount = self.fee.value
        if self.discount:
            if self.discount.discount_type == "percent":
                amount -= (amount * self.discount.value / Decimal(100))
            elif self.discount.discount_type == "fixed":
                amount -= self.discount.value
        return max(amount, Decimal(0))
    
    @property
    def remaining(self):
        total_paid = sum(p.amount_paid for p in self.payments.all())
        return max(self.final_amount - total_paid, Decimal(0))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fee', 'student'], name='unique_fee_assignment')
        ]

class Payment(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name="payments")
    fee_assignment = models.ForeignKey(FeeAssignment, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.amount_paid} by {self.student.name} for {self.fee_assignment.fee.name}"
