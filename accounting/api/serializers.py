from rest_framework import serializers
from accounting.models import Fee, Discount, FeeAssignment, Payment
from users.models import Student

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = "__all__"


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class FeeAssignmentSerializer(serializers.ModelSerializer):
    fee = serializers.PrimaryKeyRelatedField(queryset=Fee.objects.all(), write_only=True)
    fee_data = FeeSerializer(source="fee", read_only=True)

    discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all(), write_only=True, required=False, allow_null=True)
    discount_data = DiscountSerializer(source="discount", read_only=True)
    
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)
    student_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FeeAssignment
        fields = [
            "id",
            "fee", "fee_data",
            "student", "student_data",
            "discount", "discount_data",
            "amount", "final_amount", "remaining",
        ]

    def get_student_data(self, obj):
        return {
            "id": obj.student.id,
            "name": f"{obj.student.card.first_name} {obj.student.card.last_name}"
        }

class PaymentSerializer(serializers.ModelSerializer):

    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)

    fee_assignment = serializers.PrimaryKeyRelatedField(queryset=FeeAssignment.objects.all(), write_only=True)
    # fee_assignment_data = FeeAssignmentSerializer(source="fee_assignment", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "student",
            "fee_assignment",
            # "fee_assignment_data",
            "amount_paid",
            "date",
        ]
    
    def validate(self, data):
        if self.context["request"].method == "POST":
            student = data.get("student")
            fee_assignment = data.get("fee_assignment")

            # تحقق أن الطالب فعلاً مرتبط بالـ fee assignment
            if fee_assignment.student != student:
                raise serializers.ValidationError(
                    {"detail": f"This fee is assigned to student {fee_assignment.student.card.first_name}, not {student.card.first_name}."}
                )

            # تحقق أن الدفعة لا تتجاوز المبلغ المتبقي
            remaining = fee_assignment.final_amount - sum(
                p.amount_paid for p in fee_assignment.payments.all()
            )
            if data["amount_paid"] > remaining:
                raise serializers.ValidationError(
                    {"detail": f"Payment exceeds remaining balance ({remaining})."}
                )
            
            #validate if fee is installment available
            if not fee_assignment.fee.is_installment_available and data["amount_paid"] != fee_assignment.remaining:
                raise serializers.ValidationError(
                    {"detail": f"This fee is not installment available."}
                )

        return data

