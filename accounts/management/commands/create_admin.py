import os
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Creates the admin user from environment variables'

    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write('Admin environment variables not set, skipping.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Admin user "{username}" already exists, skipping.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role=User.ADMIN
        )
        self.stdout.write(f'Admin user "{username}" created successfully.')
