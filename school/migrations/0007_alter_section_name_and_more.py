# Generated by Django 5.2.1 on 2025-06-20 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_grade_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name='section',
            constraint=models.UniqueConstraint(fields=('name', 'grade'), name='unique_section_name_per_grade'),
        ),
    ]
