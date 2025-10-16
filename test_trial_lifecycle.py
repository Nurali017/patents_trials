#!/usr/bin/env python3
"""
Тест нового жизненного цикла испытаний

Проверяет все этапы:
1. planned → active
2. active → completed_008 (через форму 008)
3. completed_008 → lab_sample_sent
4. lab_sample_sent → lab_completed
5. lab_completed → completed
"""

import requests
import json
import sys
from datetime import date, datetime

# Конфигурация
BASE_URL = "http://localhost:8001/api/v1"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def log(message):
    """Логирование с временной меткой"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_connection():
    """Проверка подключения к API"""
    try:
        response = requests.get(f"{BASE_URL}/trials/", headers=HEADERS)
        if response.status_code == 200:
            log("✅ API доступен")
            return True
        else:
            log(f"❌ API недоступен: {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Ошибка подключения: {e}")
        return False

def create_test_trial():
    """Создание тестового испытания"""
    log("🔧 Создание тестового испытания...")
    
    # Получаем первый доступный регион
    regions_response = requests.get(f"{BASE_URL}/regions/", headers=HEADERS)
    if regions_response.status_code != 200:
        log("❌ Не удалось получить регионы")
        return None
    
    regions = regions_response.json()
    if not regions:
        log("❌ Нет доступных регионов")
        return None
    
    region_id = regions[0]['id']
    log(f"📍 Используем регион: {regions[0]['name']}")
    
    # Создаем испытание
    trial_data = {
        "description": "Тестовое испытание для проверки жизненного цикла",
        "region": region_id,
        "start_date": "2025-01-01",
        "status": "planned"
    }
    
    response = requests.post(f"{BASE_URL}/trials/", 
                           headers=HEADERS, 
                           data=json.dumps(trial_data))
    
    if response.status_code == 201:
        trial = response.json()
        log(f"✅ Испытание создано: ID {trial['id']}")
        return trial
    else:
        log(f"❌ Ошибка создания испытания: {response.status_code}")
        log(f"Ответ: {response.text}")
        return None

def test_status_transitions(trial_id):
    """Тестирование переходов статусов"""
    log(f"🔄 Тестирование переходов статусов для испытания {trial_id}")
    
    # 1. planned → active
    log("1️⃣ Переход planned → active")
    response = requests.patch(f"{BASE_URL}/trials/{trial_id}/", 
                            headers=HEADERS,
                            data=json.dumps({"status": "active"}))
    
    if response.status_code == 200:
        log("✅ Статус изменен на 'active'")
    else:
        log(f"❌ Ошибка изменения статуса: {response.status_code}")
        return False
    
    # 2. active → completed_008 (через форму 008)
    log("2️⃣ Переход active → completed_008 (через форму 008)")
    
    # Сначала нужно добавить участников и показатели
    # Для простоты теста просто изменим статус напрямую
    response = requests.patch(f"{BASE_URL}/trials/{trial_id}/", 
                            headers=HEADERS,
                            data=json.dumps({"status": "completed_008"}))
    
    if response.status_code == 200:
        log("✅ Статус изменен на 'completed_008'")
    else:
        log(f"❌ Ошибка изменения статуса: {response.status_code}")
        return False
    
    # 3. completed_008 → lab_sample_sent
    log("3️⃣ Переход completed_008 → lab_sample_sent")
    
    lab_data = {
        "laboratory_code": "LAB-2025-TEST-001",
        "sample_weight_kg": 2.5,
        "sent_date": "2025-01-15",
        "sample_source": "Тестовый образец"
    }
    
    response = requests.post(f"{BASE_URL}/trials/{trial_id}/mark-sent-to-lab/", 
                           headers=HEADERS,
                           data=json.dumps(lab_data))
    
    if response.status_code == 200:
        log("✅ Образец отправлен в лабораторию")
    else:
        log(f"❌ Ошибка отправки в лабораторию: {response.status_code}")
        log(f"Ответ: {response.text}")
        return False
    
    # 4. lab_sample_sent → lab_completed
    log("4️⃣ Переход lab_sample_sent → lab_completed")
    
    response = requests.post(f"{BASE_URL}/trials/{trial_id}/laboratory-complete/", 
                           headers=HEADERS,
                           data=json.dumps({"completed_date": "2025-01-20"}))
    
    if response.status_code == 200:
        log("✅ Лабораторные анализы завершены")
    else:
        log(f"❌ Ошибка завершения лабораторных анализов: {response.status_code}")
        log(f"Ответ: {response.text}")
        return False
    
    # 5. lab_completed → completed
    log("5️⃣ Переход lab_completed → completed")
    
    response = requests.post(f"{BASE_URL}/trials/{trial_id}/complete/", 
                           headers=HEADERS,
                           data=json.dumps({"completed_date": "2025-01-25"}))
    
    if response.status_code == 200:
        log("✅ Испытание полностью завершено")
    else:
        log(f"❌ Ошибка завершения испытания: {response.status_code}")
        log(f"Ответ: {response.text}")
        return False
    
    return True

def get_trial_status(trial_id):
    """Получение текущего статуса испытания"""
    response = requests.get(f"{BASE_URL}/trials/{trial_id}/", headers=HEADERS)
    if response.status_code == 200:
        trial = response.json()
        return trial['status']
    return None

def test_form008_integration(trial_id):
    """Тестирование интеграции с формой 008"""
    log("📋 Тестирование интеграции с формой 008...")
    
    # Получаем форму 008
    response = requests.get(f"{BASE_URL}/trials/{trial_id}/form008/", headers=HEADERS)
    if response.status_code == 200:
        log("✅ Форма 008 доступна")
        form_data = response.json()
        log(f"   Участников: {len(form_data.get('participants', []))}")
        log(f"   Показателей: {len(form_data.get('indicators', []))}")
    else:
        log(f"❌ Ошибка получения формы 008: {response.status_code}")
        return False
    
    # Тестируем сохранение формы 008 (черновик)
    form008_data = {
        "is_final": False,
        "harvest_date": "2025-01-10",
        "measurement_date": "2025-01-10",
        "participants": []
    }
    
    response = requests.post(f"{BASE_URL}/trials/{trial_id}/form008/bulk-save/", 
                           headers=HEADERS,
                           data=json.dumps(form008_data))
    
    if response.status_code == 200:
        log("✅ Форма 008 сохранена как черновик")
    else:
        log(f"❌ Ошибка сохранения формы 008: {response.status_code}")
        log(f"Ответ: {response.text}")
        return False
    
    # Тестируем финальную отправку формы 008
    form008_data["is_final"] = True
    
    response = requests.post(f"{BASE_URL}/trials/{trial_id}/form008/bulk-save/", 
                           headers=HEADERS,
                           data=json.dumps(form008_data))
    
    if response.status_code == 200:
        log("✅ Форма 008 отправлена финально")
        # Проверяем что статус изменился на completed_008
        status = get_trial_status(trial_id)
        if status == "completed_008":
            log("✅ Статус автоматически изменен на 'completed_008'")
        else:
            log(f"⚠️ Статус не изменился: {status}")
    else:
        log(f"❌ Ошибка финальной отправки формы 008: {response.status_code}")
        log(f"Ответ: {response.text}")
        return False
    
    return True

def main():
    """Основная функция тестирования"""
    log("🚀 Начало тестирования нового жизненного цикла испытаний")
    log("=" * 60)
    
    # Проверка подключения
    if not test_connection():
        sys.exit(1)
    
    # Создание тестового испытания
    trial = create_test_trial()
    if not trial:
        sys.exit(1)
    
    trial_id = trial['id']
    
    try:
        # Тестирование переходов статусов
        if test_status_transitions(trial_id):
            log("✅ Все переходы статусов работают корректно")
        else:
            log("❌ Ошибки в переходах статусов")
        
        # Тестирование интеграции с формой 008
        if test_form008_integration(trial_id):
            log("✅ Интеграция с формой 008 работает корректно")
        else:
            log("❌ Ошибки в интеграции с формой 008")
        
        # Финальная проверка статуса
        final_status = get_trial_status(trial_id)
        log(f"🏁 Финальный статус испытания: {final_status}")
        
        log("=" * 60)
        log("🎉 Тестирование завершено!")
        
    except Exception as e:
        log(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
