#!/usr/bin/env python3
"""Привязка ГСУ Абай области к группе GRAIN"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import GroupCulture, Region, Oblast

# Получаем группу GRAIN
grain = GroupCulture.objects.get(code='GRAIN', is_deleted=False)
print(f"✓ Группа: {grain.name} (код: {grain.code})")

# Получаем область Абай
abay = Oblast.objects.get(name__icontains='Абай')
print(f"✓ Область: {abay.name}\n")

# Получаем все ГСУ Абай области
abay_gsu = Region.objects.filter(oblast=abay, is_deleted=False)
print(f"Найдено {abay_gsu.count()} ГСУ в области Абай:")
for region in abay_gsu:
    print(f"  - ID {region.id}: {region.name}")

print(f"\nПривязываем к группе GRAIN...")
for region in abay_gsu:
    grain.regions.add(region)
    print(f"  ✓ Привязан: {region.name}")

# Проверяем результат
total = grain.regions.filter(oblast=abay, is_deleted=False).count()
print(f"\n✅ Итого регионов GRAIN в Абай области: {total}")
