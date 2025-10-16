"""
Django management command to wait for database to be available.
"""
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('⏳ Ожидание доступности БД...')
        db_conn = None
        max_retries = 30
        retry_count = 0
        
        while not db_conn and retry_count < max_retries:
            try:
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS('✅ БД доступна!'))
                break
            except OperationalError:
                retry_count += 1
                self.stdout.write(
                    f'⏳ БД недоступна, попытка {retry_count}/{max_retries}...'
                )
                time.sleep(1)
        
        if retry_count >= max_retries:
            self.stdout.write(
                self.style.ERROR('❌ Не удалось подключиться к БД!')
            )
            raise Exception('Database connection failed after maximum retries')


















