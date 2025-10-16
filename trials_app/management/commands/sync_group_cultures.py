"""
Команда для синхронизации всех групп культур из Patents Service

Использование:
    python manage.py sync_group_cultures
    python manage.py sync_group_cultures --dry-run
"""

from django.core.management.base import BaseCommand
from trials_app.models import GroupCulture
from trials_app.patents_integration import patents_api


class Command(BaseCommand):
    help = 'Синхронизировать все группы культур из Patents Service'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет создано без записи в БД',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим\n'))
        
        self.stdout.write('Синхронизация групп культур из Patents Service...\n')
        
        # Получить все группы из Patents
        groups = patents_api.get_all_group_cultures()
        
        if not groups:
            self.stdout.write(self.style.ERROR('❌ Не удалось получить данные из Patents Service'))
            return
        
        self.stdout.write(f'Получено групп из Patents: {len(groups)}\n')
        
        created_count = 0
        updated_count = 0
        
        for group_data in groups:
            group_id = group_data.get('id')
            name = group_data.get('name')
            code = group_data.get('code', '')
            description = group_data.get('description', '')
            
            if not group_id or not name:
                continue
            
            if dry_run:
                exists = GroupCulture.objects.filter(group_culture_id=group_id).exists()
                status = '🔄 Обновится' if exists else '✅ Создастся'
                self.stdout.write(f'  {status}: {name} (ID: {group_id}, code: {code})')
            else:
                group, created = GroupCulture.objects.update_or_create(
                    group_culture_id=group_id,
                    defaults={
                        'name': name,
                        'code': code,
                        'description': description
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✅ Создано: {name} (ID: {group_id})'))
                else:
                    updated_count += 1
                    self.stdout.write(f'  🔄 Обновлено: {name} (ID: {group_id})')
        
        # Итоговый отчет
        self.stdout.write('\n' + '='*70)
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN ЗАВЕРШЕН'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!'))
            self.stdout.write(f'\n   Создано: {created_count}')
            self.stdout.write(f'   Обновлено: {updated_count}')
            self.stdout.write(f'   Всего в БД: {GroupCulture.objects.count()}')
        self.stdout.write('='*70 + '\n')

