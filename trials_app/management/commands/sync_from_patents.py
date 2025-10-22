"""
Management команда для полной синхронизации с Patents Service

Использование:
    python manage.py sync_from_patents
    python manage.py sync_from_patents --dry-run
    python manage.py sync_from_patents --model=originators
    python manage.py sync_from_patents --model=sorts --limit=100
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from trials_app.patents_integration import PatentsServiceClient
from trials_app.models import SortRecord, Culture, GroupCulture, Originator, SortOriginator
from trials_app.sync_helpers import get_or_sync_originator, SyncStrategy
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Полная синхронизация данных с Patents Service'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет синхронизировано без выполнения'
        )
        parser.add_argument(
            '--model',
            choices=['sorts', 'cultures', 'group-cultures', 'originators', 'all'],
            default='all',
            help='Модель для синхронизации'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Ограничить количество записей для синхронизации'
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
            help='Количество дней для определения устаревших записей'
        )
    
    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.model = options['model']
        self.limit = options['limit']
        self.outdated_only = options['outdated_only']
        self.days = options['days']
        
        self.client = PatentsServiceClient()
        self.stats = {
            'sorts': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
            'cultures': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
            'group_cultures': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
            'originators': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
        }
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим\n'))
        
        self.stdout.write('🚀 Запуск полной синхронизации с Patents Service...\n')
        
        try:
            if self.model in ['all', 'group-cultures']:
                self.sync_group_cultures()
            
            if self.model in ['all', 'cultures']:
                self.sync_cultures()
            
            if self.model in ['all', 'originators']:
                self.sync_originators()
            
            if self.model in ['all', 'sorts']:
                self.sync_sorts()
            
            self.print_summary()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка синхронизации: {e}')
            )
            raise
    
    def sync_group_cultures(self):
        """Синхронизация групп культур"""
        self.stdout.write('🌿 Синхронизация групп культур...')
        
        try:
            patents_groups = self.client.get_all_group_cultures()
            if not patents_groups:
                self.stdout.write('  ⚠️ Не удалось получить группы культур из Patents Service')
                return
            
            for i, group_data in enumerate(patents_groups[:self.limit] if self.limit else patents_groups):
                if i % 10 == 0:
                    self.stdout.write(f'  Прогресс: {i}/{len(patents_groups)}...')
                
                try:
                    if self.dry_run:
                        self.stdout.write(f'  [DRY] Группа: {group_data.get("name", "Без названия")}')
                        self.stats['group_cultures']['skipped'] += 1
                        continue
                    
                    group, created = GroupCulture.objects.get_or_create(
                        group_culture_id=group_data.get('id'),
                        defaults={
                            'name': group_data.get('name', ''),
                            'is_deleted': False,
                            'synced_at': timezone.now()
                        }
                    )
                    
                    if created:
                        self.stats['group_cultures']['created'] += 1
                    else:
                        if group.name != group_data.get('name', '') or group.is_deleted:
                            group.name = group_data.get('name', '')
                            group.is_deleted = False
                            group.synced_at = timezone.now()
                            group.save()
                            self.stats['group_cultures']['updated'] += 1
                        else:
                            self.stats['group_cultures']['skipped'] += 1
                            
                except Exception as e:
                    self.stdout.write(f'  ❌ Ошибка группы {group_data.get("id")}: {e}')
                    self.stats['group_cultures']['errors'] += 1
            
            self.stdout.write(f'  ✅ Группы культур: {self.stats["group_cultures"]["created"]} создано, {self.stats["group_cultures"]["updated"]} обновлено')
            
        except Exception as e:
            self.stdout.write(f'  ❌ Ошибка синхронизации групп культур: {e}')
    
    def sync_cultures(self):
        """Синхронизация культур"""
        self.stdout.write('🌱 Синхронизация культур...')
        
        try:
            patents_cultures = self.client.get_all_cultures()
            if not patents_cultures:
                self.stdout.write('  ⚠️ Не удалось получить культуры из Patents Service')
                return
            
            for i, culture_data in enumerate(patents_cultures[:self.limit] if self.limit else patents_cultures):
                if i % 20 == 0:
                    self.stdout.write(f'  Прогресс: {i}/{len(patents_cultures)}...')
                
                try:
                    if self.dry_run:
                        self.stdout.write(f'  [DRY] Культура: {culture_data.get("name", "Без названия")}')
                        self.stats['cultures']['skipped'] += 1
                        continue
                    
                    # Получаем группу культуры
                    group_culture = None
                    if culture_data.get('group_culture'):
                        group_culture = GroupCulture.objects.filter(
                            group_culture_id=culture_data['group_culture'].get('id')
                        ).first()
                    
                    culture, created = Culture.objects.get_or_create(
                        culture_id=culture_data.get('id'),
                        defaults={
                            'name': culture_data.get('name', ''),
                            'group_culture': group_culture,
                            'is_deleted': False,
                            'synced_at': timezone.now()
                        }
                    )
                    
                    if created:
                        self.stats['cultures']['created'] += 1
                    else:
                        if (culture.name != culture_data.get('name', '') or 
                            culture.is_deleted or 
                            culture.group_culture != group_culture):
                            culture.name = culture_data.get('name', '')
                            culture.group_culture = group_culture
                            culture.is_deleted = False
                            culture.synced_at = timezone.now()
                            culture.save()
                            self.stats['cultures']['updated'] += 1
                        else:
                            self.stats['cultures']['skipped'] += 1
                            
                except Exception as e:
                    self.stdout.write(f'  ❌ Ошибка культуры {culture_data.get("id")}: {e}')
                    self.stats['cultures']['errors'] += 1
            
            self.stdout.write(f'  ✅ Культуры: {self.stats["cultures"]["created"]} создано, {self.stats["cultures"]["updated"]} обновлено')
            
        except Exception as e:
            self.stdout.write(f'  ❌ Ошибка синхронизации культур: {e}')
    
    def sync_originators(self):
        """Синхронизация оригинаторов"""
        self.stdout.write('👥 Синхронизация оригинаторов...')
        
        try:
            patents_originators = self.client.get_all_originators()
            if not patents_originators:
                self.stdout.write('  ⚠️ Не удалось получить оригинаторов из Patents Service')
                return
            
            # Получаем ID всех оригинаторов из Patents Service
            patents_originator_ids = {originator_data.get('id') for originator_data in patents_originators}
            
            # Находим локальные оригинаторы, которых нет в Patents Service
            local_originators = Originator.objects.filter(is_deleted=False)
            deleted_count = 0
            
            for local_originator in local_originators:
                if local_originator.originator_id not in patents_originator_ids:
                    if self.dry_run:
                        self.stdout.write(f'  [DRY] Удалить: {local_originator.name} (ID: {local_originator.originator_id})')
                    else:
                        # Удаляем связи с сортами перед удалением оригинатора
                        SortOriginator.objects.filter(originator=local_originator).delete()
                        local_originator.delete()  # Полное удаление
                        deleted_count += 1
            
            if deleted_count > 0:
                self.stdout.write(f'  🗑️ Удалено {deleted_count} оригинаторов, которых нет в Patents Service')
            
            for i, originator_data in enumerate(patents_originators[:self.limit] if self.limit else patents_originators):
                if i % 50 == 0:
                    self.stdout.write(f'  Прогресс: {i}/{len(patents_originators)}...')
                
                try:
                    if self.dry_run:
                        self.stdout.write(f'  [DRY] Оригинатор: {originator_data.get("name", "Без названия")}')
                        self.stats['originators']['skipped'] += 1
                        continue
                    
                    originator, created = Originator.objects.get_or_create(
                        originator_id=originator_data.get('id'),
                        defaults={
                            'name': originator_data.get('name', ''),
                            'code': originator_data.get('code'),
                            'is_foreign': originator_data.get('is_foreign', False),
                            'is_nanoc': originator_data.get('is_nanoc', False),
                            'is_deleted': False,
                            'synced_at': timezone.now()
                        }
                    )
                    
                    if created:
                        self.stats['originators']['created'] += 1
                    else:
                        if (originator.name != originator_data.get('name', '') or 
                            originator.code != originator_data.get('code') or
                            originator.is_foreign != originator_data.get('is_foreign', False) or
                            originator.is_nanoc != originator_data.get('is_nanoc', False) or
                            originator.is_deleted):
                            originator.name = originator_data.get('name', '')
                            originator.code = originator_data.get('code')
                            originator.is_foreign = originator_data.get('is_foreign', False)
                            originator.is_nanoc = originator_data.get('is_nanoc', False)
                            originator.is_deleted = False
                            originator.synced_at = timezone.now()
                            originator.save()
                            self.stats['originators']['updated'] += 1
                        else:
                            self.stats['originators']['skipped'] += 1
                            
                except Exception as e:
                    self.stdout.write(f'  ❌ Ошибка оригинатора {originator_data.get("id")}: {e}')
                    self.stats['originators']['errors'] += 1
            
            self.stdout.write(f'  ✅ Оригинаторы: {self.stats["originators"]["created"]} создано, {self.stats["originators"]["updated"]} обновлено')
            
        except Exception as e:
            self.stdout.write(f'  ❌ Ошибка синхронизации оригинаторов: {e}')
    
    def sync_sorts(self):
        """Синхронизация сортов"""
        self.stdout.write('🌾 Синхронизация сортов...')
        
        try:
            patents_sorts = self.client.get_all_sorts()
            if not patents_sorts:
                self.stdout.write('  ⚠️ Не удалось получить сорта из Patents Service')
                return
            
            # Получаем ID всех сортов из Patents Service
            patents_sort_ids = {sort_data.get('id') for sort_data in patents_sorts}
            
            # Находим локальные сорта, которых нет в Patents Service
            local_sorts = SortRecord.objects.filter(is_deleted=False)
            deleted_count = 0
            
            for local_sort in local_sorts:
                if local_sort.sort_id not in patents_sort_ids:
                    if self.dry_run:
                        self.stdout.write(f'  [DRY] Удалить: {local_sort.name} (ID: {local_sort.sort_id})')
                    else:
                        # Удаляем связи с оригинаторами перед удалением сорта
                        SortOriginator.objects.filter(sort_record=local_sort).delete()
                        local_sort.delete()  # Полное удаление
                        deleted_count += 1
            
            if deleted_count > 0:
                self.stdout.write(f'  🗑️ Удалено {deleted_count} сортов, которых нет в Patents Service')
            
            for i, sort_data in enumerate(patents_sorts[:self.limit] if self.limit else patents_sorts):
                if i % 100 == 0:
                    self.stdout.write(f'  Прогресс: {i}/{len(patents_sorts)}...')
                
                try:
                    if self.dry_run:
                        self.stdout.write(f'  [DRY] Сорт: {sort_data.get("name", "Без названия")}')
                        self.stats['sorts']['skipped'] += 1
                        continue
                    
                    # Получаем культуру
                    culture = None
                    if sort_data.get('culture'):
                        culture = Culture.objects.filter(
                            culture_id=sort_data['culture'].get('id')
                        ).first()
                    
                    sort_record, created = SortRecord.objects.get_or_create(
                        sort_id=sort_data.get('id'),
                        defaults={
                            'name': sort_data.get('name', ''),
                            'culture': culture,
                            'is_deleted': False,
                            'synced_at': timezone.now()
                        }
                    )
                    
                    if created:
                        self.stats['sorts']['created'] += 1
                    else:
                        if (sort_record.name != sort_data.get('name', '') or 
                            sort_record.culture != culture or
                            sort_record.is_deleted):
                            sort_record.name = sort_data.get('name', '')
                            sort_record.culture = culture
                            sort_record.is_deleted = False
                            sort_record.synced_at = timezone.now()
                            sort_record.save()
                            self.stats['sorts']['updated'] += 1
                        else:
                            self.stats['sorts']['skipped'] += 1
                    
                    # Синхронизируем оригинаторов сорта
                    if sort_data.get('originators'):
                        # Получаем ID оригинаторов из Patents Service для этого сорта
                        patents_originator_ids = {orig.get('id') for orig in sort_data['originators']}
                        
                        # Удаляем связи с оригинаторами, которых нет в Patents Service
                        SortOriginator.objects.filter(
                            sort_record=sort_record
                        ).exclude(
                            originator__originator_id__in=patents_originator_ids
                        ).delete()
                        
                        # Создаем/обновляем связи с оригинаторами из Patents Service
                        for originator_data in sort_data['originators']:
                            originator = get_or_sync_originator(
                                originator_data.get('id'),
                                strategy=SyncStrategy.EAGER
                            )
                            if originator:
                                SortOriginator.objects.get_or_create(
                                    sort_record=sort_record,
                                    originator=originator,
                                    defaults={'percentage': 100}  # По умолчанию 100%
                                )
                            
                except Exception as e:
                    self.stdout.write(f'  ❌ Ошибка сорта {sort_data.get("id")}: {e}')
                    self.stats['sorts']['errors'] += 1
            
            self.stdout.write(f'  ✅ Сорта: {self.stats["sorts"]["created"]} создано, {self.stats["sorts"]["updated"]} обновлено')
            
        except Exception as e:
            self.stdout.write(f'  ❌ Ошибка синхронизации сортов: {e}')
    
    def print_summary(self):
        """Вывод итоговой статистики"""
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('📊 ИТОГИ СИНХРОНИЗАЦИИ'))
        self.stdout.write('='*70)
        
        total_created = sum(stats['created'] for stats in self.stats.values())
        total_updated = sum(stats['updated'] for stats in self.stats.values())
        total_skipped = sum(stats['skipped'] for stats in self.stats.values())
        total_errors = sum(stats['errors'] for stats in self.stats.values())
        
        self.stdout.write(f'🌿 Группы культур: {self.stats["group_cultures"]["created"]} создано, {self.stats["group_cultures"]["updated"]} обновлено, {self.stats["group_cultures"]["skipped"]} пропущено, {self.stats["group_cultures"]["errors"]} ошибок')
        self.stdout.write(f'🌱 Культуры: {self.stats["cultures"]["created"]} создано, {self.stats["cultures"]["updated"]} обновлено, {self.stats["cultures"]["skipped"]} пропущено, {self.stats["cultures"]["errors"]} ошибок')
        self.stdout.write(f'👥 Оригинаторы: {self.stats["originators"]["created"]} создано, {self.stats["originators"]["updated"]} обновлено, {self.stats["originators"]["skipped"]} пропущено, {self.stats["originators"]["errors"]} ошибок')
        self.stdout.write(f'🌾 Сорта: {self.stats["sorts"]["created"]} создано, {self.stats["sorts"]["updated"]} обновлено, {self.stats["sorts"]["skipped"]} пропущено, {self.stats["sorts"]["errors"]} ошибок')
        
        self.stdout.write('-'*70)
        self.stdout.write(f'📈 ВСЕГО: {total_created} создано, {total_updated} обновлено, {total_skipped} пропущено, {total_errors} ошибок')
        
        if total_errors > 0:
            self.stdout.write(self.style.WARNING(f'⚠️ Обнаружено {total_errors} ошибок'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Синхронизация завершена без ошибок'))
        
        self.stdout.write('='*70)
