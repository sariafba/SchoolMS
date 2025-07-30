from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q
from users.api.serializers import EmployeeSerializer, CreateStudentSerializer
from school.models import *
from users.models import *
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.utils.timezone import make_aware
from datetime import datetime
from .factories import StudentFactory


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
            self.seed_school()
            self.seed_users()



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


        #seed grades
        self.stdout.write(self.style.WARNING('seeding grades...'))
        Grade.objects.all().delete()
        self.reset_sequence(Grade)
        Grade.objects.create(name='KG1', study_stage=StudyStage.objects.get(name='kindergarten'), study_year=StudyYear.objects.get(name='2020/2021'))
        Grade.objects.create(name='KG2', study_stage=StudyStage.objects.get(name='kindergarten'), study_year=StudyYear.objects.get(name='2020/2021'))

        Grade.objects.create(name='Grade 1', study_stage=StudyStage.objects.get(name='elementary'), study_year=StudyYear.objects.get(name='2020/2021'))
        Grade.objects.create(name='Grade 2', study_stage=StudyStage.objects.get(name='elementary'), study_year=StudyYear.objects.get(name='2020/2021'))
        Grade.objects.create(name='Grade 3', study_stage=StudyStage.objects.get(name='elementary'), study_year=StudyYear.objects.get(name='2020/2021'))
        Grade.objects.create(name='Grade 4', study_stage=StudyStage.objects.get(name='elementary'), study_year=StudyYear.objects.get(name='2020/2021'))
        Grade.objects.create(name='Grade 5', study_stage=StudyStage.objects.get(name='elementary'), study_year=StudyYear.objects.get(name='2020/2021'))
        Grade.objects.create(name='Grade 6', study_stage=StudyStage.objects.get(name='elementary'), study_year=StudyYear.objects.get(name='2020/2021'))
        self.stdout.write(self.style.SUCCESS('✅ grades seeded.'))

        #seed sections
        self.stdout.write(self.style.WARNING('seeding sections...'))
        Section.objects.all().delete()
        self.reset_sequence(Section)
        Section.objects.create(name='A', grade=Grade.objects.get(name='KG1'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='KG1'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='KG2'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='KG2'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='Grade 1'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='Grade 1'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='Grade 2'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='Grade 2'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='Grade 3'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='Grade 3'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='Grade 4'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='Grade 4'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='Grade 5'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='Grade 5'))
        Section.objects.create(name='A', grade=Grade.objects.get(name='Grade 6'))
        Section.objects.create(name='B', grade=Grade.objects.get(name='Grade 6'))
        self.stdout.write(self.style.SUCCESS('✅ sections seeded.'))


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

        #seed placement-dates
        self.stdout.write(self.style.WARNING('seeding placement-dates'))
        PlacementDate.objects.all().delete()
        self.reset_sequence(PlacementDate)
        PlacementDate.objects.create(
            date=make_aware(datetime(2025, 12, 1, 9, 30)), limit=10
        )
        PlacementDate.objects.create(
            date=make_aware(datetime(2024, 12, 2, 10, 30)), limit=10
        )
        self.stdout.write(self.style.SUCCESS('✅ placement-dates seeded.'))

    def seed_users(self):

        #seed students
        self.stdout.write(self.style.WARNING('seeding students'))
        Student.objects.all().delete()
        self.reset_sequence(User)
        self.reset_sequence(Student)
        self.reset_sequence(Parent)
        self.reset_sequence(Card)

        for _ in range(30):
            StudentFactory()

        self.stdout.write(self.style.SUCCESS('✅ students seeded.'))

        #seed employees
        self.stdout.write(self.style.WARNING('seeding employees'))
        User.objects.filter(
            Q(username__icontains='ahmed')
        ).delete()
        self.reset_sequence(User)
        self.reset_sequence(Employee)
        self.reset_sequence(Teacher)

        common_fields = {
        "father_name": "Ahmed",
        "mother_name": "Marwan",
        "nationality": "Egyptian",
        "gender": "male",
        "address": "Cairo",
        "birth_date": "2000-01-01",
        "family_status": "married",
        "national_no": "1234567890",
    }

        #1
        serializer = EmployeeSerializer(data={
        "user": {
            "username": "ahmed01",
            "password": "password",
            "phone": "0900000001",
            "first_name": "Ahmed1",
            "last_name": "Marwan1"
        },
        "role": 'admin',
        "father_name": "Ahmed1",
        "mother_name": "Marwan1",
        "nationality": "Egyptian",
        "gender": "male",
        "address": "Cairo",
        "birth_date": "2000-01-01",
        "family_status": "married",
        "national_no": "1234567890",
        "salary": "15000.00",
        "contract_start": "2024-09-01",
        "contract_end": "2025-06-01",
        "day_start": "08:00:00",
        "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #2
        serializer = EmployeeSerializer(data={
        "user": {
            "username": "ahmed02",
            "password": "password",
            "phone": "0900000002",
            "first_name": "Ahmed2",
            "last_name": "Marwan2"
        },
        "role": 'cooperator',
        **common_fields,
        "salary": "5000.00",
        "contract_start": "2024-09-01",
        "contract_end": "2025-06-01",
        "day_start": "08:00:00",
        "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()
        
        #3
        serializer = EmployeeSerializer(data={
        "user": {
            "username": "ahmed03",
            "password": "password",
            "phone": "0900000003",
            "first_name": "Ahmed3",
            "last_name": "Marwan3"
        },
        "role": 'cooperator',
        **common_fields,
        "salary": "3500.00",
        "contract_start": "2024-09-01",
        "contract_end": "2025-06-01",
        "day_start": "08:00:00",
        "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #4
        serializer = EmployeeSerializer(data={
        "user": {
            "username": "ahmed04",
            "password": "password",
            "phone": "0900000004",
            "first_name": "Ahmed4",
            "last_name": "Marwan4"
        },
        "role": 'teacher',
        **common_fields,
        "subjectIDs": [1], # Arabic
        "salary": "7000.00",
        "contract_start": "2024-09-01",
        "contract_end": "2025-06-01",
        "day_start": "08:00:00",
        "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()
    
        #5
        serializer = EmployeeSerializer(data={
        "user": {
            "username": "ahmed05",
            "password": "password",
            "phone": "0900000005",
            "first_name": "Ahmed5",
            "last_name": "Marwan5"
        },
        "role": 'teacher',
        **common_fields,
        "subjectIDs": [2], # English
        "salary": "10000.00",
        "contract_start": "2024-09-01",
        "contract_end": "2025-06-01",
        "day_start": "08:00:00",
        "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #6
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed06",
                "password": "password",
                "phone": "0900000006",
                "first_name": "Ahmed6",
                "last_name": "Marwan6"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [3],  # French
            "salary": "9000.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #7
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed07",
                "password": "password",
                "phone": "0900000007",
                "first_name": "Ahmed7",
                "last_name": "Marwan7"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [4],  # Mathematics
            "salary": "9500.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #8
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed08",
                "password": "password",
                "phone": "0900000008",
                "first_name": "Ahmed8",
                "last_name": "Marwan8"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [5],  # Science
            "salary": "8900.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #9
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed09",
                "password": "password",
                "phone": "0900000009",
                "first_name": "Ahmed09",
                "last_name": "Marwan09"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [9,10],  # History, Geography
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #10
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed10",
                "password": "password",
                "phone": "0900000010",
                "first_name": "Ahmed10",
                "last_name": "Marwan10"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [8],  # Religion
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #11
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed11",
                "password": "password",
                "phone": "0900000011",
                "first_name": "Ahmed11",
                "last_name": "Marwan11"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [11],  # Music
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #12
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed12",
                "password": "password",
                "phone": "0900000012",
                "first_name": "Ahmed12",
                "last_name": "Marwan12"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [12],  # Art
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()
        
        #13
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed13",
                "password": "password",
                "phone": "0900000013",
                "first_name": "Ahmed13",
                "last_name": "Marwan13"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [6,7],  # Physics, chemistry
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #14
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed14",
                "password": "password",
                "phone": "0900000014",
                "first_name": "Ahmed14",
                "last_name": "Marwan14"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [12],  # Art
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #15
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed15",
                "password": "password",
                "phone": "0900000015",
                "first_name": "Ahmed15",
                "last_name": "Marwan15"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [4],  # Mathematics
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()
        
        #16
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed16",
                "password": "password",
                "phone": "0900000016",
                "first_name": "Ahmed16",
                "last_name": "Marwan16"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [4],  # Mathematics
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #17
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed17",
                "password": "password",
                "phone": "0900000017",
                "first_name": "Ahmed17",
                "last_name": "Marwan17"
            },
            "role": 'teacher',
            **common_fields,    
            "subjectIDs": [2],  # English
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #18
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed18",
                "password": "password",
                "phone": "0900000018",
                "first_name": "Ahmed18",
                "last_name": "Marwan18"
            },
            "role": 'teacher',
            **common_fields,    
            "subjectIDs": [5],  # Science
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #19
        serializer = EmployeeSerializer(data={
            "user": {
                "username": "ahmed19",
                "password": "password",
                "phone": "0900000019",
                "first_name": "Ahmed19",
                "last_name": "Marwan19"
            },
            "role": 'teacher',
            **common_fields,
            "subjectIDs": [11],  # Music
            "salary": "8700.00",
            "contract_start": "2024-09-01",
            "contract_end": "2025-06-01",
            "day_start": "08:00:00",
            "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        #20
        serializer = EmployeeSerializer(data={
        "user": {
            "username": "ahmed20",
            "password": "password",
            "phone": "0900000020",
            "first_name": "Ahmed20",
            "last_name": "Marwan20"
        },
        "role": 'receptionist',
        **common_fields,
        "salary": "2000.00",
        "contract_start": "2024-09-01",
        "contract_end": "2025-06-01",
        "day_start": "08:00:00",
        "day_end": "13:15:00"
        }, context={'request': Request(APIRequestFactory().post('/'))})
        if serializer.is_valid():
            serializer.save()

        self.stdout.write(self.style.SUCCESS('✅ employees seeded.'))



        #seed schedule
        self.stdout.write(self.style.WARNING('seeding schedules'))
        Schedule.objects.all().delete()
        self.reset_sequence(Schedule)
        
        # Define days
        days = ['sun', 'mon', 'tue', 'wed', 'thu']
        
        # Define period times
        periods = [
            ('08:00:00', '08:45:00'),
            ('08:45:00', '09:30:00'),

            ('09:45:00', '10:30:00'),
            ('10:30:00', '11:15:00'),

            ('11:30:00', '12:15:00'),
            ('12:15:00', '13:00:00')
        ]
        
        # Predefined teacher assignments by section and period
        # Format: {grade: {section: [teacher_usernames_per_period]}}
        teacher_assignments = {

            'KG1': {
                'A': ['ahmed04', 'ahmed06', 'ahmed08', 'ahmed10', 'ahmed12', 'ahmed14'],
                'B': ['ahmed05', 'ahmed07', 'ahmed09', 'ahmed11', 'ahmed13', 'ahmed15']
            },
            'KG2': {
                'A': ['ahmed16', 'ahmed18', 'ahmed04', 'ahmed06', 'ahmed08', 'ahmed10'],
                'B': ['ahmed17', 'ahmed19', 'ahmed05', 'ahmed07', 'ahmed09', 'ahmed11']
            },
            'Grade 1': {
                'A': ['ahmed12', 'ahmed14', 'ahmed16', 'ahmed18', 'ahmed04', 'ahmed06'],
                'B': ['ahmed13', 'ahmed15', 'ahmed17', 'ahmed19', 'ahmed05', 'ahmed07']
            },
            'Grade 2': {
                'A': ['ahmed08', 'ahmed10', 'ahmed12', 'ahmed14', 'ahmed16', 'ahmed18'],
                'B': ['ahmed09', 'ahmed11', 'ahmed13', 'ahmed15', 'ahmed17', 'ahmed19']
            },
            'Grade 3': {
                'A': ['ahmed18', 'ahmed16', 'ahmed14', 'ahmed08', 'ahmed10', 'ahmed08'],
                'B': ['ahmed19', 'ahmed17', 'ahmed15', 'ahmed09', 'ahmed11', 'ahmed09']
            },
            'Grade 4': {
                'A': ['ahmed14', 'ahmed04', 'ahmed18', 'ahmed16', 'ahmed06', 'ahmed12'],
                'B': ['ahmed15', 'ahmed05', 'ahmed19', 'ahmed17', 'ahmed07', 'ahmed13']
            },
            'Grade 5': {
                'A': ['ahmed10', 'ahmed12', 'ahmed06', 'ahmed04', 'ahmed18', 'ahmed04'],
                'B': ['ahmed11', 'ahmed13', 'ahmed07', 'ahmed05', 'ahmed19', 'ahmed05']
            },
            'Grade 6': {
                'A': ['ahmed06', 'ahmed08', 'ahmed10', 'ahmed12', 'ahmed14', 'ahmed16'],
                'B': ['ahmed07', 'ahmed09', 'ahmed11', 'ahmed13', 'ahmed15', 'ahmed17']
            }
        }
                
        for day in days:
            for period_idx, (start, end) in enumerate(periods):
                for grade_name, sections in teacher_assignments.items():
                    for section_name, teachers in sections.items():
                        # Get teacher username for this specific period
                        username = teachers[period_idx]
                        
                        try:
                            # Get teacher by username through Employee and User
                            teacher = Teacher.objects.get(employee__user__username=username)                            # Get section
                            grade = Grade.objects.get(name=grade_name)
                            section = Section.objects.get(grade=grade, name=section_name)
                            
                            # Create schedule entry
                            Schedule.objects.create(
                                day=day,
                                start_time=start,
                                end_time=end,
                                teacher=teacher,
                                section=section
                            )
                        except Teacher.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Teacher {username} not found'))
                        except Grade.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Grade {grade_name} not found'))
                        except Section.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Section {section_name} for {grade_name} not found'))
        
        self.stdout.write(self.style.SUCCESS('✅ Schedule seeded'))

        




    def reset_sequence(self, model):
        """Reset SQLite auto-increment counter for a model"""
        table_name = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{table_name}";')


        