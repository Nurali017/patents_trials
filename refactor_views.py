#!/usr/bin/env python3
"""
Автоматический рефакторинг views.py на модули
"""
import os
import re

# Читаем исходный файл
with open('trials_app/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📊 Всего строк в views.py: {len(lines)}")

# Находим все ViewSet классы
viewset_pattern = re.compile(r'^class (\w+ViewSet)\(')
viewsets = []
for i, line in enumerate(lines, 1):
    match = viewset_pattern.match(line)
    if match:
        viewsets.append((i, match.group(1)))

print(f"📦 Найдено ViewSet'ов: {len(viewsets)}")
for line_num, name in viewsets:
    print(f"  {line_num:5d}: {name}")

# Определяем границы каждого ViewSet
viewset_boundaries = []
for i in range(len(viewsets)):
    start_line = viewsets[i][0]
    end_line = viewsets[i+1][0] - 1 if i+1 < len(viewsets) else len(lines)
    viewset_boundaries.append((viewsets[i][1], start_line, end_line))

print("\n🔍 Границы ViewSet'ов:")
for name, start, end in viewset_boundaries:
    print(f"  {name}: {start}-{end} ({end-start+1} строк)")

# Группируем ViewSet'ы по модулям
modules = {
    'geography': ['OblastViewSet', 'ClimateZoneViewSet', 'RegionViewSet'],
    'culture': ['IndicatorViewSet', 'TrialTypeViewSet', 'GroupCultureViewSet', 'CultureViewSet'],
    'sort': ['OriginatorViewSet', 'SortRecordViewSet'],
    'application': ['ApplicationViewSet'],
    'trial': ['TrialViewSet'],
    'trial_plan': ['TrialPlanViewSet'],
    'trial_participant': ['TrialParticipantViewSet'],
    'trial_result': ['TrialResultViewSet'],
    'document': ['DocumentViewSet'],
    'annual_report': ['AnnualReportViewSet'],
}

# Создаем директорию
os.makedirs('trials_app/views', exist_ok=True)

# Извлекаем импорты из начала файла
imports_end = 0
for i, line in enumerate(lines):
    if line.startswith('class '):
        imports_end = i
        break

base_imports = ''.join(lines[:imports_end])

print(f"\n📝 Базовые импорты: {imports_end} строк")

# Создаем файлы модулей
for module_name, viewset_names in modules.items():
    print(f"\n✅ Создаем {module_name}.py...")
    
    module_lines = []
    module_lines.append('"""\n')
    module_lines.append(f'{module_name.replace("_", " ").title()} ViewSets\n')
    module_lines.append('"""\n')
    module_lines.append('from rest_framework import viewsets, permissions, status\n')
    module_lines.append('from rest_framework.decorators import action\n')
    module_lines.append('from rest_framework.response import Response\n')
    module_lines.append('from django.utils import timezone\n')
    module_lines.append('from django.db import models as django_models\n')
    module_lines.append('\n')
    module_lines.append('from ..models import (\n')
    module_lines.append('    Oblast, Region, ClimateZone, Indicator, GroupCulture, Culture,\n')
    module_lines.append('    Originator, SortRecord, Application, ApplicationDecisionHistory,\n')
    module_lines.append('    PlannedDistribution, TrialType, Trial, TrialParticipant, TrialResult,\n')
    module_lines.append('    TrialLaboratoryResult, Document, TrialPlan, TrialPlanParticipant,\n')
    module_lines.append('    TrialPlanTrial, TrialPlanCulture, TrialPlanCultureTrialType\n')
    module_lines.append(')\n')
    module_lines.append('from ..serializers import (\n')
    module_lines.append('    OblastSerializer, RegionSerializer, ClimateZoneSerializer,\n')
    module_lines.append('    IndicatorSerializer, GroupCultureSerializer, CultureSerializer,\n')
    module_lines.append('    OriginatorSerializer, SortRecordSerializer, ApplicationSerializer,\n')
    module_lines.append('    TrialTypeSerializer, TrialSerializer, TrialParticipantSerializer,\n')
    module_lines.append('    TrialResultSerializer, TrialLaboratoryResultSerializer,\n')
    module_lines.append('    DocumentSerializer, TrialPlanSerializer, TrialPlanWriteSerializer,\n')
    module_lines.append('    TrialPlanAddParticipantsSerializer, TrialPlanCultureSerializer,\n')
    module_lines.append('    TrialPlanAddCultureSerializer, create_basic_trial_results,\n')
    module_lines.append('    create_quality_trial_results\n')
    module_lines.append(')\n')
    module_lines.append('from ..patents_integration import patents_api\n')
    module_lines.append('\n\n')
    
    # Добавляем ViewSet'ы этого модуля
    for viewset_name in viewset_names:
        for name, start, end in viewset_boundaries:
            if name == viewset_name:
                # Добавляем код ViewSet
                module_lines.extend(lines[start-1:end])
                module_lines.append('\n\n')
                print(f"  + {viewset_name} ({end-start+1} строк)")
    
    # Записываем модуль
    with open(f'trials_app/views/{module_name}.py', 'w', encoding='utf-8') as f:
        f.writelines(module_lines)
    
    print(f"  ✅ {module_name}.py создан")

# Создаем __init__.py
print("\n📝 Создаем __init__.py...")
init_lines = []
init_lines.append('"""\n')
init_lines.append('Views для Trials Service\n')
init_lines.append('Разделены по модулям для лучшей организации\n')
init_lines.append('"""\n\n')

for module_name, viewset_names in modules.items():
    init_lines.append(f'from .{module_name} import (\n')
    for i, name in enumerate(viewset_names):
        comma = ',' if i < len(viewset_names) - 1 else ''
        init_lines.append(f'    {name}{comma}\n')
    init_lines.append(')\n')

init_lines.append('\n__all__ = [\n')
for module_name, viewset_names in modules.items():
    for name in viewset_names:
        init_lines.append(f"    '{name}',\n")
init_lines.append(']\n')

with open('trials_app/views/__init__.py', 'w', encoding='utf-8') as f:
    f.writelines(init_lines)

print("  ✅ __init__.py создан")

# Переименовываем старый views.py
os.rename('trials_app/views.py', 'trials_app/views_old.py')
print("\n✅ views.py → views_old.py (backup)")

print("\n" + "="*60)
print("✨ РЕФАКТОРИНГ ЗАВЕРШЕН!")
print("="*60)
print(f"\n📊 Создано модулей: {len(modules)}")
for module_name, viewset_names in modules.items():
    print(f"  📄 {module_name}.py ({len(viewset_names)} ViewSet'ов)")
print(f"\n📦 Бэкап: trials_app/views_old.py")
print("\n🚀 Запустите: docker-compose restart trials-service")
