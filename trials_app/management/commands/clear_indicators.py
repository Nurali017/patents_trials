"""
Management command для очистки показателей испытаний

Использование:
    python manage.py clear_indicators
    python manage.py clear_indicators --confirm  # Подтвердить удаление
    python manage.py clear_indicators --dry-run  # Показать что будет удалено
    
Обновлено: 2025-01-10
"""

from django.core.management.base import BaseCommand
from trials_app.models import Indicator


class Command(BaseCommand):
    help = 'Очистить все показатели испытаний'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Подтвердить удаление (без этого флага команда не выполнится)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет удалено без выполнения',
        )

    def handle(self, *args, **options):
        self.confirm = options['confirm']
        self.dry_run = options['dry_run']
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим - изменения НЕ будут выполнены\n'))
        
        # Получить все показатели
        indicators = Indicator.objects.all()
        total_count = indicators.count()
        
        if total_count == 0:
            self.stdout.write(self.style.SUCCESS('✅ Показатели уже очищены - в БД нет показателей'))
            return
        
        # Показать что будет удалено
        self.stdout.write(f'📊 Найдено показателей для удаления: {total_count}\n')
        
        if not self.dry_run:
            # Показать первые 10 показателей как пример
            self.stdout.write('Примеры показателей которые будут удалены:')
            for indicator in indicators[:10]:
                self.stdout.write(f'  - {indicator.name} ({indicator.code})')
            
            if total_count > 10:
                self.stdout.write(f'  ... и еще {total_count - 10} показателей\n')
        
        # Проверить подтверждение
        if not self.dry_run and not self.confirm:
            self.stdout.write(
                self.style.ERROR(
                    '\n❌ УДАЛЕНИЕ НЕ ПОДТВЕРЖДЕНО!\n'
                    'Для удаления всех показателей добавьте флаг --confirm:\n'
                    'python manage.py clear_indicators --confirm'
                )
            )
            return
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('\n🔍 DRY-RUN: Показатели НЕ будут удалены'))
            return
        
        # Выполнить удаление
        self.stdout.write('\n🗑️  Удаляем показатели...')
        
        deleted_count = 0
        for indicator in indicators:
            indicator.delete()  # Мягкое удаление
            deleted_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ УСПЕШНО УДАЛЕНО {deleted_count} показателей!\n'
                'Теперь можно запустить:\n'
                'python manage.py load_indicators_v2'
            )
        )
