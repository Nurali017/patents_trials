#!/usr/bin/env python3
"""
Тестовый скрипт для проверки новой структуры TrialPlan API
"""

import os
import sys
import django
import json

# Настройка Django
sys.path.append('/Users/nuralisagyndykuly/patent_new/trials')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from trials_app.models import TrialPlan, Oblast, Culture, TrialType
from trials_app.serializers import TrialPlanSerializer

def test_trial_plan_serializer():
    """Тестируем новый сериализатор TrialPlan"""
    print("=== Тестирование TrialPlanSerializer ===")
    
    try:
        # Получаем первый план для тестирования
        trial_plan = TrialPlan.objects.filter(is_deleted=False).first()
        
        if not trial_plan:
            print("❌ Нет планов испытаний в базе данных")
            return
        
        print(f"✅ Найден план: ID={trial_plan.id}, Год={trial_plan.year}, Область={trial_plan.oblast.name}")
        
        # Тестируем сериализацию
        serializer = TrialPlanSerializer(trial_plan)
        data = serializer.data
        
        print("\n=== Структура ответа ===")
        print(f"ID: {data.get('id')}")
        print(f"Год: {data.get('year')}")
        
        oblast = data.get('oblast', {})
        print(f"Область ID: {oblast.get('id')}")
        print(f"Область название: {oblast.get('name')}")
        
        cultures = data.get('cultures', [])
        print(f"Количество культур: {len(cultures)}")
        
        for i, culture in enumerate(cultures):
            print(f"\n--- Культура {i+1} ---")
            print(f"  ID: {culture.get('id')}")
            print(f"  Название: {culture.get('name')}")
            print(f"  Patents ID: {culture.get('culture_id')}")
            
            trial_types = culture.get('trial_types', [])
            print(f"  Типов испытаний: {len(trial_types)}")
            
            for j, trial_type in enumerate(trial_types):
                print(f"\n  --- Тип испытания {j+1} ---")
                print(f"    ID: {trial_type.get('id')}")
                print(f"    Название: {trial_type.get('name')}")
                print(f"    Код: {trial_type.get('code')}")
                
                participants = trial_type.get('participants', [])
                print(f"    Участников: {len(participants)}")
                
                trials = trial_type.get('trials', [])
                print(f"    Испытаний: {len(trials)}")
                
                if trials:
                    print(f"    Пример испытания: region_id={trials[0].get('region_id')}, predecessor={trials[0].get('predecessor')}")
        
        print("\n✅ Сериализация прошла успешно!")
        print("\n=== JSON структура ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

def test_list_view():
    """Тестируем список планов"""
    print("\n=== Тестирование списка планов ===")
    
    try:
        plans = TrialPlan.objects.filter(is_deleted=False)[:3]  # Берем первые 3
        
        if not plans:
            print("❌ Нет планов испытаний в базе данных")
            return
        
        serializer = TrialPlanSerializer(plans, many=True)
        data = serializer.data
        
        print(f"✅ Найдено планов: {len(data)}")
        
        for i, plan in enumerate(data):
            print(f"\n--- План {i+1} ---")
            print(f"  ID: {plan.get('id')}")
            print(f"  Год: {plan.get('year')}")
            oblast = plan.get('oblast', {})
            print(f"  Область: {oblast.get('name')}")
            cultures = plan.get('cultures', [])
            print(f"  Культур: {len(cultures)}")
        
        print("✅ Список планов работает!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании списка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_trial_plan_serializer()
    test_list_view()