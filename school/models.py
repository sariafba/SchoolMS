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

    def __str__(self):
        return self.name

class StudyStage(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=100)
    study_stage = models.ForeignKey(StudyStage, on_delete=models.CASCADE)
    study_year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'study_year'], name='unique_grade_name_per_study_year')
        ]

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'grade'], name='unique_section_name_per_grade')
        ]






