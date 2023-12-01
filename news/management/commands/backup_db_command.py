import datetime

from django.core.management.base import BaseCommand
import os
import subprocess

from rayapp import settings


class Command(BaseCommand):
    help = 'Backup the database'

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        backup_dir = os.path.join(settings.MEDIA_ROOT, "backup/")

        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f"db_backup_{now}.sql")

        subprocess.run(
            ['docker', 'exec', '-i', 'rayapp-db-1', '/usr/bin/pg_dump', '-h', 'localhost', '-U',
             'postgres', '-d', 'postgres'],
            stdout=open(backup_file, 'w'),
            check=True
        )
        self.stdout.write(self.style.SUCCESS(f'Database backup created: {backup_file}'))

