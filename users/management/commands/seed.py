from django.core.management.base import BaseCommand
from users.models import Role

class Command(BaseCommand):

    help = 'Seeding the database with users'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding data...'))
        
        Role.objects.all().delete()
        Role.objects.create(name='cooperator')
        Role.objects.create(name='teacher')
        Role.objects.create(name='receptionist')

        self.stdout.write(self.style.SUCCESS('✅ Seeding complete!'))
