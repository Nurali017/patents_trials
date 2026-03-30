#!/usr/bin/env python
"""
Добавление показателей для кукурузы в БД
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import Indicator, GroupCulture

# Получаем группу "Зерновые культуры"
grain_crops = GroupCulture.objects.filter(name='Зерновые культуры').first()
if not grain_crops:
    print("❌ Группа 'Зерновые культуры' не найдена!")
    exit(1)

print(f"✓ Группа культур: {grain_crops.name}\n")

# Показатели кукурузы
corn_indicators = [
    {
        'code': 'grain_moisture_at_harvest',
        'name': 'Влажность зерна при уборке',
        'unit': '%',
        'category': 'quality',
        'is_quality': True,
        'is_numeric': True,
        'is_required': True,
        'description': 'Влажность зерна кукурузы на момент уборки урожая',
        'validation_rules': {
            'min_value': 0,
            'max_value': 100,
            'precision': 1
        },
        'sort_order': 10
    },
    {
        'code': 'thousand_seed_weight',
        'name': 'Масса 1000 зерен',
        'unit': 'г',
        'category': 'quality',
        'is_quality': True,
        'is_numeric': True,
        'is_required': True,
        'description': 'Масса 1000 зерен кукурузы в граммах',
        'validation_rules': {
            'min_value': 0,
            'max_value': 1000,
            'precision': 1
        },
        'sort_order': 11
    },
    {
        'code': 'grain_yield_from_cob',
        'name': 'Выход зерна при обмолоте початка',
        'unit': '%',
        'category': 'quality',
        'is_quality': True,
        'is_numeric': True,
        'is_required': True,
        'description': 'Процент выхода зерна при обмолоте початка кукурузы',
        'validation_rules': {
            'min_value': 0,
            'max_value': 100,
            'precision': 1
        },
        'sort_order': 12
    },
    {
        'code': 'leaves_per_plant',
        'name': 'Число листьев на 1 растении',
        'unit': 'шт',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': False,
        'is_recommended': True,
        'description': 'Количество листьев на одном растении кукурузы',
        'validation_rules': {
            'min_value': 0,
            'max_value': 50,
            'precision': 0
        },
        'sort_order': 13
    },
    {
        'code': 'mature_cob_weight',
        'name': 'Масса зрелого початка',
        'unit': 'г',
        'category': 'quality',
        'is_quality': True,
        'is_numeric': True,
        'is_required': True,
        'description': 'Масса зрелого початка кукурузы в граммах',
        'validation_rules': {
            'min_value': 0,
            'max_value': 1000,
            'precision': 1
        },
        'sort_order': 14
    },
    {
        'code': 'lodging_resistance',
        'name': 'Устойчивость к полеганию',
        'unit': 'балл',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': True,
        'description': 'Устойчивость кукурузы к полеганию (балльная оценка 1-5)',
        'validation_rules': {
            'min_value': 1,
            'max_value': 5,
            'precision': 0
        },
        'sort_order': 15
    },
    {
        'code': 'vegetation_period',
        'name': 'Вегетационный период',
        'unit': 'дни',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': True,
        'description': 'Длительность вегетационного периода кукурузы в днях',
        'validation_rules': {
            'min_value': 0,
            'max_value': 365,
            'precision': 0
        },
        'sort_order': 16
    },
    {
        'code': 'plant_height',
        'name': 'Высота растений',
        'unit': 'см',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': True,
        'description': 'Высота растений кукурузы в сантиметрах',
        'validation_rules': {
            'min_value': 0,
            'max_value': 500,
            'precision': 0
        },
        'sort_order': 17
    },
    {
        'code': 'lower_cob_attachment_height',
        'name': 'Высота прикрепления нижнего початка',
        'unit': 'см',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': True,
        'description': 'Высота прикрепления нижнего початка от земли в сантиметрах',
        'validation_rules': {
            'min_value': 0,
            'max_value': 300,
            'precision': 0
        },
        'sort_order': 18
    },
    {
        'code': 'cobs_per_plant',
        'name': 'Количество початков на 1 растении',
        'unit': 'шт',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': True,
        'description': 'Количество початков на одном растении кукурузы',
        'validation_rules': {
            'min_value': 0,
            'max_value': 10,
            'precision': 0
        },
        'sort_order': 19
    },
    {
        'code': 'cob_length',
        'name': 'Длина початка',
        'unit': 'см',
        'category': 'quality',
        'is_quality': True,
        'is_numeric': True,
        'is_required': True,
        'description': 'Длина початка кукурузы в сантиметрах',
        'validation_rules': {
            'min_value': 0,
            'max_value': 50,
            'precision': 1
        },
        'sort_order': 20
    },
    {
        'code': 'common_smut_resistance',
        'name': 'Пузырчатая головня',
        'unit': 'балл',
        'category': 'common',
        'is_quality': False,
        'is_numeric': True,
        'is_required': True,
        'description': 'Устойчивость к пузырчатой головне (балльная оценка 1-5)',
        'validation_rules': {
            'min_value': 1,
            'max_value': 5,
            'precision': 0
        },
        'sort_order': 21
    }
]

print("📊 Добавление показателей для кукурузы:\n")

added_count = 0
updated_count = 0
skipped_count = 0

for ind_data in corn_indicators:
    code = ind_data['code']

    # Проверяем, существует ли показатель
    existing = Indicator.objects.filter(code=code, is_deleted=False).first()

    if existing:
        # Обновляем существующий показатель
        for key, value in ind_data.items():
            if key != 'code':
                setattr(existing, key, value)

        # Добавляем связь с группой культур
        if grain_crops not in existing.group_cultures.all():
            existing.group_cultures.add(grain_crops)

        existing.save()
        print(f"✓ Обновлен: {code} - {ind_data['name']}")
        updated_count += 1
    else:
        # Создаем новый показатель
        indicator = Indicator.objects.create(**ind_data)
        indicator.group_cultures.add(grain_crops)
        print(f"+ Добавлен: {code} - {ind_data['name']}")
        added_count += 1

print(f"\n{'='*60}")
print(f"✅ Итого:")
print(f"   Добавлено новых: {added_count}")
print(f"   Обновлено: {updated_count}")
print(f"   Всего обработано: {len(corn_indicators)}")
print(f"{'='*60}\n")

# Показываем все показатели для зерновых культур
all_grain_indicators = Indicator.objects.filter(
    group_cultures=grain_crops,
    is_deleted=False
).order_by('sort_order')

print(f"📋 Все показатели для '{grain_crops.name}' ({all_grain_indicators.count()}):\n")
for ind in all_grain_indicators:
    quality_mark = " [КАЧЕСТВО]" if ind.is_quality else ""
    required_mark = " [ОБЯЗАТЕЛЬНЫЙ]" if ind.is_required else ""
    print(f"  {ind.code:40} - {ind.name:50} ({ind.unit or 'без ед.'}){quality_mark}{required_mark}")
