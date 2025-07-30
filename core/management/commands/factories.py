import factory
from faker import Faker
from users.models import Card, Student, User, Parent
from school.models import Section

fake = Faker()

class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Card

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker("phone_number")
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

    section = factory.LazyFunction(lambda: Section.objects.order_by('?').first() or Section.objects.create(name="Default"))

    card = factory.SubFactory(CardFactory)
    parent1 = factory.SubFactory(ParentFactory)
    parent2 = factory.SubFactory(ParentFactory)
