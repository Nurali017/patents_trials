"""
Management команда для синхронизации данных с Patents Service

Использование:
    python manage.py sync_from_patents --model=sorts
    python manage.py sync_from_patents --model=cultures
    python manage.py sync_from_patents --model=all
    python manage.py sync_from_patents --model=all --outdated-only --days=7
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from trials_app.models import SortRecord, Culture, Originator
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Синхронизировать данные с Patents Service'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            default='all',
            choices=['sorts', 'cultures', 'originators', 'all'],
            help='Какие данные синхронизировать'
        )
        parser.add_argument(
            '--outdated-only',
            action='store_true',
            help='Синхронизировать только устаревшие записи'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Количество дней для определения устаревших данных (default: 7)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет синхронизировано без изменений'
        )
    
    def handle(self, *args, **options):
        model = options['model']
        outdated_only = options['outdated_only']
        days = options['days']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN режим - изменения не будут сохранены'))
        
        cutoff_date = None
        if outdated_only:
            cutoff_date = timezone.now() - timedelta(days=days)
            self.stdout.write(f'📅 Синхронизация данных старше {days} дней (до {cutoff_date})')
        
        # Счетчики
        stats = {
            'sorts': {'success': 0, 'failed': 0, 'skipped': 0},
            'cultures': {'success': 0, 'failed': 0, 'skipped': 0},
            'originators': {'success': 0, 'failed': 0, 'skipped': 0}
        }
        
        # Синхронизация сортов
        if model in ['sorts', 'all']:
            self.stdout.write(self.style.HTTP_INFO('\n🌾 Синхронизация сортов...'))
            stats['sorts'] = self._sync_sorts(cutoff_date, dry_run)
        
        # Синхронизация культур
        if model in ['cultures', 'all']:
            self.stdout.write(self.style.HTTP_INFO('\n🌱 Синхронизация культур...'))
            stats['cultures'] = self._sync_cultures(cutoff_date, dry_run)
        
        # Синхронизация оригинаторов
        if model in ['originators', 'all']:
            self.stdout.write(self.style.HTTP_INFO('\n👥 Синхронизация оригинаторов...'))
            stats['originators'] = self._sync_originators(cutoff_date, dry_run)
        
        # Итоговая статистика
        self._print_summary(stats)
    
    def _sync_sorts(self, cutoff_date=None, dry_run=False):
        """Синхронизировать сорта"""
        stats = {'success': 0, 'failed': 0, 'skipped': 0}
        
        queryset = SortRecord.objects.filter(is_deleted=False)
        if cutoff_date:
            queryset = queryset.filter(synced_at__lt=cutoff_date) | queryset.filter(synced_at__isnull=True)
        
        total = queryset.count()
        self.stdout.write(f'📊 Найдено сортов для синхронизации: {total}')
        
        for sort_record in queryset:
            try:
                if dry_run:
                    self.stdout.write(f'  [DRY] {sort_record.name} (ID: {sort_record.sort_id})')
                    stats['skipped'] += 1
                else:
                    success = sort_record.sync_from_patents(sync_originators=True)
                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ {sort_record.name} (ID: {sort_record.sort_id})')
                        )
                        stats['success'] += 1
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Не удалось синхронизировать: {sort_record.sort_id}')
                        )
                        stats['failed'] += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Ошибка {sort_record.sort_id}: {e}')
                )
                stats['failed'] += 1
                logger.error(f'Sync error for sort {sort_record.sort_id}: {e}')
        
        return stats
    
    def _sync_cultures(self, cutoff_date=None, dry_run=False):
        """Синхронизировать культуры"""
        stats = {'success': 0, 'failed': 0, 'skipped': 0}
        
        queryset = Culture.objects.filter(is_deleted=False)
        if cutoff_date:
            queryset = queryset.filter(synced_at__lt=cutoff_date) | queryset.filter(synced_at__isnull=True)
        
        total = queryset.count()
        self.stdout.write(f'📊 Найдено культур для синхронизации: {total}')
        
        for culture in queryset:
            try:
                if dry_run:
                    self.stdout.write(f'  [DRY] {culture.name} (ID: {culture.culture_id})')
                    stats['skipped'] += 1
                else:
                    success = culture.sync_from_patents()
                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ {culture.name} (ID: {culture.culture_id})')
                        )
                        stats['success'] += 1
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Не удалось синхронизировать: {culture.culture_id}')
                        )
                        stats['failed'] += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Ошибка {culture.culture_id}: {e}')
                )
                stats['failed'] += 1
                logger.error(f'Sync error for culture {culture.culture_id}: {e}')
        
        return stats
    
    def _sync_originators(self, cutoff_date=None, dry_run=False):
        """Синхронизировать оригинаторов"""
        stats = {'success': 0, 'failed': 0, 'skipped': 0}
        
        queryset = Originator.objects.filter(is_deleted=False)
        if cutoff_date:
            queryset = queryset.filter(synced_at__lt=cutoff_date) | queryset.filter(synced_at__isnull=True)
        
        total = queryset.count()
        self.stdout.write(f'📊 Найдено оригинаторов для синхронизации: {total}')
        
        for originator in queryset:
            try:
                if dry_run:
                    self.stdout.write(f'  [DRY] {originator.name} (ID: {originator.originator_id})')
                    stats['skipped'] += 1
                else:
                    success = originator.sync_from_patents()
                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ {originator.name} (ID: {originator.originator_id})')
                        )
                        stats['success'] += 1
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Не удалось синхронизировать: {originator.originator_id}')
                        )
                        stats['failed'] += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Ошибка {originator.originator_id}: {e}')
                )
                stats['failed'] += 1
                logger.error(f'Sync error for originator {originator.originator_id}: {e}')
        
        return stats
    
    def _print_summary(self, stats):
        """Вывести итоговую статистику"""
        self.stdout.write(self.style.HTTP_INFO('\n' + '='*60))
        self.stdout.write(self.style.HTTP_INFO('📊 ИТОГОВАЯ СТАТИСТИКА'))
        self.stdout.write(self.style.HTTP_INFO('='*60))
        
        for model_name, model_stats in stats.items():
            if model_stats['success'] > 0 or model_stats['failed'] > 0 or model_stats['skipped'] > 0:
                self.stdout.write(f'\n{model_name.upper()}:')
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Успешно: {model_stats["success"]}')
                )
                if model_stats['failed'] > 0:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Ошибки: {model_stats["failed"]}')
                    )
                if model_stats['skipped'] > 0:
                    self.stdout.write(
                        self.style.WARNING(f'  ⊘ Пропущено: {model_stats["skipped"]}')
                    )
        
        self.stdout.write(self.style.HTTP_INFO('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Синхронизация завершена!'))

