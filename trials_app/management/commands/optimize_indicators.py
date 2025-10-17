"""
Management command для оптимизации показателей

1. Удаляет избыточные показатели
2. Помечает обязательные по методике
3. Настраивает валидацию

Использование:
    python manage.py optimize_indicators
    python manage.py optimize_indicators --confirm  # Подтвердить удаление
    python manage.py optimize_indicators --dry-run  # Показать что будет изменено
    
Обновлено: 2025-01-10
"""

from django.core.management.base import BaseCommand
from trials_app.models import Indicator


class Command(BaseCommand):
    help = 'Оптимизировать показатели: удалить избыточные, пометить обязательные'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Подтвердить удаление избыточных показателей',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет изменено без выполнения',
        )

    def handle(self, *args, **options):
        self.confirm = options['confirm']
        self.dry_run = options['dry_run']
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим - изменения НЕ будут выполнены\n'))
        
        self.stdout.write('🔧 ОПТИМИЗАЦИЯ ПОКАЗАТЕЛЕЙ...\n')
        
        # 1. Удалить избыточные показатели
        self.remove_redundant_indicators()
        
        # 2. Пометить обязательные показатели
        self.mark_required_indicators()
        
        # 3. Настроить валидацию
        self.setup_validation_rules()
        
        # 4. Пометить субъективные как нерекомендуемые
        self.mark_subjective_indicators()
        
        # Итоговый отчет
        self.print_summary()

    def remove_redundant_indicators(self):
        """Удалить избыточные показатели"""
        self.stdout.write(self.style.HTTP_INFO('🗑️ УДАЛЕНИЕ ИЗБЫТОЧНЫХ ПОКАЗАТЕЛЕЙ'))
        
        # Показатели для удаления
        redundant_codes = [
            'head_density',           # Плотность кочана - слишком специфично
            'ripening_uniformity',    # Выравненность созревания - сложно измерить
            'bolting_resistance',     # Устойчивость к цветушности - редко используется
        ]
        
        indicators_to_remove = Indicator.objects.filter(
            code__in=redundant_codes,
            is_deleted=False
        )
        
        if not indicators_to_remove.exists():
            self.stdout.write('  ✅ Избыточные показатели уже удалены')
            return
        
        self.stdout.write(f'  📊 Найдено избыточных показателей: {indicators_to_remove.count()}')
        
        for indicator in indicators_to_remove:
            self.stdout.write(f'  - {indicator.name} ({indicator.code})')
        
        if not self.dry_run and not self.confirm:
            self.stdout.write(
                self.style.ERROR(
                    '\n❌ УДАЛЕНИЕ НЕ ПОДТВЕРЖДЕНО!\n'
                    'Для удаления добавьте флаг --confirm:\n'
                    'python manage.py optimize_indicators --confirm'
                )
            )
            return
        
        if self.dry_run:
            self.stdout.write('  🔍 DRY-RUN: Показатели НЕ будут удалены')
            return
        
        # Удаляем показатели
        deleted_count = 0
        for indicator in indicators_to_remove:
            indicator.delete()  # Мягкое удаление
            deleted_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'  ✅ Удалено {deleted_count} избыточных показателей')
        )

    def mark_required_indicators(self):
        """Пометить обязательные показатели по методике"""
        self.stdout.write(self.style.HTTP_INFO('\n📋 ПОМЕТКА ОБЯЗАТЕЛЬНЫХ ПОКАЗАТЕЛЕЙ'))
        
        # Обязательные показатели по официальной методике
        required_indicators = [
            'yield',                    # Урожайность
            'thousand_seed_weight',     # Масса 1000 семян
            'grain_nature',             # Натура зерна
            'threshability',            # Обмолачиваемость
            'lodging_drooping_brittleness',  # Поникание/ломкость колоса
            'shedding_resistance',      # Осыпаемость
            'protein_content',          # Содержание белка
            'vitreousness',             # Стекловидность
            'green_mass_yield',         # Урожай зеленой массы
            'dry_matter_yield',         # Урожай сухого вещества
            'dry_matter_content',       # Содержание сухого вещества
            'fruit_vegetable_weight',   # Средняя масса плода
            'starch_content_tubers',    # Содержание крахмала
            'storability',              # Лёжкость
            'fruit_berry_weight',       # Средняя масса плода/ягоды
        ]
        
        updated_count = 0
        for code in required_indicators:
            try:
                indicator = Indicator.objects.get(code=code, is_deleted=False)
                if not indicator.is_required:
                    if not self.dry_run:
                        indicator.is_required = True
                        indicator.save()
                    self.stdout.write(f'  ✅ {indicator.name} - помечен как обязательный')
                    updated_count += 1
                else:
                    self.stdout.write(f'  ✓ {indicator.name} - уже помечен как обязательный')
            except Indicator.DoesNotExist:
                self.stdout.write(f'  ⚠️ Показатель {code} не найден')
        
        if not self.dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'  📋 Помечено обязательных показателей: {updated_count}')
            )

    def setup_validation_rules(self):
        """Настроить правила валидации для показателей"""
        self.stdout.write(self.style.HTTP_INFO('\n🔍 НАСТРОЙКА ВАЛИДАЦИИ'))
        
        # Правила валидации по типам показателей
        validation_rules = {
            # Процентные показатели
            'marketability': {'min_value': 0, 'max_value': 100, 'precision': 1},
            'deviation_standard_pct': {'min_value': -100, 'max_value': 1000, 'precision': 1},
            'protein_content': {'min_value': 0, 'max_value': 50, 'precision': 1},
            'gluten_content': {'min_value': 0, 'max_value': 50, 'precision': 1},
            'vitreousness': {'min_value': 0, 'max_value': 100, 'precision': 1},
            
            # Балльные показатели
            'variety_rating': {'min_value': 1, 'max_value': 9, 'precision': 0},
            'tasting_score': {'min_value': 1, 'max_value': 5, 'precision': 1},
            'lodging_resistance': {'min_value': 1, 'max_value': 9, 'precision': 0},
            'drought_resistance': {'min_value': 1, 'max_value': 9, 'precision': 0},
            
            # Урожайность
            'yield': {'min_value': 0, 'max_value': 1000, 'precision': 1},
            'green_mass_yield': {'min_value': 0, 'max_value': 2000, 'precision': 1},
            
            # Масса
            'thousand_seed_weight': {'min_value': 1, 'max_value': 1000, 'precision': 1},
            'fruit_vegetable_weight': {'min_value': 1, 'max_value': 50000, 'precision': 1},
            
            # Периоды
            'vegetation_period': {'min_value': 30, 'max_value': 365, 'precision': 0},
            'days_to_first_harvest': {'min_value': 30, 'max_value': 365, 'precision': 0},
        }
        
        updated_count = 0
        for code, rules in validation_rules.items():
            try:
                indicator = Indicator.objects.get(code=code, is_deleted=False)
                if not self.dry_run:
                    indicator.validation_rules = rules
                    indicator.save()
                self.stdout.write(f'  ✅ {indicator.name} - настроена валидация')
                updated_count += 1
            except Indicator.DoesNotExist:
                self.stdout.write(f'  ⚠️ Показатель {code} не найден')
        
        if not self.dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'  🔍 Настроена валидация для {updated_count} показателей')
            )

    def mark_subjective_indicators(self):
        """Пометить субъективные показатели как нерекомендуемые"""
        self.stdout.write(self.style.HTTP_INFO('\n🎭 ПОМЕТКА СУБЪЕКТИВНЫХ ПОКАЗАТЕЛЕЙ'))
        
        # Субъективные показатели
        subjective_codes = [
            'variety_rating',      # Общая оценка сорта
            'tasting_score',       # Дегустационная оценка
        ]
        
        updated_count = 0
        for code in subjective_codes:
            try:
                indicator = Indicator.objects.get(code=code, is_deleted=False)
                if indicator.is_recommended:
                    if not self.dry_run:
                        indicator.is_recommended = False
                        indicator.save()
                    self.stdout.write(f'  ✅ {indicator.name} - помечен как субъективный (нерекомендуемый)')
                    updated_count += 1
                else:
                    self.stdout.write(f'  ✓ {indicator.name} - уже помечен как субъективный')
            except Indicator.DoesNotExist:
                self.stdout.write(f'  ⚠️ Показатель {code} не найден')
        
        if not self.dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'  🎭 Помечено субъективных показателей: {updated_count}')
            )

    def print_summary(self):
        """Вывести итоговый отчет"""
        self.stdout.write('\n' + '='*70)
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('\n🔍 DRY-RUN ЗАВЕРШЕН\n'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!\n'))
            
            # Статистика
            total = Indicator.objects.filter(is_deleted=False).count()
            required = Indicator.objects.filter(is_required=True, is_deleted=False).count()
            recommended = Indicator.objects.filter(is_recommended=True, is_deleted=False).count()
            auto_calc = Indicator.objects.filter(is_auto_calculated=True, is_deleted=False).count()
            with_validation = Indicator.objects.exclude(validation_rules={}).filter(is_deleted=False).count()
            
            self.stdout.write(f'   📊 Всего показателей: {total}')
            self.stdout.write(f'   📋 Обязательных: {required}')
            self.stdout.write(f'   ✅ Рекомендуемых: {recommended}')
            self.stdout.write(f'   🤖 Авторасчетных: {auto_calc}')
            self.stdout.write(f'   🔍 С валидацией: {with_validation}')
        
        self.stdout.write('='*70 + '\n')
