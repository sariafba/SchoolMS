from django.db import models
from django.conf import settings

class Notification(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[("attendance", "Attendance"), ("mark", "Mark"), ("event", "Event")])
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} for {self.student} - {self.message[:20]}"
