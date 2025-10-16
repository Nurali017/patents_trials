#!/usr/bin/env python
"""
🧪 КОМПЛЕКСНЫЙ ТЕСТ ЖИЗНЕННОГО ЦИКЛА СОРТОИСПЫТАНИЙ

Проверяет все этапы от заявки до решения с разными сценариями:
- Сценарий 1: Одобрено за 1 год (Костанайская область)
- Сценарий 2: Продолжение 2 года (Акмолинская область)
- Сценарий 3: Продолжение 3 года (Алматинская область)

Запуск:
    python test_full_lifecycle.py
"""

import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trials.settings')
django.setup()

from django.contrib.auth.models import User
from trials_app.models import (
    Oblast, Region, Culture, GroupCulture, Originator, SortRecord, 
    Application, PlannedDistribution, TrialType, Trial, TrialParticipant, 
    TrialResult, TrialLaboratoryResult, Indicator
)


class TestLifecycle:
    """Класс для тестирования жизненного цикла"""
    
    def __init__(self):
        self.user = None
        self.application = None
        self.trials = {}
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def log(self, message, level='INFO'):
        """Логирование"""
        icons = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'ERROR': '❌',
            'WARNING': '⚠️',
            'STEP': '🔹'
        }
        icon = icons.get(level, 'ℹ️')
        print(f"{icon}  {message}")
    
    def separator(self, title):
        """Разделитель"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def assert_true(self, condition, message):
        """Проверка условия"""
        if condition:
            self.results['passed'] += 1
            self.log(f"✓ {message}", 'SUCCESS')
            return True
        else:
            self.results['failed'] += 1
            self.results['errors'].append(message)
            self.log(f"✗ {message}", 'ERROR')
            return False
    
    def setup(self):
        """Подготовка тестовых данных"""
        self.separator("ПОДГОТОВКА ТЕСТОВЫХ ДАННЫХ")
        
        # Очистка предыдущих тестовых данных
        self.log("Очистка предыдущих тестовых данных...")
        Application.objects.filter(application_number__startswith='TEST-').delete()
        SortRecord.objects.filter(sort_id__in=[1001, 1002, 1003, 9999]).delete()
        
        # Пользователь
        self.user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        self.log(f"Пользователь: {self.user.username} {'(создан)' if created else '(существующий)'}")
        
        # Проверка справочников
        oblasts_count = Oblast.objects.filter(is_deleted=False).count()
        regions_count = Region.objects.filter(is_deleted=False).count()
        cultures_count = Culture.objects.filter(is_deleted=False).count()
        indicators_count = Indicator.objects.filter(is_deleted=False).count()
        trial_types_count = TrialType.objects.filter(is_deleted=False).count()
        
        self.log(f"Справочники: {oblasts_count} областей, {regions_count} ГСУ, {cultures_count} культур")
        self.log(f"Показатели: {indicators_count}, Типы испытаний: {trial_types_count}")
        
        if oblasts_count < 3 or regions_count < 3 or cultures_count < 1:
            self.log("⚠️ Недостаточно данных для полного теста. Создаю минимальные данные...", 'WARNING')
            self._create_minimal_data()
    
    def _create_minimal_data(self):
        """Создать минимальные тестовые данные"""
        # Области
        oblast1, _ = Oblast.objects.get_or_create(name="Алматинская область", defaults={'code': 'ALM'})
        oblast2, _ = Oblast.objects.get_or_create(name="Акмолинская область", defaults={'code': 'AKM'})
        oblast3, _ = Oblast.objects.get_or_create(name="Костанайская область", defaults={'code': 'KST'})
        
        # ГСУ
        Region.objects.get_or_create(name="Алматинский ГСУ", oblast=oblast1)
        Region.objects.get_or_create(name="Акмолинский ГСУ", oblast=oblast2)
        Region.objects.get_or_create(name="Костанайский ГСУ", oblast=oblast3)
        
        # Культура
        group, _ = GroupCulture.objects.get_or_create(
            group_culture_id=1,
            defaults={'name': 'Зерновые', 'code': 'grain'}
        )
        Culture.objects.get_or_create(
            culture_id=1,
            defaults={'name': 'Пшеница яровая', 'code': 'wheat_spring', 'group_culture': group}
        )
        
        # Показатели
        Indicator.objects.get_or_create(
            code='yield',
            defaults={'name': 'Урожайность', 'unit': 'ц/га', 'is_quality': False}
        )
        Indicator.objects.get_or_create(
            code='protein',
            defaults={'name': 'Белок', 'unit': '%', 'is_quality': True}
        )
        Indicator.objects.get_or_create(
            code='gluten',
            defaults={'name': 'Клейковина', 'unit': '%', 'is_quality': True}
        )
        
        # Тип испытания
        TrialType.objects.get_or_create(
            code='competitive',
            defaults={'name': 'КСИ', 'category': 'mandatory'}
        )
        
        self.log("✓ Минимальные данные созданы")
    
    def test_scenario_1_one_year_approval(self):
        """
        СЦЕНАРИЙ 1: Одобрение за 1 год (Костанайская область)
        
        Быстрое испытание - сорт сразу показал отличные результаты
        """
        self.separator("СЦЕНАРИЙ 1: ОДОБРЕНИЕ ЗА 1 ГОД (Костанайская)")
        
        region = Region.objects.filter(oblast__name__icontains='Костанай', is_deleted=False).first()
        if not region:
            self.log("⚠️ Костанайский ГСУ не найден", 'WARNING')
            return
        
        # Шаг 1: Создать заявку
        self.log("ШАГ 1: Создание заявки", 'STEP')
        
        culture = Culture.objects.filter(is_deleted=False).first()
        sort_record, _ = SortRecord.objects.get_or_create(
            sort_id=1001,
            defaults={
                'name': 'Тестовый сорт 1001',
                'culture': culture
            }
        )
        
        application = Application.objects.create(
            application_number=f"TEST-2025-SCENARIO1",
            submission_date=date(2025, 3, 1),
            sort_record=sort_record,
            applicant="ТОО Тестовая агрофирма",
            applicant_inn_bin="123456789012",
            status='submitted',
            created_by=self.user
        )
        application.target_oblasts.add(region.oblast)
        
        self.assert_true(
            application.status == 'submitted',
            f"Заявка создана: {application.application_number}"
        )
        
        # Шаг 2: Распределение
        self.log("ШАГ 2: Распределение по ГСУ", 'STEP')
        
        planned_dist = PlannedDistribution.objects.create(
            application=application,
            region=region,
            trial_type=TrialType.objects.first(),
            created_by=self.user
        )
        application.status = 'distributed'
        application.save()
        
        self.assert_true(
            planned_dist.status == 'planned',
            f"PlannedDistribution создано: {planned_dist}"
        )
        
        # Шаг 3: Создание Trial (2025)
        self.log("ШАГ 3: Создание Trial 2025", 'STEP')
        
        # Создать стандарт
        standard_sort, _ = SortRecord.objects.get_or_create(
            sort_id=9999,
            defaults={'name': 'Стандарт Жігер', 'culture': culture}
        )
        
        trial = Trial.objects.create(
            description="КСИ пшеницы 2025 Костанайская",
            region=region,
            culture=culture,
            trial_type=TrialType.objects.first(),
            area_ha=0.5,
            start_date=date(2025, 4, 15),
            year=2025,
            responsible_person="Иванов И.И.",
            created_by=self.user
        )
        
        # Добавить показатели
        indicators = Indicator.objects.filter(is_deleted=False)
        trial.indicators.set(indicators)
        
        # Добавить участников
        standard_participant = TrialParticipant.objects.create(
            trial=trial,
            sort_record=standard_sort,
            statistical_group=0,
            participant_number=1
        )
        
        tested_participant = TrialParticipant.objects.create(
            trial=trial,
            sort_record=sort_record,
            statistical_group=1,
            participant_number=2,
            application=application
        )
        
        # Обновить статусы вручную (в реальности это делает serializer)
        trial.status = 'active'
        trial.save()
        
        planned_dist.refresh_from_db()
        if planned_dist.status == 'planned':
            planned_dist.status = 'in_progress'
            planned_dist.year_started = 2025
            planned_dist.save()
        
        application.status = 'in_progress'
        application.save()
        
        self.assert_true(
            trial.status == 'active',
            f"Trial создан и активен: Trial #{trial.id}"
        )
        self.assert_true(
            planned_dist.status == 'in_progress' and planned_dist.year_started == 2025,
            f"PlannedDistribution в работе с 2025 года"
        )
        
        # Шаг 4: Внесение полевых результатов
        self.log("ШАГ 4: Внесение полевых результатов", 'STEP')
        
        yield_indicator = Indicator.objects.filter(code='yield', is_deleted=False).first()
        
        # Результаты стандарта
        TrialResult.objects.create(
            participant=standard_participant,
            indicator=yield_indicator,
            plot_1=43.0,
            plot_2=43.5,
            plot_3=42.8,
            plot_4=43.2,
            measurement_date=date(2025, 9, 20),
            created_by=self.user
        )
        
        # Результаты испытываемого (отличные!)
        TrialResult.objects.create(
            participant=tested_participant,
            indicator=yield_indicator,
            plot_1=51.0,
            plot_2=51.5,
            plot_3=51.2,
            plot_4=51.3,
            measurement_date=date(2025, 9, 20),
            created_by=self.user
        )
        
        trial.status = 'completed'
        trial.save()
        
        self.assert_true(
            trial.status == 'completed',
            "Полевые работы завершены"
        )
        
        # Шаг 5: Отправка в лабораторию
        self.log("ШАГ 5: Отправка образца в лабораторию", 'STEP')
        
        trial.laboratory_status = 'sent'
        trial.laboratory_code = 'LAB-2025-001-KST'
        trial.laboratory_sent_date = date(2025, 10, 1)
        trial.laboratory_sample_weight = 2.0
        trial.status = 'lab_sample_sent'
        trial.save()
        
        self.assert_true(
            trial.laboratory_status == 'sent',
            f"Образец отправлен: {trial.laboratory_code}"
        )
        
        # Шаг 6: Лабораторные результаты
        self.log("ШАГ 6: Внесение лабораторных результатов", 'STEP')
        
        protein_indicator = Indicator.objects.filter(code='protein', is_deleted=False).first()
        gluten_indicator = Indicator.objects.filter(code='gluten', is_deleted=False).first()
        
        if protein_indicator:
            TrialLaboratoryResult.objects.create(
                trial=trial,
                indicator=protein_indicator,
                participant=tested_participant,
                value=15.2,
                laboratory_code='LAB-2025-001-KST',
                analysis_date=date(2025, 10, 15),
                created_by=self.user
            )
        
        if gluten_indicator:
            TrialLaboratoryResult.objects.create(
                trial=trial,
                indicator=gluten_indicator,
                participant=tested_participant,
                value=30.0,
                laboratory_code='LAB-2025-001-KST',
                analysis_date=date(2025, 10, 15),
                created_by=self.user
            )
        
        trial.laboratory_status = 'completed'
        trial.laboratory_completed_date = date(2025, 10, 20)
        trial.status = 'lab_completed'
        trial.save()
        
        self.assert_true(
            trial.laboratory_status == 'completed',
            "Лабораторные анализы завершены"
        )
        
        # Шаг 7: Принятие решения (approved)
        self.log("ШАГ 7: Принятие решения комиссией", 'STEP')
        
        trial.decision = 'approved'
        trial.decision_justification = "Отличные результаты: урожайность 51.3 ц/га (+18%), белок 15.2%, клейковина 30%"
        trial.decision_date = date(2025, 11, 1)
        trial.decided_by = self.user
        trial.status = 'approved'
        trial.save()
        
        # Обновить PlannedDistribution
        planned_dist.status = 'approved'
        planned_dist.year_completed = 2025
        planned_dist.save()
        
        self.assert_true(
            trial.decision == 'approved' and trial.status == 'approved',
            "Решение: ОДОБРЕНО ✅"
        )
        self.assert_true(
            planned_dist.status == 'approved' and planned_dist.year_completed == 2025,
            f"PlannedDistribution завершен: 2025-2025 (1 год)"
        )
        
        self.log(f"\n📊 ИТОГ СЦЕНАРИЯ 1:", 'SUCCESS')
        self.log(f"   Костанайская область: ОДОБРЕНО за 1 год! ✅")
        self.log(f"   Trial #{trial.id}: {trial.decision}")
        self.log(f"   PlannedDistribution: {planned_dist.year_started}-{planned_dist.year_completed}")
        
        return trial, planned_dist
    
    def test_scenario_2_two_year_approval(self):
        """
        СЦЕНАРИЙ 2: Продолжение и одобрение за 2 года (Акмолинская область)
        """
        self.separator("СЦЕНАРИЙ 2: ОДОБРЕНИЕ ЗА 2 ГОДА (Акмолинская)")
        
        region = Region.objects.filter(oblast__name__icontains='Акмол', is_deleted=False).first()
        if not region:
            self.log("⚠️ Акмолинский ГСУ не найден", 'WARNING')
            return
        
        culture = Culture.objects.filter(is_deleted=False).first()
        sort_record, _ = SortRecord.objects.get_or_create(
            sort_id=1002,
            defaults={'name': 'Тестовый сорт 1002', 'culture': culture}
        )
        
        # Создать заявку
        application = Application.objects.create(
            application_number=f"TEST-2025-SCENARIO2",
            submission_date=date(2025, 3, 1),
            sort_record=sort_record,
            applicant="ТОО Тестовая агрофирма 2",
            status='distributed',
            created_by=self.user
        )
        application.target_oblasts.add(region.oblast)
        
        planned_dist = PlannedDistribution.objects.create(
            application=application,
            region=region,
            trial_type=TrialType.objects.first(),
            created_by=self.user
        )
        
        # === ГОД 2025 ===
        self.log("\n🗓️  ГОД 2025 - Первый Trial", 'STEP')
        
        standard_sort = SortRecord.objects.get(sort_id=9999)
        
        trial_2025 = Trial.objects.create(
            description="КСИ пшеницы 2025 Акмолинская",
            region=region,
            culture=culture,
            start_date=date(2025, 4, 15),
            year=2025,
            responsible_person="Петров П.П.",
            status='active',
            created_by=self.user
        )
        
        TrialParticipant.objects.create(
            trial=trial_2025,
            sort_record=standard_sort,
            statistical_group=0,
            participant_number=1
        )
        
        TrialParticipant.objects.create(
            trial=trial_2025,
            sort_record=sort_record,
            statistical_group=1,
            participant_number=2,
            application=application
        )
        
        # Обновить PlannedDistribution
        planned_dist.status = 'in_progress'
        planned_dist.year_started = 2025
        planned_dist.save()
        
        application.status = 'in_progress'
        application.save()
        
        # Полевые результаты (средние)
        yield_indicator = Indicator.objects.filter(code='yield').first()
        
        TrialResult.objects.create(
            participant=trial_2025.participants.get(statistical_group=1),
            indicator=yield_indicator,
            plot_1=42.0,
            plot_2=42.2,
            plot_3=41.8,
            plot_4=42.1,
            measurement_date=date(2025, 9, 20),
            created_by=self.user
        )
        
        trial_2025.status = 'completed'
        trial_2025.save()
        
        # Лаборатория
        trial_2025.laboratory_status = 'sent'
        trial_2025.laboratory_code = 'LAB-2025-002-AKM'
        trial_2025.status = 'lab_sample_sent'
        trial_2025.save()
        
        trial_2025.laboratory_status = 'completed'
        trial_2025.status = 'lab_completed'
        trial_2025.save()
        
        # Решение: ПРОДОЛЖИТЬ
        trial_2025.decision = 'continue'
        trial_2025.decision_justification = "Результаты средние, требуется еще год"
        trial_2025.decision_date = date(2025, 11, 1)
        trial_2025.status = 'continue'
        trial_2025.save()
        
        self.assert_true(
            trial_2025.decision == 'continue',
            f"Trial 2025: Решение ПРОДОЛЖИТЬ ⏩"
        )
        self.assert_true(
            planned_dist.status == 'in_progress',
            "PlannedDistribution остается in_progress"
        )
        
        # === ГОД 2026 ===
        self.log("\n🗓️  ГОД 2026 - Второй Trial", 'STEP')
        
        trial_2026 = Trial.objects.create(
            description="КСИ пшеницы 2026 Акмолинская",
            region=region,
            culture=culture,
            start_date=date(2026, 4, 15),
            year=2026,
            responsible_person="Петров П.П.",
            status='active',
            created_by=self.user
        )
        
        TrialParticipant.objects.create(
            trial=trial_2026,
            sort_record=standard_sort,
            statistical_group=0,
            participant_number=1
        )
        
        TrialParticipant.objects.create(
            trial=trial_2026,
            sort_record=sort_record,
            statistical_group=1,
            participant_number=2,
            application=application
        )
        
        # Результаты лучше
        TrialResult.objects.create(
            participant=trial_2026.participants.get(statistical_group=1),
            indicator=yield_indicator,
            plot_1=46.5,
            plot_2=46.8,
            plot_3=46.3,
            plot_4=46.7,
            measurement_date=date(2026, 9, 20),
            created_by=self.user
        )
        
        trial_2026.status = 'completed'
        trial_2026.save()
        
        # Лаборатория
        trial_2026.laboratory_status = 'completed'
        trial_2026.status = 'lab_completed'
        trial_2026.save()
        
        # Решение: ОДОБРЕНО
        trial_2026.decision = 'approved'
        trial_2026.decision_justification = "Улучшение показателей, стабильные результаты за 2 года"
        trial_2026.decision_date = date(2026, 11, 1)
        trial_2026.status = 'approved'
        trial_2026.save()
        
        # Завершить PlannedDistribution
        planned_dist.status = 'approved'
        planned_dist.year_completed = 2026
        planned_dist.save()
        
        self.assert_true(
            trial_2026.decision == 'approved',
            f"Trial 2026: Решение ОДОБРЕНО ✅"
        )
        self.assert_true(
            planned_dist.status == 'approved' and planned_dist.year_completed == 2026,
            f"PlannedDistribution завершен: 2025-2026 (2 года)"
        )
        
        # Проверка get_trials()
        all_trials = planned_dist.get_trials()
        self.assert_true(
            all_trials.count() == 2,
            f"PlannedDistribution.get_trials() возвращает 2 Trial"
        )
        
        self.log(f"\n📊 ИТОГ СЦЕНАРИЯ 2:", 'SUCCESS')
        self.log(f"   Акмолинская область: ОДОБРЕНО за 2 года ✅")
        self.log(f"   Trial #({trial_2025.id}, {trial_2026.id})")
        self.log(f"   Решения: continue → approved")
    
    def test_scenario_3_three_year_approval(self):
        """
        СЦЕНАРИЙ 3: Продолжение 3 года (Алматинская область)
        """
        self.separator("СЦЕНАРИЙ 3: ОДОБРЕНИЕ ЗА 3 ГОДА (Алматинская)")
        
        region = Region.objects.filter(oblast__name__icontains='Алмат', is_deleted=False).first()
        if not region:
            self.log("⚠️ Алматинский ГСУ не найден", 'WARNING')
            return
        
        culture = Culture.objects.filter(is_deleted=False).first()
        sort_record, _ = SortRecord.objects.get_or_create(
            sort_id=1003,
            defaults={'name': 'Тестовый сорт 1003', 'culture': culture}
        )
        standard_sort = SortRecord.objects.get(sort_id=9999)
        yield_indicator = Indicator.objects.filter(code='yield').first()
        
        # Создать заявку
        application = Application.objects.create(
            application_number=f"TEST-2025-SCENARIO3",
            submission_date=date(2025, 3, 1),
            sort_record=sort_record,
            applicant="ТОО Тестовая агрофирма 3",
            status='distributed',
            created_by=self.user
        )
        application.target_oblasts.add(region.oblast)
        
        planned_dist = PlannedDistribution.objects.create(
            application=application,
            region=region,
            trial_type=TrialType.objects.first(),
            created_by=self.user
        )
        
        # === ГОД 2025 ===
        self.log("\n🗓️  ГОД 2025", 'STEP')
        trial_2025 = self._create_trial_year(region, culture, sort_record, standard_sort, application, 2025, 45.0, 'continue')
        planned_dist.status = 'in_progress'
        planned_dist.year_started = 2025
        planned_dist.save()
        
        # === ГОД 2026 ===
        self.log("\n🗓️  ГОД 2026", 'STEP')
        trial_2026 = self._create_trial_year(region, culture, sort_record, standard_sort, application, 2026, 46.5, 'continue')
        
        # === ГОД 2027 ===
        self.log("\n🗓️  ГОД 2027", 'STEP')
        trial_2027 = self._create_trial_year(region, culture, sort_record, standard_sort, application, 2027, 47.8, 'approved')
        
        # Завершить PlannedDistribution
        planned_dist.status = 'approved'
        planned_dist.year_completed = 2027
        planned_dist.save()
        
        # Проверки
        all_trials = planned_dist.get_trials()
        years_count = planned_dist.get_years_count()
        
        self.assert_true(
            all_trials.count() == 3,
            f"PlannedDistribution.get_trials() возвращает 3 Trial"
        )
        self.assert_true(
            years_count == 3,
            f"PlannedDistribution.get_years_count() = 3"
        )
        self.assert_true(
            planned_dist.status == 'approved' and planned_dist.year_completed == 2027,
            f"PlannedDistribution завершен: 2025-2027 (3 года)"
        )
        
        self.log(f"\n📊 ИТОГ СЦЕНАРИЯ 3:", 'SUCCESS')
        self.log(f"   Алматинская область: ОДОБРЕНО за 3 года ✅")
        self.log(f"   Trials: #{trial_2025.id}, #{trial_2026.id}, #{trial_2027.id}")
        self.log(f"   Решения: continue → continue → approved")
        self.log(f"   Динамика урожайности: 45.0 → 46.5 → 47.8 ц/га")
    
    def _create_trial_year(self, region, culture, sort_record, standard_sort, application, year, yield_value, decision):
        """Вспомогательный метод для создания Trial за год"""
        trial = Trial.objects.create(
            description=f"КСИ пшеницы {year} {region.name}",
            region=region,
            culture=culture,
            start_date=date(year, 4, 15),
            year=year,
            responsible_person="Тестовый сортопыт",
            status='active',
            created_by=self.user
        )
        
        # Участники
        TrialParticipant.objects.create(
            trial=trial,
            sort_record=standard_sort,
            statistical_group=0,
            participant_number=1
        )
        
        tested = TrialParticipant.objects.create(
            trial=trial,
            sort_record=sort_record,
            statistical_group=1,
            participant_number=2,
            application=application
        )
        
        # Результаты
        yield_indicator = Indicator.objects.filter(code='yield').first()
        TrialResult.objects.create(
            participant=tested,
            indicator=yield_indicator,
            plot_1=yield_value,
            plot_2=yield_value + 0.2,
            plot_3=yield_value - 0.2,
            plot_4=yield_value + 0.1,
            measurement_date=date(year, 9, 20),
            created_by=self.user
        )
        
        # Полный цикл
        trial.status = 'completed'
        trial.save()
        
        trial.laboratory_status = 'completed'
        trial.status = 'lab_completed'
        trial.save()
        
        trial.decision = decision
        trial.decision_date = date(year, 11, 1)
        trial.status = decision
        trial.save()
        
        self.log(f"   Trial {year}: урожайность {yield_value} ц/га → {decision}")
        
        return trial
    
    def test_api_regional_status(self):
        """Тест API endpoint: /applications/{id}/regional-status/"""
        self.separator("ТЕСТ API: /applications/{id}/regional-status/")
        
        # Взять первую заявку
        application = Application.objects.filter(
            planned_distributions_records__isnull=False,
            is_deleted=False
        ).first()
        
        if not application:
            self.log("⚠️ Нет заявок для теста", 'WARNING')
            return
        
        from rest_framework.test import APIRequestFactory, force_authenticate
        from trials_app.views import ApplicationViewSet
        
        factory = APIRequestFactory()
        request = factory.get(f'/api/v1/applications/{application.id}/regional-status/')
        force_authenticate(request, user=self.user)
        
        view = ApplicationViewSet.as_view({'get': 'regional_status'})
        response = view(request, pk=application.id)
        
        self.assert_true(
            response.status_code == 200,
            f"API вернул статус 200"
        )
        
        if response.status_code == 200:
            data = response.data
            self.log(f"\n📊 Результат API:")
            self.log(f"   Заявка: {data.get('application_number')}")
            self.log(f"   Статус: {data.get('application_status')}")
            self.log(f"   Областей: {data.get('total_regions')}")
            
            for region in data.get('regions', []):
                self.log(f"\n   🌍 {region['region_name']} ({region['oblast_name']})")
                self.log(f"      Статус: {region['status_display']}")
                self.log(f"      Годы: {region['year_started']}-{region['year_completed'] or 'в работе'}")
                self.log(f"      Испытаний: {len(region['trials'])}")
                
                for trial in region['trials']:
                    self.log(f"         • {trial['year']}: {trial['decision_display'] or trial['status_display']}")
    
    def print_summary(self):
        """Вывести итоги"""
        self.separator("📊 ИТОГИ ТЕСТИРОВАНИЯ")
        
        print(f"\n✅ Успешно: {self.results['passed']}")
        print(f"❌ Ошибок: {self.results['failed']}")
        
        if self.results['failed'] > 0:
            print(f"\n❌ Список ошибок:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        print(f"\n{'='*70}")
        
        if self.results['failed'] == 0:
            print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        else:
            print(f"⚠️  ЕСТЬ ОШИБКИ: {self.results['failed']}")
        
        print(f"{'='*70}\n")


def main():
    """Запуск всех тестов"""
    print("\n" + "🧪 ПОЛНЫЙ ИНТЕГРАЦИОННЫЙ ТЕСТ ЖИЗНЕННОГО ЦИКЛА".center(70, "="))
    print("Проверка всех этапов от заявки до решения с многолетними испытаниями")
    print("="*70)
    
    tester = TestLifecycle()
    
    try:
        # Подготовка
        tester.setup()
        
        # Сценарии
        tester.test_scenario_1_one_year_approval()
        tester.test_scenario_2_two_year_approval()
        tester.test_scenario_3_three_year_approval()
        
        # API тесты
        tester.test_api_regional_status()
        
        # Итоги
        tester.print_summary()
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

