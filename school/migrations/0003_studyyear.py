# Generated by Django 5.2.1 on 2025-06-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_subject_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
