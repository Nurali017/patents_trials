#!/usr/bin/env python3
"""
Полная синхронизация всех данных из Patents Service

Этот скрипт синхронизирует:
- Сорта (2130+ штук)
- Культуры (150 штук) 
- Группы культур (15 штук)
- Оригинаторы (связанные с сортами)

Использование:
    python full_sync_from_patents.py
    python full_sync_from_patents.py --dry-run
    python full_sync_from_patents.py --limit 100
"""

import os
import sys
import django
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from django.utils import timezone
from trials_app.patents_integration import PatentsServiceClient
from trials_app.models import SortRecord, Culture, GroupCulture, Originator, SortOriginator


class FullSyncFromPatents:
    def __init__(self, dry_run=False, limit=None):
        self.dry_run = dry_run
        self.limit = limit
        self.client = PatentsServiceClient()
        self.stats = {
            'sorts': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
            'cultures': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
            'group_cultures': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
            'originators': {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0},
        }
        
    def log(self, message, level='INFO'):
        """Логирование с временной меткой"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def sync_group_cultures(self):
        """Синхронизация групп культур"""
        self.log("🌿 Синхронизация групп культур...")
        
        patents_groups = self.client.get_all_group_cultures()
        self.log(f"Получено групп из Patents: {len(patents_groups)}")
        
        for group_data in patents_groups:
            group_id = group_data.get('id')
            name = group_data.get('name', '')
            
            if not group_id or not name:
                self.stats['group_cultures']['errors'] += 1
                continue
            
            try:
                if self.dry_run:
                    self.log(f"  [DRY] Группа: {name} (ID: {group_id})")
                    self.stats['group_cultures']['skipped'] += 1
                    continue
                
                group, created = GroupCulture.objects.get_or_create(
                    group_culture_id=group_id,
                    defaults={
                        'name': name,
                        'is_deleted': False
                    }
                )
                
                if created:
                    self.log(f"  ✅ Создана: {name} (ID: {group_id})")
                    self.stats['group_cultures']['created'] += 1
                else:
                    if group.name != name or group.is_deleted:
                        group.name = name
                        group.is_deleted = False
                        group.save()
                        self.log(f"  🔄 Обновлена: {name} (ID: {group_id})")
                        self.stats['group_cultures']['updated'] += 1
                    else:
                        self.stats['group_cultures']['skipped'] += 1
                        
            except Exception as e:
                self.log(f"  ❌ Ошибка группы {group_id}: {e}", 'ERROR')
                self.stats['group_cultures']['errors'] += 1
    
    def sync_cultures(self):
        """Синхронизация культур"""
        self.log("🌱 Синхронизация культур...")
        
        patents_cultures = self.client.get_all_cultures()
        self.log(f"Получено культур из Patents: {len(patents_cultures)}")
        
        for culture_data in patents_cultures:
            culture_id = culture_data.get('id')
            name = culture_data.get('name', '')
            
            if not culture_id or not name:
                self.stats['cultures']['errors'] += 1
                continue
            
            try:
                if self.dry_run:
                    # Показываем информацию о группе в dry-run
                    group_data = culture_data.get('group', {})
                    group_name = group_data.get('name', 'Без группы') if group_data else 'Без группы'
                    self.log(f"  [DRY] Культура: {name} (ID: {culture_id}, Группа: {group_name})")
                    self.stats['cultures']['skipped'] += 1
                    continue
                
                culture, created = Culture.objects.get_or_create(
                    culture_id=culture_id,
                    defaults={
                        'name': name,
                        'is_deleted': False,
                        'synced_at': timezone.now()
                    }
                )
                
                if created:
                    self.log(f"  ✅ Создана: {name} (ID: {culture_id})")
                    self.stats['cultures']['created'] += 1
                else:
                    if culture.name != name or culture.is_deleted:
                        culture.name = name
                        culture.is_deleted = False
                        culture.synced_at = timezone.now()
                        culture.save()
                        self.log(f"  🔄 Обновлена: {name} (ID: {culture_id})")
                        self.stats['cultures']['updated'] += 1
                    else:
                        self.stats['cultures']['skipped'] += 1
                        
            except Exception as e:
                self.log(f"  ❌ Ошибка культуры {culture_id}: {e}", 'ERROR')
                self.stats['cultures']['errors'] += 1
    
    def sync_culture_group_links(self):
        """Синхронизация связей культур с группами культур"""
        self.log("🔗 Синхронизация связей культур с группами...")
        
        patents_cultures = self.client.get_all_cultures()
        self.log(f"Получено культур из Patents: {len(patents_cultures)}")
        
        # Создаем маппинг культур к группам
        group_mapping = {}
        cultures_with_groups = 0
        
        for culture_data in patents_cultures:
            culture_id = culture_data.get('id')
            culture_name = culture_data.get('name', '')
            group_data = culture_data.get('group')  # Используем 'group' а не 'group_culture'
            
            if group_data and culture_id:
                cultures_with_groups += 1
                group_id = group_data.get('id')
                group_name = group_data.get('name', '')
                
                group_mapping[culture_id] = {
                    'group_id': group_id,
                    'group_name': group_name,
                    'culture_name': culture_name
                }
        
        self.log(f"Культур с группами: {cultures_with_groups}")
        
        # Обновляем связи в БД
        stats = {'updated': 0, 'errors': 0, 'skipped': 0}
        
        for culture_id, group_info in group_mapping.items():
            try:
                # Получаем культуру из БД
                try:
                    culture = Culture.objects.get(culture_id=culture_id, is_deleted=False)
                except Culture.DoesNotExist:
                    stats['skipped'] += 1
                    continue
                
                # Получаем группу культур из БД
                try:
                    group_culture = GroupCulture.objects.get(group_culture_id=group_info['group_id'], is_deleted=False)
                except GroupCulture.DoesNotExist:
                    stats['skipped'] += 1
                    continue
                
                # Обновляем связь
                if culture.group_culture != group_culture:
                    culture.group_culture = group_culture
                    culture.synced_at = timezone.now()
                    culture.save()
                    stats['updated'] += 1
                    if stats['updated'] <= 10:  # Показываем первые 10
                        self.log(f"  ✅ {culture.name} → {group_culture.name}")
                else:
                    stats['skipped'] += 1
                    
            except Exception as e:
                stats['errors'] += 1
                self.log(f"  ❌ Ошибка для культуры {culture_id}: {e}", 'ERROR')
        
        self.log(f"Обновлено связей: {stats['updated']}")
        self.log(f"Пропущено: {stats['skipped']}")
        self.log(f"Ошибок: {stats['errors']}")
        
        # Обновляем статистику
        self.stats['cultures']['updated'] += stats['updated']
        self.stats['cultures']['errors'] += stats['errors']
        self.stats['cultures']['skipped'] += stats['skipped']
    
    def sync_sorts(self):
        """Синхронизация сортов"""
        self.log("🌾 Синхронизация сортов...")
        
        patents_sorts = self.client.get_all_sorts()
        self.log(f"Получено сортов из Patents: {len(patents_sorts)}")
        
        # Применяем лимит если указан
        if self.limit:
            patents_sorts = patents_sorts[:self.limit]
            self.log(f"Ограничено до {self.limit} сортов")
        
        for i, sort_data in enumerate(patents_sorts, 1):
            sort_id = sort_data.get('id')
            name = sort_data.get('name', '')
            
            if not sort_id or not name:
                self.stats['sorts']['errors'] += 1
                continue
            
            # Показываем прогресс каждые 100 сортов
            if i % 100 == 0:
                self.log(f"  Прогресс: {i}/{len(patents_sorts)}...")
            
            try:
                if self.dry_run:
                    if i <= 10:  # Показываем только первые 10 в dry-run
                        culture_name = sort_data.get('culture', {}).get('name', 'Без культуры') if sort_data.get('culture') else 'Без культуры'
                        self.log(f"  [DRY] {i:2d}. {name} (ID: {sort_id}, Культура: {culture_name})")
                    self.stats['sorts']['skipped'] += 1
                    continue
                
                # Получаем культуру
                culture_id = sort_data.get('culture', {}).get('id') if sort_data.get('culture') else None
                culture = None
                if culture_id:
                    try:
                        culture = Culture.objects.get(culture_id=culture_id, is_deleted=False)
                    except Culture.DoesNotExist:
                        self.log(f"  ⚠️  Культура {culture_id} не найдена для сорта {name}", 'WARNING')
                
                # Создаем или обновляем сорт
                sort_record, created = SortRecord.objects.get_or_create(
                    sort_id=sort_id,
                    defaults={
                        'name': name,
                        'culture': culture,
                        'is_deleted': False,
                        'synced_at': timezone.now()
                    }
                )
                
                if created:
                    if i <= 10:  # Показываем только первые 10
                        self.log(f"  ✅ {i:2d}. Создан: {name} (ID: {sort_id})")
                    self.stats['sorts']['created'] += 1
                else:
                    # Обновляем если нужно
                    updated = False
                    if sort_record.name != name:
                        sort_record.name = name
                        updated = True
                    if sort_record.culture != culture:
                        sort_record.culture = culture
                        updated = True
                    if sort_record.is_deleted:
                        sort_record.is_deleted = False
                        updated = True
                    
                    if updated:
                        sort_record.synced_at = timezone.now()
                        sort_record.save()
                        if i <= 10:
                            self.log(f"  🔄 {i:2d}. Обновлен: {name} (ID: {sort_id})")
                        self.stats['sorts']['updated'] += 1
                    else:
                        self.stats['sorts']['skipped'] += 1
                        
            except Exception as e:
                self.log(f"  ❌ Ошибка сорта {sort_id}: {e}", 'ERROR')
                self.stats['sorts']['errors'] += 1
    
    def sync_originators_from_sorts(self):
        """Синхронизация оригинаторов из сортов"""
        self.log("👥 Синхронизация оригинаторов из сортов...")
        
        # Получаем все сорта с оригинаторами
        patents_sorts = self.client.get_all_sorts()
        
        if self.limit:
            patents_sorts = patents_sorts[:self.limit]
        
        # Статистика
        sorts_processed = 0
        
        for i, sort_data in enumerate(patents_sorts, 1):
            sort_id = sort_data.get('id')
            sort_name = sort_data.get('name', '')
            
            if not sort_id:
                continue
            
            # Получаем оригинаторов для этого сорта (поле называется 'ariginators' с опечаткой)
            ariginators_data = sort_data.get('ariginators', [])
            
            if not ariginators_data:
                continue
            
            sorts_processed += 1
            
            # Показываем прогресс каждые 500 сортов
            if sorts_processed % 500 == 0:
                self.log(f"  Прогресс: {sorts_processed} сортов с оригинаторами обработано...")
            
            try:
                # Получаем SortRecord
                try:
                    sort_record = SortRecord.objects.get(sort_id=sort_id, is_deleted=False)
                except SortRecord.DoesNotExist:
                    continue
                
                for ariginator_data in ariginators_data:
                    # Извлекаем данные оригинатора из структуры ariginators
                    ariginator_info = ariginator_data.get('ariginator', {})
                    originator_id = ariginator_info.get('id')
                    originator_name = ariginator_info.get('name', '')
                    percentage = ariginator_data.get('percentage', 0)
                    
                    if not originator_id or not originator_name:
                        continue
                    
                    if self.dry_run:
                        if sorts_processed <= 5:  # Показываем только первые 5 в dry-run
                            self.log(f"  [DRY] Оригинатор: {originator_name} для {sort_name} ({percentage}%)")
                        self.stats['originators']['skipped'] += 1
                        continue
                    
                    # Создаем или получаем оригинатора
                    originator, created = Originator.objects.get_or_create(
                        originator_id=originator_id,
                        defaults={
                            'name': originator_name,
                            'is_deleted': False,
                            'synced_at': timezone.now()
                        }
                    )
                    
                    if created:
                        self.stats['originators']['created'] += 1
                        if sorts_processed <= 10:  # Показываем первые 10
                            self.log(f"  ✅ Создан оригинатор: {originator_name}")
                    else:
                        if originator.name != originator_name or originator.is_deleted:
                            originator.name = originator_name
                            originator.is_deleted = False
                            originator.synced_at = timezone.now()
                            originator.save()
                            self.stats['originators']['updated'] += 1
                        else:
                            self.stats['originators']['skipped'] += 1
                    
                    # Создаем связь SortOriginator
                    sort_originator, created = SortOriginator.objects.get_or_create(
                        sort_record=sort_record,
                        originator=originator,
                        defaults={'percentage': percentage}
                    )
                    
                    if created:
                        self.stats['originators']['created'] += 1
                        if sorts_processed <= 10:  # Показываем первые 10
                            self.log(f"  🔗 Связь: {sort_name} → {originator_name} ({percentage}%)")
                    elif sort_originator.percentage != percentage:
                        sort_originator.percentage = percentage
                        sort_originator.save()
                        self.stats['originators']['updated'] += 1
                        
            except Exception as e:
                self.log(f"  ❌ Ошибка оригинаторов для сорта {sort_id}: {e}", 'ERROR')
                self.stats['originators']['errors'] += 1
        
        self.log(f"Обработано сортов с оригинаторами: {sorts_processed}")
    
    def sync_originators(self):
        """Синхронизация оригинаторов из отдельного endpoint"""
        self.log("👥 Синхронизация оригинаторов...")
        
        patents_originators = self.client.get_all_originators()
        self.log(f"Получено оригинаторов из Patents: {len(patents_originators)}")
        
        for i, originator_data in enumerate(patents_originators, 1):
            originator_id = originator_data.get('id')
            name = originator_data.get('name', '')
            
            if not originator_id or not name:
                self.stats['originators']['errors'] += 1
                continue
            
            # Показываем прогресс каждые 100 оригинаторов
            if i % 100 == 0:
                self.log(f"  Прогресс: {i}/{len(patents_originators)}...")
            
            try:
                if self.dry_run:
                    if i <= 10:  # Показываем только первые 10 в dry-run
                        self.log(f"  [DRY] Оригинатор: {name} (ID: {originator_id})")
                    self.stats['originators']['skipped'] += 1
                    continue
                
                originator, created = Originator.objects.get_or_create(
                    originator_id=originator_id,
                    defaults={
                        'name': name,
                        'country': originator_data.get('country', ''),
                        'is_nanoc': originator_data.get('is_nanoc', False),
                        'is_deleted': False,
                        'synced_at': timezone.now()
                    }
                )

                if created:
                    if i <= 10:  # Показываем только первые 10
                        self.log(f"  ✅ {i:2d}. Создан: {name} (ID: {originator_id})")
                    self.stats['originators']['created'] += 1
                else:
                    new_country = originator_data.get('country', '')
                    new_is_nanoc = originator_data.get('is_nanoc', False)
                    if (originator.name != name or originator.country != new_country or
                            originator.is_nanoc != new_is_nanoc or originator.is_deleted):
                        originator.name = name
                        originator.country = new_country
                        originator.is_nanoc = new_is_nanoc
                        originator.is_deleted = False
                        originator.synced_at = timezone.now()
                        originator.save()  # is_foreign пересчитается в save()
                        if i <= 10:
                            self.log(f"  🔄 {i:2d}. Обновлен: {name} (ID: {originator_id})")
                        self.stats['originators']['updated'] += 1
                    else:
                        self.stats['originators']['skipped'] += 1
                        
            except Exception as e:
                self.log(f"  ❌ Ошибка оригинатора {originator_id}: {e}", 'ERROR')
                self.stats['originators']['errors'] += 1
    
    def print_summary(self):
        """Вывод итоговой статистики"""
        self.log("=" * 80)
        self.log("📊 ИТОГОВАЯ СТАТИСТИКА СИНХРОНИЗАЦИИ")
        self.log("=" * 80)
        
        for data_type, stats in self.stats.items():
            if any(stats.values()):
                self.log(f"\n{data_type.upper()}:")
                if stats['created'] > 0:
                    self.log(f"  ✅ Создано: {stats['created']}")
                if stats['updated'] > 0:
                    self.log(f"  🔄 Обновлено: {stats['updated']}")
                if stats['skipped'] > 0:
                    self.log(f"  ⊘ Пропущено: {stats['skipped']}")
                if stats['errors'] > 0:
                    self.log(f"  ❌ Ошибок: {stats['errors']}")
        
        # Итоговые цифры в БД
        self.log(f"\n📈 ИТОГО В БД:")
        self.log(f"  Сортов: {SortRecord.objects.filter(is_deleted=False).count()}")
        self.log(f"  Культур: {Culture.objects.filter(is_deleted=False).count()}")
        self.log(f"  Групп культур: {GroupCulture.objects.filter(is_deleted=False).count()}")
        self.log(f"  Оригинаторов: {Originator.objects.filter(is_deleted=False).count()}")
        self.log(f"  Связей SortOriginator: {SortOriginator.objects.count()}")
        
        self.log("=" * 80)
        if self.dry_run:
            self.log("🔍 DRY-RUN ЗАВЕРШЕН - изменения не были сохранены")
        else:
            self.log("✅ ПОЛНАЯ СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!")
    
    def run(self):
        """Запуск полной синхронизации"""
        start_time = datetime.now()
        
        if self.dry_run:
            self.log("🔍 ЗАПУСК В РЕЖИМЕ DRY-RUN")
        else:
            self.log("🚀 ЗАПУСК ПОЛНОЙ СИНХРОНИЗАЦИИ")
        
        self.log(f"Время начала: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. Синхронизация групп культур
            self.sync_group_cultures()
            
            # 2. Синхронизация культур
            self.sync_cultures()
            
            # 3. Синхронизация связей культур с группами
            self.sync_culture_group_links()
            
            # 4. Синхронизация сортов
            self.sync_sorts()
            
            # 5. Синхронизация оригинаторов из отдельного endpoint
            self.sync_originators()
            
            # 6. Синхронизация связей сортов с оригинаторами
            self.sync_originators_from_sorts()
            
        except Exception as e:
            self.log(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}", 'ERROR')
            raise
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.log(f"Время завершения: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Длительность: {duration}")
        
        self.print_summary()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Полная синхронизация данных из Patents Service')
    parser.add_argument('--dry-run', action='store_true', help='Показать что будет синхронизировано без выполнения')
    parser.add_argument('--limit', type=int, help='Ограничить количество сортов для синхронизации')
    
    args = parser.parse_args()
    
    sync = FullSyncFromPatents(dry_run=args.dry_run, limit=args.limit)
    sync.run()


if __name__ == '__main__':
    main()
