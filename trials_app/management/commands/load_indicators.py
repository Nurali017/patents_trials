"""
Management command для загрузки показателей испытаний

Использование:
    python manage.py load_indicators
    python manage.py load_indicators --strict  # Прервать при отсутствии культуры
    python manage.py load_indicators --dry-run # Показать что будет создано
    
Обновлено: 2025-10-13
Основано на методике испытаний сельскохозяйственных культур
"""

from django.core.management.base import BaseCommand
from trials_app.models import Indicator, Culture, GroupCulture


class Command(BaseCommand):
    help = 'Загрузить показатели испытаний для различных культур (обновленная версия)'

    def __init__(self):
        super().__init__()
        self.missing_cultures = []
        self.missing_groups = []
        self.created_count = 0
        self.updated_count = 0
        self.cultures_linked = 0

    def add_arguments(self, parser):
        parser.add_argument(
            '--strict',
            action='store_true',
            help='Прервать выполнение если культура не найдена',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет создано без записи в БД',
        )

    def handle(self, *args, **options):
        self.strict = options['strict']
        self.dry_run = options['dry_run']
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим - изменения не будут сохранены\n'))
        
        self.stdout.write('Загрузка показателей испытаний (обновленная версия)...\n')
        
        # Загрузить показатели по категориям
        self.load_cereals_indicators()
        self.load_legumes_indicators()
        self.load_corn_grain_indicators()
        self.load_corn_silage_indicators()
        self.load_forage_feed_indicators()
        self.load_forage_seed_indicators()
        self.load_oilseeds_indicators()
        self.load_potato_indicators()
        self.load_root_crops_indicators()
        self.load_vegetables_tomato_indicators()
        self.load_vegetables_cabbage_indicators()
        self.load_melons_indicators()
        self.load_fruit_berry_indicators()
        self.load_grape_indicators()
        
        # Итоговый отчет
        self.print_summary()

    def create_indicator(self, code, name, unit, category='common', is_quality=False, 
                        sort_order=0, is_universal=False, culture_codes=None, 
                        group_codes=None, description=''):
        """
        Создать или обновить показатель
        
        Args:
            code: Уникальный код
            name: Название
            unit: Единица измерения
            category: common/quality/specific
            is_quality: Показатель качества
            sort_order: Порядок сортировки
            is_universal: Применим ко всем культурам
            culture_codes: Список кодов конкретных культур
            group_codes: Список кодов групп культур
            description: Описание
        """
        if self.dry_run:
            self.stdout.write(f'  [DRY-RUN] {name} ({unit or "без ед."})')
            return None
        
        # Создать или обновить показатель
        indicator, created = Indicator.objects.update_or_create(
            code=code,
            defaults={
                'name': name,
                'unit': unit,
                'category': category,
                'is_quality': is_quality,
                'sort_order': sort_order,
                'is_universal': is_universal,
                'description': description,
                'is_numeric': True,
            }
        )
        
        if created:
            self.created_count += 1
            status = '✅ Создан'
        else:
            self.updated_count += 1
            status = '🔄 Обновлен'
        
        self.stdout.write(f'  {status}: {name} ({unit or "балл"})')
        
        # Привязать к культурам
        if not is_universal:
            self._link_cultures(indicator, culture_codes, group_codes)
        
        return indicator

    def _link_cultures(self, indicator, culture_codes=None, group_codes=None):
        """Привязать показатель к культурам"""
        cultures_to_add = []
        
        # По кодам конкретных культур
        if culture_codes:
            for code in culture_codes:
                try:
                    culture = Culture.objects.get(code=code, is_deleted=False)
                    cultures_to_add.append(culture)
                except Culture.DoesNotExist:
                    self._handle_missing_culture(code)
        
        # По кодам групп культур
        if group_codes:
            for group_code in group_codes:
                try:
                    group = GroupCulture.objects.get(code=group_code, is_deleted=False)
                    group_cultures = Culture.objects.filter(
                        group_culture=group,
                        is_deleted=False
                    )
                    cultures_to_add.extend(list(group_cultures))
                    
                    if not group_cultures.exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'    ⚠️  Группа "{group.name}" найдена, но культур в ней нет'
                            )
                        )
                except GroupCulture.DoesNotExist:
                    self._handle_missing_group(group_code)
        
        # Добавить культуры к показателю
        if cultures_to_add:
            indicator.cultures.add(*cultures_to_add)
            self.cultures_linked += len(cultures_to_add)
            self.stdout.write(
                self.style.SUCCESS(f'    ✓ Привязано культур: {len(cultures_to_add)}')
            )

    def _handle_missing_culture(self, code):
        """Обработать отсутствующую культуру"""
        self.missing_cultures.append(code)
        msg = f'    ⚠️  Культура с кодом "{code}" не найдена в БД'
        
        if self.strict:
            self.stdout.write(self.style.ERROR(msg))
            raise Exception(f'Культура {code} не найдена (strict mode)')
        else:
            self.stdout.write(self.style.WARNING(msg))

    def _handle_missing_group(self, code):
        """Обработать отсутствующую группу"""
        self.missing_groups.append(code)
        msg = f'    ⚠️  Группа культур с кодом "{code}" не найдена в БД'
        
        if self.strict:
            self.stdout.write(self.style.ERROR(msg))
            raise Exception(f'Группа {code} не найдена (strict mode)')
        else:
            self.stdout.write(self.style.WARNING(msg))

    # ========== ЗЕРНОВЫЕ И КРУПЯНЫЕ ==========
    
    def load_cereals_indicators(self):
        """Показатели для зерновых и крупяных культур"""
        self.stdout.write(self.style.HTTP_INFO('\n🌾 Зерновые и крупяные'))
        
        # Основные показатели
        common_indicators = [
            ('cereals_yield', 'Урожайность', 'ц/га', 'common', False, 1),
            ('cereals_deviation_standard', 'Отклонение от стандарта (ц/га)', 'ц/га', 'common', False, 2),
            ('cereals_deviation_standard_pct', 'Отклонение от стандарта (%)', '%', 'common', False, 3),
            ('cereals_1000_grain_weight', 'Масса 1000 зерен', 'г', 'common', False, 4),
            ('cereals_lodging_resistance', 'Устойчивость к полеганию / пониканию / ломкости', 'балл (1-9)', 'common', False, 5),
            ('cereals_drought_resistance', 'Устойчивость к засухе', 'балл (1-9)', 'common', False, 6),
            ('cereals_disease_resistance', 'Устойчивость к болезням и вредителям', 'балл (1-9)', 'common', False, 7),
            ('cereals_germination_resistance', 'Устойчивость к прорастанию на корню', 'балл (1-9)', 'common', False, 8),
            ('cereals_winter_hardiness', 'Зимостойкость', 'балл (1-9)', 'common', False, 9),
            ('cereals_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 10),
            ('cereals_plant_height', 'Высота растений', 'см', 'common', False, 11),
            ('cereals_tillering', 'Кустистость', 'шт. продуктивных стеблей', 'common', False, 12),
            ('cereals_grain_nature', 'Натура зерна', 'г/л', 'common', False, 13),
            ('cereals_threshability', 'Обмолачиваемость', 'балл (1-9)', 'common', False, 14),
            ('cereals_variety_rating', 'Общая оценка сорта', 'балл (1-9)', 'common', False, 15),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('cereals_protein', 'Содержание белка', '%', 'quality', True, 100),
            ('cereals_gluten', 'Содержание клейковины', '%', 'quality', True, 101),
            ('cereals_vitreousness', 'Стекловидность', '%', 'quality', True, 102),
            ('cereals_bread_volume', 'Объём хлеба', 'мл', 'quality', True, 103),
            ('cereals_baking_score', 'Общая хлебопекарная оценка', 'балл (1-5)', 'quality', True, 104),
        ]
        
        # Создаем показатели
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['GRAIN'],  # Код группы зерновых (из Patents Service)
                description='Показатель для зерновых и крупяных культур'
            )

    # ========== ЗЕРНОБОБОВЫЕ ==========
    
    def load_legumes_indicators(self):
        """Показатели для зернобобовых"""
        self.stdout.write(self.style.HTTP_INFO('\n🫘 Зернобобовые'))
        
        # Основные показатели
        common_indicators = [
            ('legumes_yield', 'Урожайность', 'ц/га', 'common', False, 20),
            ('legumes_deviation_standard', 'Отклонение от стандарта (ц/га)', 'ц/га', 'common', False, 21),
            ('legumes_deviation_standard_pct', 'Отклонение от стандарта (%)', '%', 'common', False, 22),
            ('legumes_1000_grain_weight', 'Масса 1000 зёрен', 'г', 'common', False, 23),
            ('legumes_plant_height', 'Высота растений / стеблестоя', 'см', 'common', False, 24),
            ('legumes_lodging_resistance', 'Устойчивость к полеганию / осыпанию', 'балл (1-9)', 'common', False, 25),
            ('legumes_drought_resistance', 'Устойчивость к засухе', 'балл (1-9)', 'common', False, 26),
            ('legumes_disease_resistance', 'Устойчивость к болезням и вредителям', 'балл (1-9)', 'common', False, 27),
            ('legumes_winter_hardiness', 'Зимостойкость', 'балл (1-9)', 'common', False, 28),
            ('legumes_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 29),
            ('legumes_variety_rating', 'Общая оценка сорта', 'балл (1-9)', 'common', False, 30),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('legumes_protein', 'Содержание белка', '%', 'quality', True, 120),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['LEGUMES'],  # Код группы из Patents Service
                description='Показатель для зернобобовых культур'
            )

    # ========== КУКУРУЗА НА ЗЕРНО ==========
    
    def load_corn_grain_indicators(self):
        """Показатели для кукурузы на зерно"""
        self.stdout.write(self.style.HTTP_INFO('\n🌽 Кукуруза (на зерно)'))
        
        indicators = [
            ('corn_grain_yield', 'Урожайность', 'ц/га', 'common', False, 40),
            ('corn_grain_deviation_standard', 'Отклонение от стандарта (ц/га)', 'ц/га', 'common', False, 41),
            ('corn_grain_deviation_standard_pct', 'Отклонение от стандарта (%)', '%', 'common', False, 42),
            ('corn_grain_1000_grain_weight', 'Масса 1000 зерен', 'г', 'common', False, 43),
            ('corn_grain_ear_weight', 'Масса початка', 'г', 'common', False, 44),
            ('corn_grain_output', 'Выход зерна', '%', 'common', False, 45),
            ('corn_grain_plant_height', 'Высота растений', 'см', 'common', False, 46),
            ('corn_grain_lower_ear_height', 'Высота прикрепления нижнего початка', 'см', 'common', False, 47),
            ('corn_grain_ears_per_plant', 'Количество початков на растении', 'шт.', 'common', False, 48),
            ('corn_grain_lodging_drought_resistance', 'Устойчивость к полеганию и засухе', 'балл (1-9)', 'common', False, 49),
            ('corn_grain_disease_pest_damage', 'Поражаемость болезнями и вредителями', '%', 'common', False, 50),
            ('corn_grain_days_to_maturity', 'Вегетационный период (до восковой спелости)', 'дней', 'common', False, 51),
        ]
        
        for code, name, unit, category, is_quality, sort_order in indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['GRAIN'],  # Кукуруза тоже относится к зерновым
                description='Показатель для кукурузы на зерно'
            )

    # ========== КУКУРУЗА НА СИЛОС ==========
    
    def load_corn_silage_indicators(self):
        """Показатели для кукурузы на силос"""
        self.stdout.write(self.style.HTTP_INFO('\n🌽 Кукуруза (на силос)'))
        
        # Основные показатели
        common_indicators = [
            ('corn_silage_green_mass_yield', 'Урожайность зеленой массы', 'ц/га', 'common', False, 60),
            ('corn_silage_dry_matter_yield', 'Урожайность сухого вещества (нормализованного)', 'ц/га', 'common', False, 61),
            ('corn_silage_leafiness', 'Облиственность', '%', 'common', False, 62),
            ('corn_silage_plant_height', 'Высота растений', 'см', 'common', False, 63),
            ('corn_silage_lodging_drought_resistance', 'Устойчивость к полеганию и засухе', 'балл (1-9)', 'common', False, 64),
            ('corn_silage_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 65),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('corn_silage_dry_matter_content', 'Содержание сухого вещества', '%', 'quality', True, 140),
            ('corn_silage_protein', 'Содержание белка', '%', 'quality', True, 141),
            ('corn_silage_fat', 'Содержание жира', '%', 'quality', True, 142),
            ('corn_silage_starch', 'Содержание крахмала', '%', 'quality', True, 143),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['FORAGE'],  # Кукуруза на силос = кормовая
                description='Показатель для кукурузы на силос'
            )

    # ========== КОРМОВЫЕ КУЛЬТУРЫ (НА КОРМ) ==========
    
    def load_forage_feed_indicators(self):
        """Показатели для кормовых культур на зеленый корм / сено"""
        self.stdout.write(self.style.HTTP_INFO('\n🌿 Кормовые культуры (на зеленый корм / сено)'))
        
        indicators = [
            ('forage_feed_green_mass_yield', 'Урожайность зеленой массы', 'ц/га', 'common', False, 80),
            ('forage_feed_dry_matter_yield', 'Урожайность абсолютного сухого вещества', 'ц/га', 'common', False, 81),
            ('forage_feed_leafiness', 'Облиственность', '%', 'common', False, 82),
            ('forage_feed_plant_height', 'Высота растений', 'см', 'common', False, 83),
            ('forage_feed_lodging_drought_resistance', 'Устойчивость к полеганию и засухе', 'балл (1-9)', 'common', False, 84),
            ('forage_feed_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 85),
        ]
        
        for code, name, unit, category, is_quality, sort_order in indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['FORAGE'],
                description='Показатель для кормовых культур (зеленый корм / сено)'
            )

    # ========== КОРМОВЫЕ КУЛЬТУРЫ (НА СЕМЕНА) ==========
    
    def load_forage_seed_indicators(self):
        """Показатели для кормовых культур на семена"""
        self.stdout.write(self.style.HTTP_INFO('\n🌿 Кормовые культуры (на семена)'))
        
        # Основные показатели
        common_indicators = [
            ('forage_seed_yield', 'Урожайность семян', 'ц/га', 'common', False, 100),
            ('forage_seed_1000_grain_weight', 'Масса 1000 зёрен', 'г', 'common', False, 101),
            ('forage_seed_plant_height', 'Высота растений', 'см', 'common', False, 102),
            ('forage_seed_lodging_shedding_drought_resistance', 'Устойчивость к полеганию / осыпанию / засухе', 'балл (1-9)', 'common', False, 103),
            ('forage_seed_winter_hardiness', 'Зимостойкость', 'балл (1-9)', 'common', False, 104),
            ('forage_seed_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 105),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('forage_seed_protein', 'Содержание протеина', '%', 'quality', True, 160),
            ('forage_seed_fiber', 'Содержание клетчатки', '%', 'quality', True, 161),
            ('forage_seed_dry_matter', 'Содержание сухого вещества', '%', 'quality', True, 162),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['FORAGE'],
                description='Показатель для кормовых культур (семена)'
            )

    # ========== МАСЛИЧНЫЕ ==========
    
    def load_oilseeds_indicators(self):
        """Показатели для масличных культур (Подсолнечник, рапс, соя и др.)"""
        self.stdout.write(self.style.HTTP_INFO('\n🌻 Масличные'))
        
        indicators = [
            ('oilseeds_yield', 'Урожайность', 'ц/га', 'common', False, 120),
            ('oilseeds_deviation_standard', 'Отклонение от стандарта (ц/га)', 'ц/га', 'common', False, 121),
            ('oilseeds_deviation_standard_pct', 'Отклонение от стандарта (%)', '%', 'common', False, 122),
            ('oilseeds_1000_seed_weight', 'Масса 1000 семян', 'г', 'common', False, 123),
            ('oilseeds_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 124),
            ('oilseeds_plant_height', 'Высота растений', 'см', 'common', False, 125),
            ('oilseeds_lodging_drought_resistance', 'Устойчивость к полеганию и засухе', 'балл (1-9)', 'common', False, 126),
            ('oilseeds_disease_pest_resistance', 'Устойчивость к болезням и вредителям', 'балл (1-9)', 'common', False, 127),
            ('oilseeds_basket_seed_weight', 'Масса семян в одной корзинке/коробочке/стручке', 'г', 'common', False, 128),
            ('oilseeds_ripening_uniformity', 'Выравненность созревания', '%', 'common', False, 129),
            ('oilseeds_variety_rating', 'Общая оценка сорта', 'балл (1-9)', 'common', False, 130),
        ]
        
        for code, name, unit, category, is_quality, sort_order in indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['OILSEEDS'],
                description='Показатель для масличных культур'
            )

    # ========== КАРТОФЕЛЬ ==========
    
    def load_potato_indicators(self):
        """Показатели для картофеля"""
        self.stdout.write(self.style.HTTP_INFO('\n🥔 Картофель'))
        
        # Основные показатели
        common_indicators = [
            ('potato_total_yield', 'Общая урожайность', 'ц/га', 'common', False, 140),
            ('potato_marketable_yield', 'Товарная урожайность', 'ц/га', 'common', False, 141),
            ('potato_marketability', 'Товарность', '%', 'common', False, 142),
            ('potato_tuber_weight', 'Средняя масса одного клубня', 'г', 'common', False, 143),
            ('potato_disease_pest_damage', 'Поражаемость болезнями и вредителями', '%', 'common', False, 144),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('potato_starch', 'Содержание крахмала', '%', 'quality', True, 180),
            ('potato_storability', 'Лёжкость при хранении', '%', 'quality', True, 181),
            ('potato_vitamin_c', 'Содержание витамина С', 'мг/%', 'quality', True, 182),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['VEGETABLES'],  # Картофель = овощная культура
                description='Показатель для картофеля'
            )

    # ========== КОРНЕПЛОДЫ ==========
    
    def load_root_crops_indicators(self):
        """Показатели для корнеплодов (морковь, свёкла и др.)"""
        self.stdout.write(self.style.HTTP_INFO('\n🥕 Корнеплоды'))
        
        # Основные показатели
        common_indicators = [
            ('root_crops_total_yield', 'Общая урожайность', 'ц/га', 'common', False, 150),
            ('root_crops_marketable_yield', 'Товарная урожайность', 'ц/га', 'common', False, 151),
            ('root_crops_marketability', 'Товарность', '%', 'common', False, 152),
            ('root_crops_root_weight', 'Средняя масса одного корнеплода', 'г', 'common', False, 153),
            ('root_crops_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 154),
            ('root_crops_tasting_score', 'Дегустационная оценка', 'балл (1-5)', 'common', False, 155),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('root_crops_storability', 'Лёжкость при хранении', '%', 'quality', True, 190),
            ('root_crops_carotenoids', 'Содержание каротиноидов (для моркови)', '%', 'quality', True, 191),
            ('root_crops_sugar', 'Содержание сахара (для свёклы)', '%', 'quality', True, 192),
            ('root_crops_dry_matter', 'Содержание сухого вещества', '%', 'quality', True, 193),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['VEGETABLES'],  # Корнеплоды = овощи
                description='Показатель для корнеплодов'
            )
    
    # ========== ОВОЩНЫЕ (ТОМАТ, ПЕРЕЦ, БАКЛАЖАН) ==========
    
    def load_vegetables_tomato_indicators(self):
        """Показатели для томата, перца, баклажана"""
        self.stdout.write(self.style.HTTP_INFO('\n🍅 Томат, перец, баклажан'))
        
        # Основные показатели
        common_indicators = [
            ('tomato_early_yield', 'Ранняя урожайность', 'ц/га', 'common', False, 160),
            ('tomato_total_yield', 'Общая урожайность', 'ц/га', 'common', False, 161),
            ('tomato_marketability', 'Товарность', '%', 'common', False, 162),
            ('tomato_fruit_weight', 'Средняя масса одного плода', 'г', 'common', False, 163),
            ('tomato_days_to_first_harvest', 'Вегетационный период до 1-го сбора', 'дней', 'common', False, 164),
            ('tomato_tasting_score', 'Дегустационная оценка', 'балл (1-5)', 'common', False, 165),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('tomato_dry_matter', 'Содержание сухого вещества', '%', 'quality', True, 200),
            ('tomato_vitamin_c', 'Содержание витамина С', 'мг/%', 'quality', True, 201),
            ('tomato_juice_dry_matter', 'Содержание сухого вещества в соке (для томата)', '%', 'quality', True, 202),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['VEGETABLES'],
                description='Показатель для томата, перца, баклажана'
            )
    
    # ========== ОВОЩНЫЕ (КАПУСТА, САЛАТ) ==========
    
    def load_vegetables_cabbage_indicators(self):
        """Показатели для капусты и салата"""
        self.stdout.write(self.style.HTTP_INFO('\n🥬 Капуста, салат'))
        
        # Основные показатели
        common_indicators = [
            ('cabbage_early_yield', 'Ранняя урожайность', 'ц/га', 'common', False, 170),
            ('cabbage_total_yield', 'Общая урожайность', 'ц/га', 'common', False, 171),
            ('cabbage_head_weight', 'Средняя масса кочана / растения', 'г', 'common', False, 172),
            ('cabbage_marketability', 'Товарность', '%', 'common', False, 173),
            ('cabbage_density', 'Плотность кочана', 'балл (1-5)', 'common', False, 174),
            ('cabbage_bolting_resistance', 'Устойчивость к цветушности', '%', 'common', False, 175),
            ('cabbage_vegetation_period', 'Вегетационный период', 'дней', 'common', False, 176),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('cabbage_dry_matter', 'Содержание сухого вещества', '%', 'quality', True, 210),
            ('cabbage_vitamin_c', 'Содержание витамина С', 'мг/%', 'quality', True, 211),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['VEGETABLES'],
                description='Показатель для капусты и салата'
            )
    
    # ========== БАХЧЕВЫЕ (АРБУЗ, ДЫНЯ) ==========
    
    def load_melons_indicators(self):
        """Показатели для бахчевых культур (арбуз, дыня)"""
        self.stdout.write(self.style.HTTP_INFO('\n🍉 Бахчевые (арбуз, дыня)'))
        
        # Основные показатели
        common_indicators = [
            ('melons_early_yield', 'Ранняя урожайность', 'ц/га', 'common', False, 180),
            ('melons_total_yield', 'Общая урожайность', 'ц/га', 'common', False, 181),
            ('melons_fruit_weight', 'Средняя масса одного плода', 'кг', 'common', False, 182),
            ('melons_marketability', 'Товарность', '%', 'common', False, 183),
            ('melons_days_to_first_harvest', 'Вегетационный период до 1-го сбора', 'дней', 'common', False, 184),
            ('melons_tasting_score', 'Дегустационная оценка', 'балл (1-5)', 'common', False, 185),
        ]
        
        # Показатели качества
        quality_indicators = [
            ('melons_dry_matter', 'Содержание сухого вещества / сахаров', '%', 'quality', True, 220),
            ('melons_vitamin_c', 'Содержание витамина С', 'мг/%', 'quality', True, 221),
        ]
        
        for code, name, unit, category, is_quality, sort_order in common_indicators + quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['melons'],  # Бахчевые культуры
                description='Показатель для бахчевых культур'
            )

    # ========== ПЛОДОВО-ЯГОДНЫЕ И ВИНОГРАД ==========
    
    def load_fruit_berry_indicators(self):
        """Показатели для плодово-ягодных культур и винограда"""
        self.stdout.write(self.style.HTTP_INFO('\n🍎🍓 Плодово-ягодные культуры'))
        
        indicators = [
            ('fruit_yield', 'Урожайность', 'ц/га, кг/куст', 'common', False, 250),
            ('fruit_marketability', 'Товарность', '%', 'common', False, 251),
            ('fruit_avg_weight', 'Средняя масса одного плода/грозди', 'г', 'common', False, 252),
            ('fruit_tasting_score', 'Дегустационная оценка', 'балл (1-5)', 'common', False, 253),
            ('fruit_disease_pest_resistance', 'Устойчивость к болезням и вредителям', 'балл (1-9)', 'common', False, 254),
            ('fruit_storability', 'Лёжкость (для винограда, яблок)', 'дней, %', 'common', False, 255),
        ]
        
        for code, name, unit, category, is_quality, sort_order in indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['FRUITS', 'BERRY'],  # Плодовые и ягодные из Patents
                description='Показатель для плодовых и ягодных культур'
            )
    
    # ========== ВИНОГРАД ==========
    
    def load_grape_indicators(self):
        """Показатели для винограда"""
        self.stdout.write(self.style.HTTP_INFO('\n🍇 Виноград'))
        
        # Показатели качества (специфичные для винограда)
        quality_indicators = [
            ('grape_sugar_content', 'Сахаристость (для винограда)', '%', 'quality', True, 260),
        ]
        
        for code, name, unit, category, is_quality, sort_order in quality_indicators:
            self.create_indicator(
                code=code,
                name=name,
                unit=unit,
                category=category,
                is_quality=is_quality,
                sort_order=sort_order,
                group_codes=['FRUITS'],  # Виноград входит в плодовые
                description='Специфический показатель качества для винограда'
            )

    # ========== ИТОГОВЫЙ ОТЧЕТ ==========
    
    def print_summary(self):
        """Вывести итоговый отчет"""
        self.stdout.write('\n' + '='*70)
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('\n🔍 DRY-RUN ЗАВЕРШЕН - изменения НЕ сохранены\n'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ ЗАГРУЗКА ЗАВЕРШЕНА!\n'))
            self.stdout.write(f'   📊 Показателей создано: {self.created_count}')
            self.stdout.write(f'   🔄 Показателей обновлено: {self.updated_count}')
            self.stdout.write(f'   🔗 Привязок к культурам: {self.cultures_linked}')
        
        # Предупреждения
        if self.missing_cultures:
            self.stdout.write(f'\n   ⚠️  Не найдено культур: {len(self.missing_cultures)}')
            self.stdout.write('      Коды отсутствующих культур:')
            for code in set(self.missing_cultures):
                self.stdout.write(f'      - {code}')
        
        if self.missing_groups:
            self.stdout.write(f'\n   ⚠️  Не найдено групп: {len(self.missing_groups)}')
            self.stdout.write('      Коды отсутствующих групп:')
            for code in set(self.missing_groups):
                self.stdout.write(f'      - {code}')
        
        if self.missing_cultures or self.missing_groups:
            self.stdout.write(
                self.style.WARNING(
                    '\n   💡 Совет: Сначала загрузите культуры и группы культур,'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '      затем запустите эту команду снова для привязки показателей.'
                )
            )
        
        self.stdout.write('='*70 + '\n')




