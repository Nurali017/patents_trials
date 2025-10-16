#!/usr/bin/env python
"""
Тестовый скрипт для проверки новых endpoints:
- cultures-for-region
- pending-for-region (с опциональным culture_id)

Запуск:
    python test_new_endpoints.py
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from django.test import RequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from trials_app.views import ApplicationViewSet
from trials_app.models import (
    Oblast, Region, Culture, SortRecord, Application, PlannedDistribution
)


def print_separator(title):
    """Печать разделителя"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_cultures_for_region():
    """Тест 1: GET /api/v1/applications/cultures-for-region/?region_id={id}"""
    print_separator("ТЕСТ 1: cultures-for-region endpoint")
    
    # Найти любой регион с распределениями
    region = Region.objects.filter(
        planned_distributions__isnull=False,
        is_deleted=False
    ).first()
    
    if not region:
        print("⚠️  Нет регионов с распределениями. Создайте тестовые данные.")
        return
    
    print(f"✓ Тестируем регион: {region.name} (ID: {region.id})")
    
    # Создать запрос
    factory = RequestFactory()
    request = factory.get(f'/api/v1/applications/cultures-for-region/?region_id={region.id}')
    
    # Аутентификация (если нужна)
    user = User.objects.first()
    if user:
        force_authenticate(request, user=user)
    
    # Вызвать view
    view = ApplicationViewSet.as_view({'get': 'cultures_for_region'})
    response = view(request)
    
    print(f"\n📊 Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        data = response.data
        print(f"\n✅ Успешно получены данные:")
        print(f"   Регион: {data.get('region_name')}")
        print(f"   Область: {data.get('oblast_name')}")
        print(f"   Культур найдено: {len(data.get('cultures', []))}")
        
        for culture in data.get('cultures', []):
            print(f"\n   🌾 {culture['culture_name']}:")
            print(f"      • Всего заявок: {culture['applications_count']}")
            print(f"      • Ожидают распределения: {culture['pending_count']}")
            print(f"      • Уже в испытаниях: {culture['in_trial_count']}")
            print(f"      • Примеры: {', '.join(culture['sample_applications'][:2])}")
    else:
        print(f"❌ Ошибка: {response.data}")


def test_pending_for_region_with_culture():
    """Тест 2: GET /api/v1/applications/pending-for-region/?region_id={id}&culture_id={id}"""
    print_separator("ТЕСТ 2: pending-for-region с culture_id")
    
    # Найти регион и культуру
    region = Region.objects.filter(is_deleted=False).first()
    culture = Culture.objects.filter(is_deleted=False).first()
    
    if not region or not culture:
        print("⚠️  Нет тестовых данных")
        return
    
    print(f"✓ Регион: {region.name} (ID: {region.id})")
    print(f"✓ Культура: {culture.name} (ID: {culture.id})")
    
    # Создать запрос
    factory = RequestFactory()
    request = factory.get(
        f'/api/v1/applications/pending-for-region/?region_id={region.id}&culture_id={culture.id}'
    )
    
    user = User.objects.first()
    if user:
        force_authenticate(request, user=user)
    
    view = ApplicationViewSet.as_view({'get': 'pending_for_region'})
    response = view(request)
    
    print(f"\n📊 Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        data = response.data
        print(f"\n✅ Успешно получены данные:")
        print(f"   Всего заявок: {data.get('total')}")
        print(f"   Регион: {data.get('region_name')}")
        print(f"   Культура ID: {data.get('culture_id')}")
        
        for app in data.get('applications', [])[:3]:
            print(f"\n   📋 {app['application_number']}")
            if app.get('sort_record'):
                print(f"      Сорт: {app['sort_record']['name']}")
            print(f"      Уже в испытании: {'Да' if app['already_in_trial'] else 'Нет'}")
    else:
        print(f"❌ Ошибка: {response.data}")


def test_pending_for_region_without_culture():
    """Тест 3: GET /api/v1/applications/pending-for-region/?region_id={id}"""
    print_separator("ТЕСТ 3: pending-for-region БЕЗ culture_id (все культуры)")
    
    region = Region.objects.filter(is_deleted=False).first()
    
    if not region:
        print("⚠️  Нет тестовых данных")
        return
    
    print(f"✓ Регион: {region.name} (ID: {region.id})")
    
    # Создать запрос БЕЗ culture_id
    factory = RequestFactory()
    request = factory.get(f'/api/v1/applications/pending-for-region/?region_id={region.id}')
    
    user = User.objects.first()
    if user:
        force_authenticate(request, user=user)
    
    view = ApplicationViewSet.as_view({'get': 'pending_for_region'})
    response = view(request)
    
    print(f"\n📊 Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        data = response.data
        print(f"\n✅ Успешно получены ВСЕ заявки для региона:")
        print(f"   Всего заявок: {data.get('total')}")
        print(f"   Регион: {data.get('region_name')}")
        print(f"   Культура ID: {data.get('culture_id')} (None = все культуры)")
        
        # Сгруппировать по культурам
        cultures = {}
        for app in data.get('applications', []):
            if app.get('sort_record') and app['sort_record'].get('culture_name'):
                culture_name = app['sort_record']['culture_name']
                if culture_name not in cultures:
                    cultures[culture_name] = []
                cultures[culture_name].append(app['application_number'])
        
        print(f"\n   📊 Разбивка по культурам:")
        for culture_name, apps in cultures.items():
            print(f"      • {culture_name}: {len(apps)} заявок")
    else:
        print(f"❌ Ошибка: {response.data}")


def main():
    """Запуск всех тестов"""
    print("\n" + "🧪 ТЕСТИРОВАНИЕ НОВЫХ ENDPOINTS".center(70, "="))
    print("Вариант A: Минимальные изменения")
    print("="*70)
    
    try:
        # Проверка наличия данных
        print("\n📦 Проверка наличия тестовых данных:")
        print(f"   • Областей: {Oblast.objects.filter(is_deleted=False).count()}")
        print(f"   • Регионов (ГСУ): {Region.objects.filter(is_deleted=False).count()}")
        print(f"   • Культур: {Culture.objects.filter(is_deleted=False).count()}")
        print(f"   • Заявок: {Application.objects.filter(is_deleted=False).count()}")
        print(f"   • Распределений: {PlannedDistribution.objects.filter(is_deleted=False).count()}")
        
        # Запуск тестов
        test_cultures_for_region()
        test_pending_for_region_with_culture()
        test_pending_for_region_without_culture()
        
        print_separator("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
        print("\n💡 Теперь можно тестировать через HTTP:")
        print("   GET http://localhost:8001/api/v1/applications/cultures-for-region/?region_id=1")
        print("   GET http://localhost:8001/api/v1/applications/pending-for-region/?region_id=1")
        print("   GET http://localhost:8001/api/v1/applications/pending-for-region/?region_id=1&culture_id=10")
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

