from django.core.management.base import BaseCommand
from django.db import connection
from school.models import *
from users.models import *

class Command(BaseCommand):
    help = 'seeding database with default data'

    def add_arguments(self, parser):
        parser.add_argument('--app', type=str, help='App name to seed (e.g. users, school)')

    def handle(self, *args, **options):

        if options['app']:
            app = options['app']
            if app == 'school':
                self.seed_school()
            elif app == 'users':
                self.seed_users()
            else:
                self.stdout.write(self.style.ERROR(f'Unknown app: {app}'))

        else:
            self.seed_users()
            self.seed_school()



    def seed_users(self):

        #seed roles
        self.stdout.write(self.style.WARNING('seeding roles...'))
        Role.objects.all().delete()
        self.reset_sequence(Role)
        Role.objects.create(name='admin')
        Role.objects.create(name='cooperator')
        Role.objects.create(name='teacher')
        self.stdout.write(self.style.SUCCESS('✅ roles seeded.'))


    def seed_school(self):

        # seed study years
        self.stdout.write(self.style.WARNING('seeding study years...'))
        StudyYear.objects.all().delete()
        self.reset_sequence(StudyYear)
        StudyYear.objects.create(name='2020/2021')
        StudyYear.objects.create(name='2021/2022')
        StudyYear.objects.create(name='2022/2023')
        StudyYear.objects.create(name='2023/2024')
        StudyYear.objects.create(name='2024/2025')
        self.stdout.write(self.style.SUCCESS('✅ study years seeded.'))

        # seed study stages
        self.stdout.write(self.style.WARNING('seeding study stages...'))
        StudyStage.objects.all().delete()
        self.reset_sequence(StudyStage)
        StudyStage.objects.create(name='kindergarten')
        StudyStage.objects.create(name='elementary')
        self.stdout.write(self.style.SUCCESS('✅ study stages seeded.'))

        # seed subjects
        self.stdout.write(self.style.WARNING('seeding subjects...'))
        Subject.objects.all().delete()
        self.reset_sequence(Subject)
        Subject.objects.create(name='Arabic')
        Subject.objects.create(name='English')
        Subject.objects.create(name='French')
        Subject.objects.create(name='Mathematics')
        Subject.objects.create(name='Science')
        Subject.objects.create(name='Physics')
        Subject.objects.create(name='Chemistry')
        Subject.objects.create(name='Religion')
        Subject.objects.create(name='History')
        Subject.objects.create(name='Geography')
        Subject.objects.create(name='Music')
        Subject.objects.create(name='Art')
        self.stdout.write(self.style.SUCCESS('✅ subjects seeded.'))











    def reset_sequence(self, model):
        """Reset SQLite auto-increment counter for a model"""
        table_name = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{table_name}";')