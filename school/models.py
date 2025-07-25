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

class Schedule(models.Model):
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    # class Meta:
    #     unique_together = ['teacher', 'day', 'start_time']

class PlacementDate(models.Model):
    date = models.DateTimeField()
    limit = models.IntegerField()

class Placement(models.Model):
    placement_date = models.ForeignKey(PlacementDate, on_delete=models.CASCADE)
    placement_result = models.BooleanField(default=False, null=True, blank=True)

    student_religion = models.CharField(max_length=20, choices=[('islam', 'Islam'),('christianity', 'Christianity'),('other', 'Other')])
    student_card = models.ForeignKey('users.Card', on_delete=models.CASCADE, related_name='student_placements')

    parent1_job = models.CharField(max_length=100)
    parent1_card = models.ForeignKey('users.Card', on_delete=models.CASCADE, related_name='parent1_placements')

    parent2_job = models.CharField(max_length=100)
    parent2_card = models.ForeignKey('users.Card', on_delete=models.CASCADE, related_name='parent2_placements')

    # def delete(self, *args, **kwargs):
    #     self.student_card.delete()
    #     self.parent1_card.delete()
    #     self.parent2_card.delete()
    #     super().delete(*args, **kwargs)
    