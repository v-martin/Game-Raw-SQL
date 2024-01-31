import os
from django.core.management.base import BaseCommand
from django.db import connection

from game import settings


class Command(BaseCommand):
    help = 'Initialize the database with custom SQL scripts'

    def handle(self, *args, **options):
        scripts_directory = os.path.join(settings.BASE_DIR, 'sql_scripts')

        for filename in os.listdir(scripts_directory):
            if filename.endswith('.sql'):
                script_path = os.path.join(scripts_directory, filename)
                with open(script_path, 'r', encoding='utf-8') as script_file:
                    script = script_file.read()

                with connection.cursor() as cursor:
                    cursor.execute(script)

                self.stdout.write(self.style.SUCCESS(f'Successfully executed {filename}'))

        self.stdout.write(self.style.SUCCESS('Database initialized successfully.'))
