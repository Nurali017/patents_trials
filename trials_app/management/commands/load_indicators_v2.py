"""
Management command для загрузки показателей испытаний (версия 2.0 - без дублей)

ПРИНЦИП: Один показатель → Несколько групп культур

Использование:
    python manage.py load_indicators_v2
    python manage.py load_indicators_v2 --dry-run
    
Обновлено: 2025-10-13
Автор: Trials System
"""

from django.core.management.base import BaseCommand
from trials_app.models import Indicator, Culture, GroupCulture


class Command(BaseCommand):
    help = 'Загрузить показатели испытаний V2 (один показатель для нескольких групп)'

    def __init__(self):
        super().__init__()
        self.missing_groups = []
        self.created_count = 0
        self.updated_count = 0
        self.cultures_linked = 0

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет создано без записи в БД',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN режим\n'))
        
        self.stdout.write('Загрузка показателей V2.0 (без дублей)...\n')
        
        # Загрузить показатели
        self.load_common_indicators()
        self.load_specific_indicators()
        
        # Итоговый отчет
        self.print_summary()

    def create_indicator(self, code, name, unit, category='common', is_quality=False, 
                        sort_order=0, group_codes=None, description='', is_auto_calculated=False, 
                        calculation_formula='', is_required=False, is_recommended=True):
        """Создать или обновить показатель с привязкой к группам"""
        if self.dry_run:
            self.stdout.write(f'  [DRY-RUN] {name} ({unit or "балл"})')
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
                'is_universal': False,
                'description': description,
                'is_numeric': True,
                'is_auto_calculated': is_auto_calculated,
                'calculation_formula': calculation_formula,
                'is_required': is_required,
                'is_recommended': is_recommended,
            }
        )
        
        if created:
            self.created_count += 1
            status = '✅ Создан'
        else:
            self.updated_count += 1
            status = '🔄 Обновлен'
        
        self.stdout.write(f'  {status}: {name} ({unit or "балл"})')
        
        # Привязать к культурам через группы
        if group_codes:
            self._link_to_groups(indicator, group_codes)
        
        return indicator

    def _link_to_groups(self, indicator, group_codes):
        """Привязать показатель к группам культур (новая логика)"""
        groups = []
        
        for group_code in group_codes:
            try:
                group = GroupCulture.objects.get(code=group_code, is_deleted=False)
                groups.append(group)
                
            except GroupCulture.DoesNotExist:
                if group_code not in self.missing_groups:
                    self.missing_groups.append(group_code)
                    self.stdout.write(
                        self.style.WARNING(f'    ⚠️  Группа "{group_code}" не найдена')
                    )
        
        if groups:
            # Привязать к группам (а не к культурам!)
            indicator.group_cultures.set(groups)
            
            # Подсчитать сколько культур получит этот показатель
            total_cultures = Culture.objects.filter(
                group_culture__in=groups,
                is_deleted=False
            ).distinct().count()
            
            self.cultures_linked += total_cultures
            self.stdout.write(
                self.style.SUCCESS(
                    f'    ✓ Привязано к группам: {[g.name for g in groups]}'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'    ✓ Охватывает культур: {total_cultures}'
                )
            )

    # ========== ОБЩИЕ ПОКАЗАТЕЛИ ==========
    
    def load_common_indicators(self):
        """Общие показатели для нескольких групп культур"""
        self.stdout.write(self.style.HTTP_INFO('\n📊 ОБЩИЕ ПОКАЗАТЕЛИ'))
        
        # 1. Урожайность (почти все группы) - ОБЯЗАТЕЛЬНЫЙ ПО МЕТОДИКЕ
        self.create_indicator(
            code='yield',
            name='Урожайность',
            unit='ц/га',
            category='common',
            is_quality=False,
            sort_order=1,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS', 'FORAGE', 'VEGETABLES', 'melons', 'FRUITS', 'BERRY'],
            description='Общий показатель урожайности для большинства культур',
            is_required=True,
            is_recommended=True
        )
        
        # 2. Отклонение от стандарта (зерновые, зернобобовые, масличные) - АВТОРАСЧЕТНЫЕ
        self.create_indicator(
            code='deviation_standard_abs',
            name='Отклонение от стандарта (абсолютное)',
            unit='ц/га',
            category='common',
            is_quality=False,
            sort_order=2,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS'],
            description='Отклонение урожайности от стандартного сорта в ц/га',
            is_auto_calculated=True,
            calculation_formula='Урожайность участника - Урожайность стандарта'
        )
        
        self.create_indicator(
            code='deviation_standard_pct',
            name='Отклонение от стандарта (%)',
            unit='%',
            category='common',
            is_quality=False,
            sort_order=3,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS'],
            description='Отклонение урожайности от стандартного сорта в процентах',
            is_auto_calculated=True,
            calculation_formula='((Урожайность участника - Урожайность стандарта) / Урожайность стандарта) × 100'
        )
        
        # 3. Вегетационный период (все группы)
        self.create_indicator(
            code='vegetation_period',
            name='Вегетационный период',
            unit='дней',
            category='common',
            is_quality=False,
            sort_order=4,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS', 'FORAGE', 'VEGETABLES', 'melons'],
            description='Период от посева/всходов до созревания'
        )
        
        # 4. Высота растений (почти все)
        self.create_indicator(
            code='plant_height',
            name='Высота растений',
            unit='см',
            category='common',
            is_quality=False,
            sort_order=5,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS', 'FORAGE'],
            description='Высота растения или стеблестоя'
        )
        
        # 5. Устойчивость к полеганию (зерновые, зернобобовые, кормовые, масличные)
        self.create_indicator(
            code='lodging_resistance',
            name='Устойчивость к полеганию',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=6,
            group_codes=['GRAIN', 'LEGUMES', 'FORAGE', 'OILSEEDS'],
            description='Устойчивость к полеганию стеблей'
        )
        
        # 6. Устойчивость к засухе (зерновые, зернобобовые, кормовые, масличные)
        self.create_indicator(
            code='drought_resistance',
            name='Устойчивость к засухе',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=7,
            group_codes=['GRAIN', 'LEGUMES', 'FORAGE', 'OILSEEDS'],
            description='Устойчивость к засушливым условиям'
        )
        
        # 7. Устойчивость к болезням и вредителям (все)
        self.create_indicator(
            code='disease_pest_resistance',
            name='Устойчивость к болезням и вредителям',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=8,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS', 'FORAGE', 'VEGETABLES', 'melons', 'FRUITS', 'BERRY'],
            description='Общая устойчивость к болезням и вредителям'
        )
        
        # 8. Зимостойкость (зерновые озимые, зернобобовые, кормовые многолетние)
        self.create_indicator(
            code='winter_hardiness',
            name='Зимостойкость',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=9,
            group_codes=['GRAIN', 'LEGUMES', 'FORAGE'],
            description='Устойчивость к зимним условиям (для озимых и многолетних)'
        )
        
        # 9. Масса 1000 зёрен/семян (зерновые, зернобобовые, кормовые, масличные)
        self.create_indicator(
            code='thousand_seed_weight',
            name='Масса 1000 зёрен/семян',
            unit='г',
            category='common',
            is_quality=False,
            sort_order=10,
            group_codes=['GRAIN', 'LEGUMES', 'FORAGE', 'OILSEEDS'],
            description='Масса 1000 семян или зёрен'
        )
        
        # 10. Общая оценка сорта (зерновые, зернобобовые, масличные)
        self.create_indicator(
            code='variety_rating',
            name='Общая оценка сорта',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=11,
            group_codes=['GRAIN', 'LEGUMES', 'OILSEEDS'],
            description='Комплексная оценка сорта'
        )
        
        # 11. Товарность (овощные, бахчевые) - АВТОРАСЧЕТНАЯ
        self.create_indicator(
            code='marketability',
            name='Товарность',
            unit='%',
            category='common',
            is_quality=False,
            sort_order=12,
            group_codes=['VEGETABLES', 'melons', 'FRUITS', 'BERRY'],
            description='Процент товарной продукции от общего урожая',
            is_auto_calculated=True,
            calculation_formula='(Товарная урожайность / Общая урожайность) × 100'
        )
        
        # 12. Дегустационная оценка (овощные, бахчевые, плодовые)
        self.create_indicator(
            code='tasting_score',
            name='Дегустационная оценка',
            unit='балл (1-5)',
            category='common',
            is_quality=False,
            sort_order=13,
            group_codes=['VEGETABLES', 'melons', 'FRUITS', 'BERRY'],
            description='Органолептическая оценка вкусовых качеств'
        )
        
        # ПОКАЗАТЕЛИ КАЧЕСТВА (общие)
        
        # 13. Содержание белка/протеина (зерновые, зернобобовые, кормовые)
        self.create_indicator(
            code='protein_content',
            name='Содержание белка/протеина',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=100,
            group_codes=['GRAIN', 'LEGUMES', 'FORAGE'],
            description='Лабораторный анализ содержания белка'
        )
        
        # 14. Содержание сухого вещества (кормовые, овощные)
        self.create_indicator(
            code='dry_matter_content',
            name='Содержание сухого вещества',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=101,
            group_codes=['FORAGE', 'VEGETABLES', 'melons'],
            description='Процент сухого вещества в общей массе'
        )
        
        # 15. Содержание витамина С (овощные, бахчевые)
        self.create_indicator(
            code='vitamin_c_content',
            name='Содержание витамина С',
            unit='мг/%',
            category='quality',
            is_quality=True,
            sort_order=102,
            group_codes=['VEGETABLES', 'melons'],
            description='Лабораторный анализ витамина С'
        )

    # ========== СПЕЦИФИЧНЫЕ ПОКАЗАТЕЛИ ==========
    
    def load_specific_indicators(self):
        """Специфичные показатели для конкретных групп"""
        self.stdout.write(self.style.HTTP_INFO('\n🎯 СПЕЦИФИЧНЫЕ ПОКАЗАТЕЛИ'))
        
        # === ЗЕРНОБОБОВЫЕ (LEGUMES) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🫘 Зернобобовые'))
        
        self.create_indicator(
            code='shedding_resistance',
            name='Устойчивость к осыпанию',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=15,
            group_codes=['LEGUMES'],
            description='Устойчивость бобов/стручков к осыпанию'
        )
        
        # === ЗЕРНОВЫЕ (GRAIN) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🌾 Зерновые'))
        
        self.create_indicator(
            code='grain_nature',
            name='Натура зерна',
            unit='г/л',
            category='common',
            is_quality=False,
            sort_order=20,
            group_codes=['GRAIN'],
            description='Объёмная масса зерна (только для зерновых)'
        )
        
        self.create_indicator(
            code='tillering',
            name='Кустистость',
            unit='шт. продуктивных стеблей',
            category='common',
            is_quality=False,
            sort_order=21,
            group_codes=['GRAIN'],
            description='Количество продуктивных стеблей на растении'
        )
        
        self.create_indicator(
            code='lodging_drooping_brittleness',
            name='Устойчивость к пониканию / ломкости колоса',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=22,
            group_codes=['GRAIN'],
            description='Устойчивость колоса к пониканию и ломкости'
        )
        
        self.create_indicator(
            code='germination_resistance',
            name='Устойчивость к прорастанию на корню',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=23,
            group_codes=['GRAIN'],
            description='Устойчивость зерна к прорастанию до уборки'
        )
        
        self.create_indicator(
            code='threshability',
            name='Обмолачиваемость',
            unit='балл (1-9)',
            category='common',
            is_quality=False,
            sort_order=24,
            group_codes=['GRAIN'],
            description='Легкость обмолота зерна'
        )
        
        # Качество зерновых
        self.create_indicator(
            code='gluten_content',
            name='Содержание клейковины',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=110,
            group_codes=['GRAIN'],
            description='Содержание клейковины (для пшеницы)'
        )
        
        self.create_indicator(
            code='vitreousness',
            name='Стекловидность',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=111,
            group_codes=['GRAIN'],
            description='Стекловидность зерна'
        )
        
        self.create_indicator(
            code='bread_volume',
            name='Объём хлеба',
            unit='мл',
            category='quality',
            is_quality=True,
            sort_order=112,
            group_codes=['GRAIN'],
            description='Объём хлеба из муки (хлебопекарное качество)'
        )
        
        self.create_indicator(
            code='baking_score',
            name='Общая хлебопекарная оценка',
            unit='балл (1-5)',
            category='quality',
            is_quality=True,
            sort_order=113,
            group_codes=['GRAIN'],
            description='Комплексная хлебопекарная оценка'
        )
        
        # === КУКУРУЗА (тоже GRAIN, но специфичные показатели) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🌽 Кукуруза (специфичные)'))
        
        self.create_indicator(
            code='ear_weight',
            name='Масса початка',
            unit='г',
            category='specific',
            is_quality=False,
            sort_order=30,
            group_codes=['GRAIN'],
            description='Средняя масса одного початка (кукуруза)'
        )
        
        self.create_indicator(
            code='grain_output',
            name='Выход зерна',
            unit='%',
            category='specific',
            is_quality=False,
            sort_order=31,
            group_codes=['GRAIN'],
            description='Процент зерна от массы початка (кукуруза)',
            is_auto_calculated=True,
            calculation_formula='(Масса зерна / Масса початка) × 100'
        )
        
        self.create_indicator(
            code='ear_attachment_height',
            name='Высота прикрепления нижнего початка',
            unit='см',
            category='specific',
            is_quality=False,
            sort_order=32,
            group_codes=['GRAIN'],
            description='Высота первого початка от земли (кукуруза)'
        )
        
        self.create_indicator(
            code='ears_per_plant',
            name='Количество початков на растении',
            unit='шт.',
            category='specific',
            is_quality=False,
            sort_order=33,
            group_codes=['GRAIN'],
            description='Число початков на одном растении (кукуруза)'
        )
        
        # === КОРМОВЫЕ (FORAGE) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🌿 Кормовые'))
        
        self.create_indicator(
            code='green_mass_yield',
            name='Урожайность зеленой массы',
            unit='ц/га',
            category='common',
            is_quality=False,
            sort_order=40,
            group_codes=['FORAGE'],
            description='Урожай зеленой (свежей) массы'
        )
        
        self.create_indicator(
            code='dry_matter_yield',
            name='Урожайность сухого вещества',
            unit='ц/га',
            category='common',
            is_quality=False,
            sort_order=41,
            group_codes=['FORAGE'],
            description='Урожай в пересчете на абсолютно сухое вещество'
        )
        
        self.create_indicator(
            code='leafiness',
            name='Облиственность',
            unit='%',
            category='common',
            is_quality=False,
            sort_order=42,
            group_codes=['FORAGE'],
            description='Доля листьев в общей массе растения'
        )
        
        # Качество кормовых
        self.create_indicator(
            code='fiber_content',
            name='Содержание клетчатки',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=120,
            group_codes=['FORAGE'],
            description='Содержание сырой клетчатки'
        )
        
        self.create_indicator(
            code='fat_content',
            name='Содержание жира',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=121,
            group_codes=['FORAGE'],
            description='Содержание сырого жира'
        )
        
        self.create_indicator(
            code='starch_content',
            name='Содержание крахмала',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=122,
            group_codes=['FORAGE'],
            description='Содержание крахмала (для силосных)'
        )
        
        # === МАСЛИЧНЫЕ (OILSEEDS) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🌻 Масличные'))
        
        self.create_indicator(
            code='seeds_per_basket',
            name='Масса семян в одной корзинке/коробочке/стручке',
            unit='г',
            category='specific',
            is_quality=False,
            sort_order=50,
            group_codes=['OILSEEDS'],
            description='Масса семян из одного соцветия/плода'
        )
        
        self.create_indicator(
            code='ripening_uniformity',
            name='Выравненность созревания',
            unit='%',
            category='common',
            is_quality=False,
            sort_order=51,
            group_codes=['OILSEEDS'],
            description='Процент одновременно созревших растений'
        )
        
        # Качество масличных
        self.create_indicator(
            code='oil_content',
            name='Содержание масла',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=130,
            group_codes=['OILSEEDS'],
            description='Масличность семян'
        )
        
        # === ОВОЩНЫЕ (VEGETABLES) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🥬 Овощные'))
        
        self.create_indicator(
            code='early_yield',
            name='Ранняя урожайность',
            unit='ц/га',
            category='common',
            is_quality=False,
            sort_order=60,
            group_codes=['VEGETABLES', 'melons'],
            description='Урожайность от первых сборов'
        )
        
        self.create_indicator(
            code='total_marketable_yield',
            name='Товарная урожайность',
            unit='ц/га',
            category='common',
            is_quality=False,
            sort_order=61,
            group_codes=['VEGETABLES'],
            description='Урожайность товарной продукции',
            is_auto_calculated=True,
            calculation_formula='Общая урожайность × (Товарность / 100)'
        )
        
        self.create_indicator(
            code='fruit_vegetable_weight',
            name='Средняя масса плода/корнеплода/кочана',
            unit='г',
            category='common',
            is_quality=False,
            sort_order=62,
            group_codes=['VEGETABLES', 'melons'],
            description='Средний вес товарного плода/корнеплода'
        )
        
        # Специфичные для картофеля/корнеплодов
        self.create_indicator(
            code='starch_content_tubers',
            name='Содержание крахмала (картофель)',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=140,
            group_codes=['VEGETABLES'],
            description='Содержание крахмала в клубнях'
        )
        
        self.create_indicator(
            code='storability',
            name='Лёжкость при хранении',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=141,
            group_codes=['VEGETABLES', 'FRUITS'],
            description='Процент сохранившейся продукции после хранения'
        )
        
        self.create_indicator(
            code='carotenoids_content',
            name='Содержание каротиноидов (морковь)',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=142,
            group_codes=['VEGETABLES'],
            description='Содержание каротиноидов (провитамин А)'
        )
        
        self.create_indicator(
            code='sugar_content_beet',
            name='Содержание сахара (свёкла)',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=143,
            group_codes=['VEGETABLES'],
            description='Содержание сахара в столовой свёкле'
        )
        
        # Специфичные для капусты/салата
        self.create_indicator(
            code='head_density',
            name='Плотность кочана',
            unit='балл (1-5)',
            category='common',
            is_quality=False,
            sort_order=63,
            group_codes=['VEGETABLES'],
            description='Плотность кочана капусты'
        )
        
        self.create_indicator(
            code='bolting_resistance',
            name='Устойчивость к цветушности',
            unit='%',
            category='common',
            is_quality=False,
            sort_order=64,
            group_codes=['VEGETABLES'],
            description='Устойчивость к преждевременному стрелкованию'
        )
        
        # Специфичные для томатов
        self.create_indicator(
            code='juice_dry_matter',
            name='Содержание сухого вещества в соке (томат)',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=144,
            group_codes=['VEGETABLES'],
            description='Сухое вещество в соке томата'
        )
        
        self.create_indicator(
            code='days_to_first_harvest',
            name='Период до первого сбора',
            unit='дней',
            category='common',
            is_quality=False,
            sort_order=65,
            group_codes=['VEGETABLES', 'melons'],
            description='От всходов до первого сбора урожая'
        )
        
        # === ПЛОДОВО-ЯГОДНЫЕ (FRUITS, BERRY) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🍎🍓 Плодово-ягодные'))
        
        self.create_indicator(
            code='fruit_berry_weight',
            name='Средняя масса плода/ягоды',
            unit='г',
            category='common',
            is_quality=False,
            sort_order=70,
            group_codes=['FRUITS', 'BERRY'],
            description='Средняя масса одного плода или ягоды'
        )
        
        # === ВИНОГРАД (FRUITS) ===
        self.stdout.write(self.style.HTTP_INFO('\n  🍇 Виноград'))
        
        self.create_indicator(
            code='sugar_content_grapes',
            name='Сахаристость (виноград)',
            unit='%',
            category='quality',
            is_quality=True,
            sort_order=150,
            group_codes=['FRUITS'],
            description='Содержание сахара в ягодах винограда'
        )

    # ========== ИТОГОВЫЙ ОТЧЕТ ==========
    
    def print_summary(self):
        """Вывести итоговый отчет"""
        self.stdout.write('\n' + '='*70)
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('\n🔍 DRY-RUN ЗАВЕРШЕН\n'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ ЗАГРУЗКА ЗАВЕРШЕНА!\n'))
            self.stdout.write(f'   📊 Показателей создано: {self.created_count}')
            self.stdout.write(f'   🔄 Показателей обновлено: {self.updated_count}')
            self.stdout.write(f'   🔗 Привязок к культурам: {self.cultures_linked}')
        
        if self.missing_groups:
            self.stdout.write(f'\n   ⚠️  Не найдено групп: {len(self.missing_groups)}')
            for code in set(self.missing_groups):
                self.stdout.write(f'      - {code}')
        
        self.stdout.write('='*70 + '\n')

