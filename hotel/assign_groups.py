from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Assign users to groups'

    def handle(self, *args, **kwargs):
        # Asignar un usuario al grupo 'admin'
        admin_user = User.objects.get(username='admin_user')
        admin_group = Group.objects.get(name='admin')
        admin_user.groups.add(admin_group)

        # Asignar un usuario al grupo 'cliente'
        client_user = User.objects.get(username='client_user')
        client_group = Group.objects.get(name='cliente')
        client_user.groups.add(client_group)

        self.stdout.write(self.style.SUCCESS('Usuarios asignados a los grupos correctamente'))
