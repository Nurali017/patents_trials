#!/usr/bin/env python
"""Проверка культуры ID=53 и её показателей"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import Culture, Indicator

# Проверяем культуру с ID 53
try:
    culture = Culture.objects.get(id=53, is_deleted=False)
    print(f"✓ Культура ID=53: {culture.name}")

    if culture.group_culture:
        print(f"✓ Группа культур: {culture.group_culture.name}\n")

        # Получаем все показатели для этой группы культур
        all_indicators = Indicator.objects.filter(
            group_cultures=culture.group_culture,
            is_deleted=False
        ).order_by('sort_order', 'name')

        print(f"📊 Всего показателей для '{culture.group_culture.name}': {all_indicators.count()}\n")

        # Разделяем по типам (как в API)
        required = all_indicators.filter(is_required=True, is_quality=False)
        recommended = all_indicators.filter(is_recommended=True, is_required=False, is_quality=False)
        quality = all_indicators.filter(is_quality=True)

        print(f"{'='*70}")
        print(f"ОБЯЗАТЕЛЬНЫЕ ПОКАЗАТЕЛИ: {required.count()}")
        print(f"{'='*70}")
        for ind in required:
            print(f"  {ind.id:3} | {ind.code:40} | {ind.name:40} | {ind.unit or '-':10}")

        print(f"\n{'='*70}")
        print(f"РЕКОМЕНДУЕМЫЕ ПОКАЗАТЕЛИ: {recommended.count()}")
        print(f"{'='*70}")
        for ind in recommended:
            print(f"  {ind.id:3} | {ind.code:40} | {ind.name:40} | {ind.unit or '-':10}")

        print(f"\n{'='*70}")
        print(f"ПОКАЗАТЕЛИ КАЧЕСТВА: {quality.count()}")
        print(f"{'='*70}")
        for ind in quality:
            print(f"  {ind.id:3} | {ind.code:40} | {ind.name:40} | {ind.unit or '-':10}")

        # Проверяем наши добавленные показатели кукурузы
        print(f"\n{'='*70}")
        print(f"ПОКАЗАТЕЛИ КУКУРУЗЫ (добавленные нами):")
        print(f"{'='*70}")
        corn_codes = [
            'grain_moisture_at_harvest',
            'grain_yield_from_cob',
            'leaves_per_plant',
            'mature_cob_weight',
            'lower_cob_attachment_height',
            'cobs_per_plant',
            'cob_length',
            'common_smut_resistance'
        ]

        corn_indicators = all_indicators.filter(code__in=corn_codes)
        print(f"Найдено {corn_indicators.count()} из {len(corn_codes)} показателей кукурузы:")
        for ind in corn_indicators:
            quality_mark = " [КАЧЕСТВО]" if ind.is_quality else ""
            required_mark = " [ОБЯЗАТЕЛЬНЫЙ]" if ind.is_required else ""
            print(f"  ✓ {ind.code:40} | {ind.name:40} {quality_mark}{required_mark}")

        # Проверяем API endpoint
        print(f"\n{'='*70}")
        print(f"API ENDPOINT:")
        print(f"{'='*70}")
        print(f"GET https://trials.rizeup.kz/api/indicators/by-culture/53/")
        print(f"\nВернёт:")
        print(f"  - culture: {{id: 53, name: '{culture.name}', group_culture: {{id: {culture.group_culture.id}, name: '{culture.group_culture.name}'}}}}")
        print(f"  - required_indicators: {required.count()} показателей")
        print(f"  - recommended_indicators: {recommended.count()} показателей")
        print(f"  - quality_indicators: {quality.count()} показателей")
        print(f"  - total_indicators: {all_indicators.count()}")

    else:
        print(f"❌ У культуры '{culture.name}' НЕТ группы культур (group_culture=None)")
        print(f"   API вернёт пустой список показателей")

except Culture.DoesNotExist:
    print(f"❌ Культура с ID=53 не найдена в БД")
    print(f"\nДоступные культуры:")
    cultures = Culture.objects.filter(is_deleted=False)[:20]
    for cult in cultures:
        group_name = cult.group_culture.name if cult.group_culture else "БЕЗ ГРУППЫ"
        print(f"  ID={cult.id:3} | {cult.name:40} | Группа: {group_name}")
