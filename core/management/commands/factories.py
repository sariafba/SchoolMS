import factory
from faker import Faker
from users.models import Card, Student, User, Parent, Employee, Teacher
from school.models import Section, Subject
from chat.models import ChatRoom
import random

fake = Faker()

'''
-- factory students
'''
class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Card

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker('numerify', text='09########')
    nationality = factory.Faker("country")
    gender = factory.Iterator(["male", "female"])
    birth_date = factory.Faker("date_of_birth", minimum_age=6, maximum_age=50)
    birth_city = factory.Faker("city")
    address = factory.Faker("address")
    place_of_register = factory.Faker("city")
    national_no = factory.Faker("ean13")  # or random number

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")

class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent
    job = factory.Faker("job")
    card = factory.SubFactory(CardFactory)

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    religion = factory.Iterator(["islam", "christianity", "other"])
    
    card = factory.SubFactory(CardFactory)
    parent1 = factory.SubFactory(ParentFactory)
    parent2 = factory.SubFactory(ParentFactory)

        

'''
-- factory teachers
'''
class EmployeeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")
    phone = factory.Faker('numerify', text='09########')
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    
class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(EmployeeUserFactory)
    role = "teacher"

    father_name = factory.Faker("first_name")
    mother_name = factory.Faker("first_name")
    nationality = factory.Faker("country")
    gender = factory.Iterator(["male", "female"])
    address = factory.Faker("address")
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=50)
    family_status = factory.Iterator(["married", "single"])
    national_no = factory.Faker("ean13")

    salary = factory.Faker('pydecimal', 
                      left_digits=4,  # max_digits - decimal_places
                      right_digits=2, 
                      positive=True)    
    contract_start = factory.Faker("date")
    contract_end = factory.Faker("date")
    day_start = factory.Faker("time")
    day_end = factory.Faker("time")

class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    employee = factory.SubFactory(EmployeeFactory)

    @factory.post_generation
    def subjects(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # If you pass subjects manually like TeacherFactory(subjects=[s1, s2])
            for subject in extracted:
                self.subjects.add(subject)
        else:
            # Otherwise, randomly assign some subjects
            subjects = Subject.objects.order_by('?')[:2]  # pick 2 random subjects
            self.subjects.set(subjects)

