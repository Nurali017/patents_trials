"""
Команда для пересинхронизации всех сортов с Patents Service

Обновляет:
- patents_status (1=MAIN, 2=TESTING, 3=ARCHIVE)
- SortOriginator связи (оригинаторы с процентами)
- Все остальные поля сорта

Использование:
    python manage.py resync_all_sorts
    python manage.py resync_all_sorts --limit 100
    python manage.py resync_all_sorts --dry-run
"""

from django.core.management.base import BaseCommand
from trials_app.models import SortRecord, SortOriginator
from django.db.models import Q


class Command(BaseCommand):
    help = 'Пересинхронизировать все сорта с Patents Service'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Ограничить количество сортов для синхронизации',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет синхронизировано без выполнения',
        )
        parser.add_argument(
            '--only-without-status',
            action='store_true',
            help='Синхронизировать только сорта без patents_status',
        )

    def handle(self, *args, **options):
        limit = options.get('limit')
        dry_run = options['dry_run']
        only_without_status = options['only_without_status']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим\n'))
        
        self.stdout.write('Пересинхронизация сортов с Patents Service...\n')
        
        # Фильтр
        queryset = SortRecord.objects.filter(is_deleted=False)
        
        if only_without_status:
            queryset = queryset.filter(patents_status__isnull=True)
            self.stdout.write(f'Фильтр: только сорта без patents_status\n')
        
        if limit:
            queryset = queryset[:limit]
            self.stdout.write(f'Ограничение: {limit} сортов\n')
        
        total = queryset.count()
        self.stdout.write(f'Сортов для синхронизации: {total}\n')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n🔍 DRY-RUN - синхронизация не будет выполнена'))
            return
        
        # Синхронизация
        success_count = 0
        error_count = 0
        originators_created = 0
        status_updated = 0
        
        for i, sort_record in enumerate(queryset, 1):
            # Прогресс
            if i % 100 == 0:
                self.stdout.write(f'   Прогресс: {i}/{total}...')
            
            # Подсчет до
            before_links = SortOriginator.objects.filter(sort_record=sort_record).count()
            had_status = sort_record.patents_status is not None
            
            # Синхронизация
            try:
                success = sort_record.sync_from_patents(sync_originators=True)
                
                if success:
                    success_count += 1
                    
                    # Подсчет после
                    after_links = SortOriginator.objects.filter(sort_record=sort_record).count()
                    new_links = after_links - before_links
                    
                    if new_links > 0:
                        originators_created += new_links
                    
                    # Проверка статуса
                    sort_record.refresh_from_db()
                    if not had_status and sort_record.patents_status:
                        status_updated += 1
                    
                    # Вывод для первых 10
                    if i <= 10:
                        status_info = f"status: {sort_record.get_patents_status_display()}" if sort_record.patents_status else "no status"
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ {sort_record.name} ({status_info}, {after_links} оригинаторов)'
                            )
                        )
                else:
                    error_count += 1
                    if i <= 10:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ {sort_record.name} - ошибка синхронизации')
                        )
            
            except Exception as e:
                error_count += 1
                if i <= 10:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ {sort_record.name} - исключение: {str(e)}')
                    )
        
        # Итоговый отчет
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('\n✅ СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!\n'))
        self.stdout.write(f'   Всего обработано: {total}')
        self.stdout.write(f'   Успешно: {success_count}')
        self.stdout.write(f'   Ошибок: {error_count}')
        self.stdout.write(f'   Связей SortOriginator создано: {originators_created}')
        self.stdout.write(f'   Статусов обновлено: {status_updated}')
        self.stdout.write(f'\n📊 Итого в БД:')
        self.stdout.write(f'   SortOriginator связей: {SortOriginator.objects.count()}')
        self.stdout.write(f'   Сортов со статусом: {SortRecord.objects.filter(patents_status__isnull=False).count()}')
        self.stdout.write('='*70 + '\n')

