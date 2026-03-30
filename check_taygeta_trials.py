#!/usr/bin/env python3
"""Проверка где реально тестируется ЭН ТАЙГЕТА"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import SortRecord, Trial

# Ищем сорт
sort_record = SortRecord.objects.filter(
    name__icontains='TAYGETA',
    is_deleted=False
).first()

if not sort_record:
    print("❌ Сорт не найден")
    exit(1)

print("="*70)
print(f"СОРТ: {sort_record.name}")
print("="*70)

# Получаем все испытания этого сорта через TrialParticipant
trials = Trial.objects.filter(
    participants__sort_record=sort_record,
    is_deleted=False
).select_related('region__oblast').distinct().order_by('year')

print(f"\nВсего испытаний: {trials.count()}")

if trials.count() == 0:
    print("❌ Нет испытаний для этого сорта")
    exit(1)

# Группируем по областям
oblasts_regions = {}
for trial in trials:
    if trial.region and trial.region.oblast:
        oblast_name = trial.region.oblast.name
        region_name = trial.region.name

        if oblast_name not in oblasts_regions:
            oblasts_regions[oblast_name] = {
                'oblast_id': trial.region.oblast.id,
                'regions': set(),
                'years': set()
            }

        oblasts_regions[oblast_name]['regions'].add(region_name)
        oblasts_regions[oblast_name]['years'].add(trial.year)

print("\n" + "="*70)
print("ОБЛАСТИ И РЕГИОНЫ ГДЕ ТЕСТИРУЕТСЯ СОРТ:")
print("="*70)

for oblast_name, data in sorted(oblasts_regions.items()):
    print(f"\n📍 {oblast_name} (ID: {data['oblast_id']})")
    print(f"   Регионов: {len(data['regions'])}")
    for region in sorted(data['regions']):
        print(f"     - {region}")
    print(f"   Годы испытаний: {sorted(data['years'])}")

# Проверяем группу культур
if sort_record.culture and sort_record.culture.group_culture:
    gc = sort_record.culture.group_culture
    print(f"\n" + "="*70)
    print(f"ГРУППА КУЛЬТУР: {gc.name} (код: {gc.code})")
    print("="*70)

    # Для каждой области проверяем сколько ГСУ привязано к группе
    for oblast_name, data in sorted(oblasts_regions.items()):
        from trials_app.models import Oblast
        oblast = Oblast.objects.get(id=data['oblast_id'])

        # Регионы группы в этой области
        group_regions = gc.regions.filter(oblast=oblast, is_deleted=False)
        print(f"\n{oblast_name}:")
        print(f"  Тестируется в регионах: {len(data['regions'])}")
        print(f"  Привязано к группе {gc.code}: {group_regions.count()}")

        if group_regions.count() == 0:
            print(f"  ⚠️ ПРОБЛЕМА: Нет привязанных регионов!")
