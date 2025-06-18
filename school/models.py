from django.db import models
from django.core.validators import RegexValidator


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

class StudyYear(models.Model):
    name = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}/\d{4}$',
                message='Format must be YYYY/YYYY (e.g., 2020/2021)'
            )
        ]
    )

