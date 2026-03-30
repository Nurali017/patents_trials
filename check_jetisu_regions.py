#!/usr/bin/env python3
"""Проверка регионов Жетісу области"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import Oblast, Region, GroupCulture

# Находим область Жетісу
jetisu = Oblast.objects.filter(name__icontains='Жетісу').first()

if not jetisu:
    print("❌ Область Жетісу не найдена")
    exit(1)

print("="*70)
print(f"ОБЛАСТЬ: {jetisu.name} (ID: {jetisu.id})")
print("="*70)

# Все ГСУ в области
all_regions = Region.objects.filter(oblast=jetisu, is_deleted=False)
print(f"\nВсего ГСУ в области: {all_regions.count()}")
for region in all_regions:
    print(f"  - ID {region.id}: {region.name}")

# Группа GRAIN
grain = GroupCulture.objects.get(code='GRAIN', is_deleted=False)
print(f"\n{'='*70}")
print(f"ГРУППА КУЛЬТУР: {grain.name} (код: {grain.code})")
print("="*70)

# ГСУ группы GRAIN в Жетісу
grain_regions = grain.regions.filter(oblast=jetisu, is_deleted=False)
print(f"\nПривязано к GRAIN в Жетісу: {grain_regions.count()}")
for region in grain_regions:
    print(f"  ✓ ID {region.id}: {region.name}")

# Проверяем что используется в коде summary_service.py
print(f"\n{'='*70}")
print("ЧТО ДОЛЖЕН ВОЗВРАЩАТЬ КОД:")
print("="*70)
print(f"total_regions = grain.regions.filter(oblast=jetisu).count() = {grain_regions.count()}")
print(f"Если 0, то fallback: Region.objects.filter(oblast=jetisu).count() = {all_regions.count()}")
