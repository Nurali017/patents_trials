"""
Management команда для проверки состояния синхронизации

Использование:
    python manage.py check_sync_health
    python manage.py check_sync_health --json  # Вывод в JSON формате
"""

from django.core.management.base import BaseCommand
from trials_app.sync_helpers import check_sync_health
import json


class Command(BaseCommand):
    help = 'Проверить состояние синхронизации с Patents Service'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            action='store_true',
            help='Вывести результат в JSON формате'
        )
    
    def handle(self, *args, **options):
        health = check_sync_health()
        
        if options['json']:
            # JSON вывод для интеграции с мониторингом
            self.stdout.write(json.dumps(health, ensure_ascii=False, indent=2))
        else:
            # Красивый вывод в консоль
            self._print_pretty(health)
    
    def _print_pretty(self, health):
        """Красивый вывод статистики"""
        self.stdout.write(self.style.HTTP_INFO('='*70))
        self.stdout.write(self.style.HTTP_INFO(' '*20 + '📊 СОСТОЯНИЕ СИНХРОНИЗАЦИИ'))
        self.stdout.write(self.style.HTTP_INFO('='*70))
        
        # Сорта
        self.stdout.write(f'\n🌾 {self.style.HTTP_INFO("СОРТА:")}')
        self.stdout.write(f'  Всего в системе:          {health["sorts"]["total"]}')
        
        if health["sorts"]["never_synced"] > 0:
            self.stdout.write(
                self.style.ERROR(f'  ✗ Не синхронизированных:  {health["sorts"]["never_synced"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Не синхронизированных:  0')
            )
        
        if health["sorts"]["outdated_week"] > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠ Устаревших (>7 дней):   {health["sorts"]["outdated_week"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Устаревших (>7 дней):   0')
            )
        
        if health["sorts"]["outdated_month"] > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠ Устаревших (>30 дней):  {health["sorts"]["outdated_month"]}')
            )
        
        # Культуры
        self.stdout.write(f'\n🌱 {self.style.HTTP_INFO("КУЛЬТУРЫ:")}')
        self.stdout.write(f'  Всего в системе:          {health["cultures"]["total"]}')
        
        if health["cultures"]["never_synced"] > 0:
            self.stdout.write(
                self.style.ERROR(f'  ✗ Не синхронизированных:  {health["cultures"]["never_synced"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Не синхронизированных:  0')
            )
        
        if health["cultures"]["outdated_month"] > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠ Устаревших (>30 дней):  {health["cultures"]["outdated_month"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Устаревших (>30 дней):  0')
            )
        
        # Оригинаторы
        self.stdout.write(f'\n👥 {self.style.HTTP_INFO("ОРИГИНАТОРЫ:")}')
        self.stdout.write(f'  Всего в системе:          {health["originators"]["total"]}')
        
        if health["originators"]["never_synced"] > 0:
            self.stdout.write(
                self.style.ERROR(f'  ✗ Не синхронизированных:  {health["originators"]["never_synced"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Не синхронизированных:  0')
            )
        
        if health["originators"]["outdated_month"] > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠ Устаревших (>30 дней):  {health["originators"]["outdated_month"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Устаревших (>30 дней):  0')
            )
        
        # Рекомендации
        self.stdout.write(f'\n💡 {self.style.HTTP_INFO("РЕКОМЕНДАЦИИ:")}')
        
        if health['recommendations']:
            for rec in health['recommendations']:
                if '⚠️' in rec or '✗' in rec:
                    self.stdout.write(self.style.WARNING(f'  {rec}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'  {rec}'))
        
        # Команды для синхронизации
        if health["sorts"]["outdated_week"] > 0 or health["sorts"]["never_synced"] > 0:
            self.stdout.write(f'\n🔧 {self.style.HTTP_INFO("КОМАНДЫ ДЛЯ СИНХРОНИЗАЦИИ:")}')
            
            if health["sorts"]["never_synced"] > 0:
                self.stdout.write(
                    '  python manage.py sync_from_patents --model=sorts'
                )
            elif health["sorts"]["outdated_week"] > 0:
                self.stdout.write(
                    '  python manage.py sync_from_patents --model=sorts --outdated-only --days=7'
                )
            
            if health["cultures"]["never_synced"] > 0 or health["cultures"]["outdated_month"] > 0:
                self.stdout.write(
                    '  python manage.py sync_from_patents --model=cultures --outdated-only --days=30'
                )
        
        self.stdout.write(self.style.HTTP_INFO('\n' + '='*70 + '\n'))

