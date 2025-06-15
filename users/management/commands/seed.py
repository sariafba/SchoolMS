from django.core.management.base import BaseCommand
from users.models import RoleView

class Command(BaseCommand):

    help = 'Seeding the database with users'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding data...'))
        
        RoleView.objects.all().delete()
        RoleView.objects.create(name='cooperator')
        RoleView.objects.create(name='teacher')
        RoleView.objects.create(name='receptionist')

        self.stdout.write(self.style.SUCCESS('✅ Seeding complete!'))
