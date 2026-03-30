#!/usr/bin/env python3
"""Проверка связей regions для сорта ЭН ТАЙГЕТА"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import SortRecord, Culture, GroupCulture, Region, Oblast

print("="*70)
print("ПОИСК СОРТА ЭН ТАЙГЕТА")
print("="*70)

# Ищем сорт
sort_record = SortRecord.objects.filter(
    name__icontains='TAYGETA',
    is_deleted=False
).select_related('culture__group_culture').first()

if not sort_record:
    print("❌ Сорт не найден")
    exit(1)

print(f"✓ Найден сорт: {sort_record.name}")
print(f"  ID: {sort_record.id}")
print(f"  Культура: {sort_record.culture.name if sort_record.culture else 'НЕТ'}")

if sort_record.culture:
    culture = sort_record.culture
    print(f"\n{'='*70}")
    print(f"КУЛЬТУРА: {culture.name}")
    print(f"{'='*70}")

    if culture.group_culture:
        gc = culture.group_culture
        print(f"✓ Группа культур: {gc.name}")
        print(f"  ID: {gc.id}")
        print(f"  Код: {gc.code}")

        # Проверяем все регионы этой группы культур
        print(f"\n{'='*70}")
        print(f"ВСЕ РЕГИОНЫ ГРУППЫ '{gc.name}':")
        print(f"{'='*70}")

        all_regions = gc.regions.filter(is_deleted=False).select_related('oblast')
        print(f"Всего регионов: {all_regions.count()}")

        for region in all_regions:
            oblast_name = region.oblast.name if region.oblast else 'Без области'
            print(f"  - ID {region.id}: {region.name} ({oblast_name})")

        # Проверяем регионы для области Абай
        print(f"\n{'='*70}")
        print(f"РЕГИОНЫ ГРУППЫ '{gc.name}' В АБАЙ ОБЛАСТИ:")
        print(f"{'='*70}")

        abay_oblast = Oblast.objects.filter(name__icontains='Абай').first()
        if abay_oblast:
            print(f"Область Абай ID: {abay_oblast.id}, Название: {abay_oblast.name}")

            abay_regions = gc.regions.filter(
                oblast=abay_oblast,
                is_deleted=False
            )
            print(f"\nРегионов группы '{gc.code}' в Абай: {abay_regions.count()}")
            for region in abay_regions:
                print(f"  ✓ ID {region.id}: {region.name}")

            # Все ГСУ в Абай области
            all_abay_gsu = Region.objects.filter(
                oblast=abay_oblast,
                is_deleted=False
            )
            print(f"\nВсего ГСУ в Абай области: {all_abay_gsu.count()}")
            for region in all_abay_gsu:
                is_linked = '✓' if region in abay_regions else '✗'
                print(f"  {is_linked} ID {region.id}: {region.name}")
        else:
            print("❌ Область Абай не найдена")
    else:
        print("❌ У культуры НЕТ группы культур")
else:
    print("❌ У сорта НЕТ культуры")
