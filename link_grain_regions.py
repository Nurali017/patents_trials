#!/usr/bin/env python
"""
Скрипт для связывания регионов ГСУ с группой культур GRAIN (Зерновые)
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import GroupCulture, Region

def link_grain_regions():
    """Связывает ГСУ регионы Абай области с группой GRAIN"""

    # Получаем группу культур GRAIN
    try:
        grain_group = GroupCulture.objects.get(code='GRAIN', is_deleted=False)
        print(f"✅ Найдена группа культур: {grain_group.name} (код: {grain_group.code})")
    except GroupCulture.DoesNotExist:
        print("❌ Группа культур GRAIN не найдена")
        return

    # Получаем все ГСУ регионы Абай области
    abay_gsu_regions = Region.objects.filter(
        oblast__name__icontains='Абай',
        is_deleted=False
    ).exclude(
        name__icontains='область'  # Исключаем саму область
    )

    print(f"\n📍 Найдено ГСУ регионов в Абай области: {abay_gsu_regions.count()}")
    for region in abay_gsu_regions:
        print(f"  - ID {region.id}: {region.name}")

    # Связываем регионы с группой культур
    print(f"\n🔗 Связываем регионы с группой {grain_group.name}...")

    linked_count = 0
    for region in abay_gsu_regions:
        # Проверяем, не связан ли уже
        if grain_group.regions.filter(id=region.id).exists():
            print(f"  ⚠️  Регион '{region.name}' уже связан")
        else:
            grain_group.regions.add(region)
            print(f"  ✅ Связан регион '{region.name}'")
            linked_count += 1

    # Проверяем результат
    total_linked = grain_group.regions.filter(is_deleted=False).count()
    print(f"\n✨ Готово! Всего регионов связано с GRAIN: {total_linked}")
    print(f"   Добавлено новых связей: {linked_count}")

    # Показываем все связанные регионы
    print(f"\n📋 Все регионы группы {grain_group.name}:")
    for region in grain_group.regions.filter(is_deleted=False):
        oblast_name = region.oblast.name if region.oblast else 'Без области'
        print(f"  - ID {region.id}: {region.name} ({oblast_name})")

if __name__ == '__main__':
    print("🌾 Связывание ГСУ регионов с группой GRAIN\n")
    link_grain_regions()
    print("\n✅ Скрипт завершен")
