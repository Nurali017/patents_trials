# Анализ формирования качественных данных

## Обзор

Качественные данные в системе формируются через модель `TrialLaboratoryResult` и используются для оценки качества продукции сортов по Методике ГСИ.

---

## 1. Структура данных

### 1.1 Модель Indicator (Показатели)

**Файл:** `trials_app/models.py:105-146`

Показатели качества определяются флагом `is_quality=True`:

```python
class Indicator(SoftDeleteModel):
    is_quality = models.BooleanField(
        default=False,
        help_text="Показатель качества (дополнительные показатели)"
    )
```

**Примеры качественных показателей:**
- `protein_content` - Содержание белка (%)
- `gluten_content` - Содержание клейковины (%)
- `vitreousness` - Стекловидность (%)
- `thousand_seed_weight` - Масса 1000 зерен (г)
- `dry_matter_content` - Содержание сухого вещества (%)
- `starch_content` - Содержание крахмала (%)
- `oil_content` - Содержание масла (%)
- `vitamin_c_content` - Содержание витамина С (мг/%)
- И другие...

### 1.2 Модель TrialLaboratoryResult

**Файл:** `trials_app/models.py:2436-2551`

**Структура:**
```python
class TrialLaboratoryResult(SoftDeleteModel):
    trial = ForeignKey(Trial)              # Испытание
    indicator = ForeignKey(Indicator)       # Показатель (is_quality=True)
    participant = ForeignKey(TrialParticipant, null=True)  # Участник (опционально)
    value = FloatField(null=True)           # Числовое значение
    text_value = TextField(null=True)       # Текстовое значение
    analysis_date = DateField(null=True)    # Дата анализа
    sample_weight_kg = FloatField(null=True) # Вес образца
    notes = TextField(null=True)            # Примечания
    created_by = ForeignKey(User)           # Кто внес данные
```

**Важные особенности:**
- Один `Trial` → один набор лабораторных результатов
- Только для показателей с `is_quality=True`
- Вносятся ПОСЛЕ завершения полевых испытаний (status: `completed_008`, `lab_sample_sent`, `lab_completed`)
- Может быть привязан к конкретному участнику (сорту) или ко всему испытанию

---

## 2. Процесс создания качественных данных

### 2.1 Автоматическое создание пустых записей

**Файл:** `trials_app/serializers.py:104-143`

**Функция:** `create_quality_trial_results(trial, created_by)`

**Когда вызывается:**
- При отправке образца в лабораторию (mark_sent_to_lab)
- При создании плана испытаний с качественными показателями

**Что делает:**
1. Получает все качественные показатели (`is_quality=True`) для данного испытания
2. Для каждого участника (сорта) создает пустые записи `TrialResult` с `value=None`
3. Записи заполняются позже лабораторией

```python
def create_quality_trial_results(trial, created_by):
    quality_indicators = trial.indicators.filter(
        is_quality=True,
        is_deleted=False
    )
    
    for participant in trial.participants.filter(is_deleted=False):
        for indicator in quality_indicators:
            result, created = TrialResult.objects.get_or_create(
                participant=participant,
                indicator=indicator,
                defaults={
                    'trial': trial,
                    'value': None,  # Пустое значение - заполнит лаборатория
                }
            )
```

### 2.2 Внесение лабораторных результатов

**Файл:** `trials_app/views/trial.py:240-336`

**Эндпоинт:** `POST /api/trials/{id}/laboratory-results/bulk-entry/`

**Процесс:**
1. Проверка статуса испытания (должно быть завершено)
2. Валидация показателей (только `is_quality=True`)
3. Массовое создание/обновление `TrialLaboratoryResult`

**Пример запроса:**
```json
{
  "results": [
    {
      "indicator": 14,  // ID показателя (protein_content)
      "value": 14.5,
      "participant_id": 123  // Опционально
    },
    {
      "indicator": 23,  // ID показателя (gluten_content)
      "value": 28.3
    }
  ],
  "analysis_date": "2025-10-22"
}
```

**Валидация:**
- Показатель должен существовать и иметь `is_quality=True`
- Испытание должно быть в статусе `completed_008`, `lab_sample_sent` или `lab_completed`
- Уникальность: `(trial, indicator, participant)`

---

## 3. Получение и агрегация качественных данных

### 3.1 Сервис QualityIndicatorsService

**Файл:** `trials_app/views/services/quality_indicators_service.py`

#### 3.1.1 Получение всех показателей качества

**Метод:** `get_all_quality_indicators()`

Возвращает список всех показателей с `is_quality=True` из базы данных:

```python
quality_indicators = Indicator.objects.filter(is_quality=True)
    .order_by('sort_order', 'name')
```

#### 3.1.2 Получение показателей для конкретного сорта

**Метод:** `get_quality_indicators(sort_item, years_range)`

**Процесс:**
1. Находит все `TrialParticipant` для сорта в регионе за указанные годы
2. Получает `TrialLaboratoryResult` для найденных испытаний
3. Группирует данные по годам

**Структура результата:**
```python
{
    'protein_content': {
        'name': 'Содержание белка',
        'unit': '%',
        'years': {
            2023: 14.5,
            2024: 15.2
        }
    },
    'gluten_content': {
        'name': 'Содержание клейковины',
        'unit': '%',
        'years': {
            2023: 28.3,
            2024: 29.1
        }
    }
}
```

**Код:**
```python
def get_quality_indicators(sort_item, years_range):
    sort_record_id = sort_item['sort_record']['id']
    region_id = sort_item['region']['id']
    
    indicators_by_year = {}
    
    for y in years_range:
        participants = TrialParticipant.objects.filter(
            sort_record_id=sort_record_id,
            trial__region_id=region_id,
            trial__year=y,
            is_deleted=False
        ).values_list('trial_id', flat=True)
        
        lab_results = TrialLaboratoryResult.objects.filter(
            trial_id__in=participants,
            participant__sort_record_id=sort_record_id
        ).select_related('indicator')
        
        for result in lab_results:
            if result.value is not None:
                indicator_code = result.indicator.code
                if indicator_code not in indicators_by_year:
                    indicators_by_year[indicator_code] = {
                        'name': result.indicator.name,
                        'unit': result.indicator.unit,
                        'years': {}
                    }
                indicators_by_year[indicator_code]['years'][y] = result.value
```

---

## 4. Оценка качества (QualityEvaluator)

**Файл:** `trials_app/evaluation/quality_evaluator.py`

### 4.1 Критерии качества по Методике ГСИ

**Стандарты оценки (баллы 1-5):**

```python
quality_standards = {
    'protein_content': {
        'excellent': 15.0,      # 5 баллов
        'good': 13.0,          # 4 балла  
        'satisfactory': 11.0,  # 3 балла
        'poor': 9.0            # 2 балла
    },
    'gluten_content': {
        'excellent': 30.0,     # 5 баллов
        'good': 25.0,          # 4 балла
        'satisfactory': 20.0,  # 3 балла
        'poor': 15.0           # 2 балла
    },
    'vitreousness': {
        'excellent': 90.0,     # 5 баллов
        'good': 80.0,          # 4 балла
        'satisfactory': 70.0,  # 3 балла
        'poor': 60.0           # 2 балла
    },
    'thousand_seed_weight': {
        'excellent': 50.0,     # 5 баллов
        'good': 45.0,          # 4 балла
        'satisfactory': 40.0,  # 3 балла
        'poor': 35.0           # 2 балла
    }
}
```

### 4.2 Расчет балла качества

**Метод:** `calculate_quality_score(sort_data)`

**Процесс:**
1. Извлечение показателей качества из данных сорта
2. Расчет балла для каждого показателя (1-5)
3. Вычисление среднего балла
4. Проверка достаточности данных (минимум 2 показателя)

**Результат:**
```python
{
    'score': 4.2,  # Средний балл
    'interpretation': 'Хорошее качество продукции',
    'indicators': {
        'protein_content': {
            'value': 14.5,
            'score': 4,
            'interpretation': 'Хороший'
        },
        'gluten_content': {
            'value': 28.3,
            'score': 4,
            'interpretation': 'Хороший'
        }
    },
    'sufficient_data': True  # Минимум 2 показателя
}
```

**Особенности:**
- Если данных нет → `score: None`, `data_available: False`
- Если недостаточно показателей (< 2) → `sufficient_data: False`
- Средний балл округляется до 1 знака после запятой

### 4.3 Извлечение показателей качества

**Метод:** `_extract_quality_indicators(sort_data)`

Ищет показатели качества в:
1. `sort_data['regions_data'][]['quality_indicators']`
2. `sort_data['summary']['quality_indicators']`

---

## 5. Использование в годовых отчетах

### 5.1 SummaryService

**Файл:** `trials_app/views/services/summary_service.py`

Качественные данные используются в:
- Балльной оценке сортов (30% веса в общей оценке)
- Рекомендациях по решениям (одобрение/продолжение/отклонение)

**Критерии для одобрения:**
```python
quality_score is not None and quality_score >= 3  # Минимум 3 балла
```

**Критерии для отклонения:**
- Качество не учитывается напрямую в жестком отклонении
- Но учитывается в общем балле (overall_score)

### 5.2 MethodologyTableService

**Файл:** `trials_app/views/services/methodology_table_service.py`

Качественные показатели включаются в таблицу методики для каждого сорта:

```python
sort_data = {
    'main_indicators': self.quality_service.get_main_indicators(...),
    'quality_indicators': self.quality_service.get_quality_indicators(...)
}
```

---

## 6. Жизненный цикл качественных данных

```
1. ПЛАНИРОВАНИЕ
   └─> Создание Trial с качественными показателями
       └─> Автоматическое создание пустых TrialResult (is_quality=True)

2. ПОЛЕВЫЕ ИСПЫТАНИЯ
   └─> Статус: active → completed_008
       └─> Сбор урожайности и основных показателей

3. ОТПРАВКА В ЛАБОРАТОРИЮ
   └─> Статус: lab_sample_sent
       └─> Автоматическое создание пустых TrialLaboratoryResult

4. ЛАБОРАТОРНЫЙ АНАЛИЗ
   └─> Внесение результатов через API
       POST /api/trials/{id}/laboratory-results/bulk-entry/
       └─> Создание/обновление TrialLaboratoryResult

5. ЗАВЕРШЕНИЕ
   └─> Статус: lab_completed
       └─> Данные доступны для оценки и отчетов

6. ОЦЕНКА И ОТЧЕТЫ
   └─> QualityEvaluator.calculate_quality_score()
       └─> Использование в SummaryService и MethodologyTableService
```

---

## 7. Важные моменты

### 7.1 Разделение данных

- **TrialResult** - для основных показателей (`is_quality=False`)
- **TrialLaboratoryResult** - для качественных показателей (`is_quality=True`)

### 7.2 Валидация

- Показатель должен иметь `is_quality=True` для лабораторных результатов
- Испытание должно быть завершено перед внесением лабораторных данных
- Уникальность: `(trial, indicator, participant)`

### 7.3 Агрегация по годам

- Данные собираются за все годы из диапазона
- Группируются по показателям и годам
- Используются для расчета средних значений и трендов

### 7.4 Оценка качества

- Минимум 2 показателя для достаточности данных
- Балльная система: 1-5 (от плохого до отличного)
- Вес в общей оценке: 30%

---

## 8. Примеры использования

### 8.1 Получение качественных показателей для сорта

```python
from trials_app.views.services import QualityIndicatorsService

service = QualityIndicatorsService()

# Получить все показатели
all_indicators = service.get_all_quality_indicators()

# Получить показатели для сорта
sort_item = {
    'sort_record': {'id': 123},
    'region': {'id': 45}
}
years_range = [2023, 2024]

quality_data = service.get_quality_indicators(sort_item, years_range)
# Результат: {'protein_content': {'name': '...', 'years': {...}}, ...}
```

### 8.2 Расчет балла качества

```python
from trials_app.evaluation import QualityEvaluator

evaluator = QualityEvaluator()

sort_data = {
    'regions_data': [
        {
            'quality_indicators': {
                'protein_content': 14.5,
                'gluten_content': 28.3
            }
        }
    ]
}

result = evaluator.calculate_quality_score(sort_data)
# Результат: {'score': 4.0, 'indicators': {...}, ...}
```

---

## 9. Потенциальные проблемы и улучшения

### 9.1 Проблемы

1. **Дублирование данных:** 
   - `TrialResult` с `is_quality=True` создаются автоматически
   - `TrialLaboratoryResult` создаются при внесении лабораторных данных
   - Может быть путаница между двумя моделями

2. **Отсутствие данных:**
   - Если лаборатория не внесла данные, качественные показатели остаются пустыми
   - Оценка качества возвращает `score: None`

3. **Агрегация:**
   - Данные собираются по годам, но нет автоматического расчета средних
   - Нет обработки выбросов или аномалий

### 9.2 Рекомендации по улучшению

1. **Унификация моделей:**
   - Рассмотреть объединение `TrialResult` и `TrialLaboratoryResult`
   - Или четко разделить их использование

2. **Валидация данных:**
   - Добавить проверку на разумность значений (min/max)
   - Проверка на выбросы

3. **Автоматический расчет:**
   - Средние значения по годам
   - Тренды и изменения
   - Сравнение с эталонными значениями

4. **Уведомления:**
   - Напоминания о необходимости внесения лабораторных данных
   - Предупреждения о недостаточности данных для оценки

---

## Заключение

Качественные данные формируются через специализированную модель `TrialLaboratoryResult` и проходят полный жизненный цикл от планирования до оценки. Система обеспечивает валидацию, агрегацию и использование данных в балльной оценке сортов по Методике ГСИ.

