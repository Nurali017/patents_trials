#!/usr/bin/env python
"""Проверка существующих показателей в БД"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import Indicator, GroupCulture

# Все показатели
indicators = Indicator.objects.filter(is_deleted=False)
print(f"Всего показателей в системе: {indicators.count()}\n")

# Проверка группы культур "Кукуруза"
corn_group = GroupCulture.objects.filter(name__icontains='кукуруз').first()
if corn_group:
    print(f"Группа культур: {corn_group.name}")
    corn_indicators = indicators.filter(group_cultures=corn_group)
    print(f"Показателей для кукурузы: {corn_indicators.count()}\n")

    if corn_indicators.exists():
        print("Существующие показатели для кукурузы:")
        for ind in corn_indicators.order_by('sort_order'):
            quality_mark = " [КАЧЕСТВО]" if ind.is_quality else ""
            print(f"  - {ind.code}: {ind.name} ({ind.unit or 'без ед.'}){quality_mark}")
else:
    print("Группа 'Кукуруза' не найдена в БД")
    print("\nДоступные группы культур:")
    for gc in GroupCulture.objects.filter(is_deleted=False):
        print(f"  - {gc.name}")

# Универсальные показатели
universal = indicators.filter(is_universal=True)
print(f"\n\nУниверсальные показатели (применимы ко всем культурам): {universal.count()}")
for ind in universal.order_by('sort_order')[:10]:
    print(f"  - {ind.code}: {ind.name} ({ind.unit or 'без ед.'})")
