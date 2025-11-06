"""
Сервис для основной информации и детальных данных годового отчета
"""
from django.utils import timezone
from django.db import models as django_models

from ...models import (
    Region, Trial, TrialParticipant, TrialResult, Application
)


class BasicReportService:
    """
    Сервис для генерации основной информации и детальных данных годового отчета
    
    Включает:
    - Основную информацию (oblast, year, regions)
    - Детальные данные (detailed_items)
    - Предупреждения (warnings)
    """
    
    def __init__(self):
        self.maturity_groups = {
            'D01': 'Ранняя группа',
            'D02': 'Среднеранняя группа', 
            'D03': 'Средняя группа (среднеспелая)',
            'D04': 'Среднепоздняя группа',
            'D05': 'Поздняя группа',
            'D06': 'Очень ранняя группа',
            'D07': 'Среднеранняя',
            'unknown': 'Группа не указана'
        }
    
    def generate_basic_report(self, oblast, year, patents_culture_id=None, recalculate_years=False):
        """
        Генерация основной информации и детальных данных

        Args:
        - oblast: объект области
        - year: отчетный год
        - patents_culture_id: ID культуры из Patents для фильтрации (опционально)
        - recalculate_years: Пересчитать years_tested по всем годам (для summary)

        Returns:
        - oblast: информация об области
        - year: отчетный год
        - years_range: диапазон лет
        - generated_at: время генерации
        - regions: список ГСУ
        - detailed_items: детальные данные
        - warnings: предупреждения
        - has_warnings: есть ли предупреждения
        - culture_filter: информация о примененном фильтре (если есть)
        """
        regions = Region.objects.filter(oblast=oblast, is_deleted=False).order_by('name')
        years_range = [year-2, year-1, year]
        
        detailed_items = []
        warnings = []
        row_number = 1
        
        # 1. Детализация по регионам
        for region in regions:
            # Найти все испытания в регионе за период
            trial_ids = Trial.objects.filter(
                region=region,
                year__in=years_range,
                is_deleted=False
            ).values_list('id', flat=True)
            
            if not trial_ids:
                continue
            
            # Найти стандартные сорта по ГРУППАМ СПЕЛОСТИ И ПРЕДШЕСТВЕННИКАМ за текущий год
            current_year_trial_ids = Trial.objects.filter(
                region=region,
                year=year,
                is_deleted=False
            ).values_list('id', flat=True)

            standard_participants = TrialParticipant.objects.filter(
                trial__id__in=current_year_trial_ids,
                statistical_group=0,  # 0 = стандарт, 1 = испытываемый
                is_deleted=False
            ).select_related('sort_record', 'trial', 'trial__predecessor_culture')

            # Группировать стандарты по (maturity_group_code, predecessor_key)
            standards_by_group = {}  # {(group_code, predecessor_key): best_standard}
            all_standards_by_group = {}  # {(group_code, predecessor_key): {sort_id: participant}}

            for participant in standard_participants:
                group_code = participant.maturity_group_code or 'unknown'
                predecessor_key = self._get_predecessor_key(participant.trial)
                composite_key = (group_code, predecessor_key)

                # Разрешаем стандарты с любым статусом (убрана проверка patents_status)
                # Ранее фильтровались сорта с patents_status != 1, теперь все статусы разрешены
                # if participant.sort_record.patents_status is not None and participant.sort_record.patents_status != 1:
                #     continue

                # Собрать УНИКАЛЬНЫЕ стандарты в группе (с учетом предшественника)
                if composite_key not in all_standards_by_group:
                    all_standards_by_group[composite_key] = {}
                # Сохраняем participant вместо sort_record, чтобы иметь доступ к application_id
                all_standards_by_group[composite_key][participant.sort_record.id] = participant

            # Выбрать ЛУЧШИЙ стандарт в каждой группе (group_code, predecessor_key)
            for composite_key, standards_dict in all_standards_by_group.items():
                group_code, predecessor_key = composite_key
                standards_list = list(standards_dict.values())  # Список participants

                if len(standards_list) == 1:
                    standards_by_group[composite_key] = standards_list[0].sort_record
                else:
                    # Выбрать стандарт с максимальной урожайностью за текущий год
                    # С УЧЕТОМ ПРЕДШЕСТВЕННИКА
                    best_standard = None
                    max_yield = 0

                    for participant in standards_list:
                        std_data = self._get_trial_data_by_sort(participant.sort_record, region, [year], group_code, predecessor_key)
                        current_yield = std_data.get('current_year_yield', 0) or 0

                        if current_yield > max_yield:
                            max_yield = current_yield
                            best_standard = participant.sort_record

                    standards_by_group[composite_key] = best_standard if best_standard else standards_list[0].sort_record

            # Найти все сорта (включая стандарты и испытываемые)
            trial_participants = TrialParticipant.objects.filter(
                trial__id__in=trial_ids,
                is_deleted=False
            ).select_related('application', 'sort_record', 'trial', 'trial__predecessor_culture')

            # Группировать участников по заявкам с группой спелости И ПРЕДШЕСТВЕННИКОМ
            apps_with_groups = {}
            standards_with_groups = {}

            for participant in trial_participants:
                group_code = participant.maturity_group_code or 'unknown'
                predecessor_key = self._get_predecessor_key(participant.trial)

                # ИСПРАВЛЕНО: Сначала проверяем наличие application
                # Если есть application, добавляем как испытываемый сорт (даже если statistical_group=0)
                if participant.application:
                    # Испытываемые сорта (включая стандарты с заявкой)
                    # КЛЮЧ: (app_id, maturity_group, predecessor)
                    composite_key = (participant.application.id, group_code, predecessor_key)
                    if composite_key not in apps_with_groups:
                        apps_with_groups[composite_key] = {
                            'application': participant.application,
                            'maturity_group_code': group_code,
                            'predecessor_key': predecessor_key,
                            'predecessor_display': self._get_predecessor_display(participant.trial),
                            'trial': participant.trial
                        }
                elif participant.statistical_group == 0:
                    # Стандарты БЕЗ заявки (только те, у кого нет application)
                    # КЛЮЧ: (sort_id, maturity_group, predecessor)
                    composite_key = (participant.sort_record.id, group_code, predecessor_key)
                    if composite_key not in standards_with_groups:
                        standards_with_groups[composite_key] = {
                            'sort_record': participant.sort_record,
                            'maturity_group_code': group_code,
                            'statistical_group': participant.statistical_group,
                            'predecessor_key': predecessor_key,
                            'predecessor_display': self._get_predecessor_display(participant.trial),
                            'trial': participant.trial
                        }
            
            # Добавить испытываемые сорта
            for app_data in apps_with_groups.values():
                app = app_data['application']
                group_code = app_data['maturity_group_code']
                predecessor_key = app_data['predecessor_key']
                predecessor_display = app_data['predecessor_display']

                # Получить данные по КОНКРЕТНОМУ предшественнику
                trial_data = self._get_trial_data_by_application(
                    app, region, years_range, group_code, predecessor_key, recalculate_years
                )

                # Вычислить отклонение от стандарта только за отчетный год
                # С УЧЕТОМ ПРЕДШЕСТВЕННИКА
                composite_key = (group_code, predecessor_key)
                region_standard = standards_by_group.get(composite_key)
                if region_standard and trial_data.get('current_year_yield'):
                    # Получить данные стандарта только за отчетный год
                    # С ТЕМ ЖЕ ПРЕДШЕСТВЕННИКОМ
                    standard_data = self._get_trial_data_by_sort(
                        region_standard, region, [year], group_code, predecessor_key
                    )

                    if standard_data.get('current_year_yield'):
                        deviation = trial_data['current_year_yield'] - standard_data['current_year_yield']
                        deviation_percent = (deviation / standard_data['current_year_yield']) * 100
                        trial_data['deviation_from_standard'] = round(deviation, 1)
                        trial_data['deviation_percent'] = round(deviation_percent, 1)
                        trial_data['standard_name'] = region_standard.name
                        trial_data['standard_current_year_yield'] = standard_data['current_year_yield']
                
                # Получить данные об устойчивости
                resistance_indicators = self._get_resistance_indicators(app, region, years_range)
                if resistance_indicators:
                    trial_data['resistance_indicators'] = resistance_indicators
                
                # Получить текущий статус решения
                decision_status = app.get_oblast_status(oblast)
                latest_decision = app.get_latest_decision(oblast)
                
                item = {
                    'row_number': row_number,
                    'region': {
                        'id': region.id,
                        'name': region.name,
                        'climate_zone': {
                            'id': region.climate_zone.id if region.climate_zone else None,
                            'name': region.climate_zone.name if region.climate_zone else None,
                            'code': region.climate_zone.code if region.climate_zone else None
                        } if region.climate_zone else None
                    },
                    'sort_record': {
                        'id': app.sort_record.id,
                        'name': app.sort_record.name,
                        'culture_name': app.sort_record.culture.name if app.sort_record.culture else None,
                        'culture_id': app.sort_record.culture.culture_id if app.sort_record.culture else None
                    },
                    'maturity_group_code': group_code,
                    'maturity_group_name': self._get_maturity_group_name(group_code),
                    'predecessor': predecessor_display,
                    'predecessor_key': predecessor_key,
                    'is_standard': False,
                    'application_id': app.id,
                    'application_number': app.application_number,
                    'trial_data': trial_data,
                    'can_make_decision': True,
                    'decision_status': decision_status,
                    'latest_decision': {
                        'year': latest_decision.year,
                        'decision': latest_decision.decision,
                        'decision_display': latest_decision.get_decision_display(),
                        'date': str(latest_decision.decision_date)
                    } if latest_decision else None,
                    'standard_for_group': region_standard.name if region_standard else None
                }
                
                detailed_items.append(item)
                row_number += 1
            
            # Добавить стандарты
            for std_data in standards_with_groups.values():
                sort_record = std_data['sort_record']
                group_code = std_data['maturity_group_code']
                statistical_group = std_data['statistical_group']
                predecessor_key = std_data['predecessor_key']
                predecessor_display = std_data['predecessor_display']

                # Получить данные с учетом предшественника
                trial_data = self._get_trial_data_by_sort(
                    sort_record, region, years_range, group_code, predecessor_key
                )

                item = {
                    'row_number': row_number,
                    'region': {
                        'id': region.id,
                        'name': region.name,
                        'climate_zone': {
                            'id': region.climate_zone.id if region.climate_zone else None,
                            'name': region.climate_zone.name if region.climate_zone else None,
                            'code': region.climate_zone.code if region.climate_zone else None
                        } if region.climate_zone else None
                    },
                    'sort_record': {
                        'id': sort_record.id,
                        'name': sort_record.name,
                        'culture_name': sort_record.culture.name if sort_record.culture else None,
                        'culture_id': sort_record.culture.culture_id if sort_record.culture else None
                    },
                    'maturity_group_code': group_code,
                    'maturity_group_name': self._get_maturity_group_name(group_code),
                    'predecessor': predecessor_display,
                    'predecessor_key': predecessor_key,
                    'is_standard': True,
                    'is_comparison_standard': (statistical_group == 0),
                    'application_id': None,
                    'application_number': None,
                    'trial_data': trial_data,
                    'can_make_decision': False,
                    'decision_status': None,
                    'latest_decision': None,
                    'standard_for_group': None
                }
                
                detailed_items.append(item)
                row_number += 1

        # Фильтрация по культуре (если указан patents_culture_id)
        culture_filter_info = None
        if patents_culture_id is not None:
            filtered_items = []
            for item in detailed_items:
                # Проверяем culture_id через sort_record или culture
                if (item.get('sort_record', {}).get('culture_id') == patents_culture_id or
                    item.get('culture', {}).get('culture_id') == patents_culture_id):
                    filtered_items.append(item)
            detailed_items = filtered_items

            # Получить название культуры для информации о фильтре
            from ...models import Culture
            try:
                culture = Culture.objects.get(culture_id=patents_culture_id, is_deleted=False)
                culture_filter_info = {
                    'patents_culture_id': patents_culture_id,
                    'culture_name': culture.name
                }
            except Culture.DoesNotExist:
                culture_filter_info = {
                    'patents_culture_id': patents_culture_id,
                    'culture_name': f'Culture ID {patents_culture_id}'
                }

        result = {
            'oblast': {
                'id': oblast.id,
                'name': oblast.name
            },
            'year': year,
            'years_range': years_range,
            'generated_at': timezone.now(),
            'regions': [{'id': r.id, 'name': r.name} for r in regions],
            'detailed_items': detailed_items,
            'warnings': warnings,
            'has_warnings': len(warnings) > 0
        }

        # Добавляем информацию о фильтре, если он применен
        if culture_filter_info:
            result['culture_filter'] = culture_filter_info

        return result
    
    def _get_trial_data_by_sort(self, sort_record, region, years, maturity_group_code=None, predecessor_key=None):
        """
        Получить данные испытаний для сорта-стандарта в регионе

        Args:
            sort_record: Запись сорта
            region: Регион
            years: Список годов
            maturity_group_code: Код группы спелости (опционально)
            predecessor_key: Ключ предшественника для фильтрации (опционально)

        Returns:
            Словарь с данными урожайности
        """
        yields_by_year = {}

        for y in years:
            filters = {
                'sort_record': sort_record,
                'trial__region': region,
                'trial__year': y,
                'statistical_group': 0,  # Стандарты
                'is_deleted': False
            }

            if maturity_group_code:
                filters['maturity_group_code'] = maturity_group_code

            # Получить участников
            participants = TrialParticipant.objects.filter(**filters).select_related('trial', 'trial__predecessor_culture')

            # Фильтровать по предшественнику, если указан
            trial_ids = []
            if predecessor_key:
                for participant in participants:
                    if self._get_predecessor_key(participant.trial) == predecessor_key:
                        trial_ids.append(participant.trial_id)
            else:
                trial_ids = list(participants.values_list('trial_id', flat=True))
            
            trials = Trial.objects.filter(
                id__in=trial_ids,
                is_deleted=False
            )
            
            if trials.exists():
                for trial in trials:
                    yield_results = TrialResult.objects.filter(
                        trial=trial,
                        sort_record=sort_record,
                        indicator__code='yield',
                        is_deleted=False
                    )
                    
                    if yield_results.exists():
                        avg_yield = yield_results.aggregate(
                            avg=django_models.Avg('value')
                        )['avg']
                        
                        if avg_yield:
                            yields_by_year[y] = round(float(avg_yield), 1)
        
        average_yield = None
        if yields_by_year:
            average_yield = round(sum(yields_by_year.values()) / len(yields_by_year), 1)
        
        current_year = max(years) if years else None
        current_year_yield = yields_by_year.get(current_year) if current_year else None
        
        return {
            'years_tested': len(yields_by_year),
            'year_started': min(yields_by_year.keys()) if yields_by_year else None,
            'yields_by_year': yields_by_year,
            'average_yield': average_yield,
            'current_year_yield': current_year_yield,
            'has_data': len(yields_by_year) > 0
        }

    def _get_trial_data_by_application(self, application, region, years, maturity_group_code=None, predecessor_key=None, recalculate_years=False):
        """
        Получить данные испытаний для заявки в регионе

        Args:
            application: Заявка
            region: Регион
            years: Список годов
            maturity_group_code: Код группы спелости (опционально)
            predecessor_key: Ключ предшественника для фильтрации (опционально)
            recalculate_years: Если True, игнорировать фильтр по предшественнику

        Returns:
            Словарь с данными урожайности
        """
        yields_by_year = {}

        for y in years:
            filters = {
                'application': application,
                'sort_record': application.sort_record,
                'trial__region': region,
                'trial__year': y,
                'is_deleted': False
            }

            if maturity_group_code:
                filters['maturity_group_code'] = maturity_group_code

            # Получить участников
            participants = TrialParticipant.objects.filter(**filters).select_related('trial', 'trial__predecessor_culture')

            # Фильтровать по предшественнику, если указан
            # НО: если recalculate_years=True, игнорируем фильтр по предшественнику
            trial_ids = []
            if predecessor_key and not recalculate_years:
                for participant in participants:
                    if self._get_predecessor_key(participant.trial) == predecessor_key:
                        trial_ids.append(participant.trial_id)
            else:
                trial_ids = list(participants.values_list('trial_id', flat=True))
            
            if trial_ids:
                yield_results = TrialResult.objects.filter(
                    trial__id__in=trial_ids,
                    sort_record=application.sort_record,
                    indicator__code='yield',
                    is_deleted=False
                )
                
                if yield_results.exists():
                    avg_yield = yield_results.aggregate(
                        avg=django_models.Avg('value')
                    )['avg']
                    
                    if avg_yield:
                        yields_by_year[y] = round(float(avg_yield), 1)

        average_yield = None
        if yields_by_year:
            average_yield = round(sum(yields_by_year.values()) / len(yields_by_year), 1)

        current_year = max(years) if years else None
        current_year_yield = yields_by_year.get(current_year) if current_year else None

        return {
            'years_tested': len(yields_by_year),
            'year_started': min(yields_by_year.keys()) if yields_by_year else None,
            'yields_by_year': yields_by_year,
            'average_yield': average_yield,
            'current_year_yield': current_year_yield,
            'has_data': len(yields_by_year) > 0
        }
    
    def _get_resistance_indicators(self, application, region, years_range):
        """
        Получить показатели устойчивости для заявки в регионе
        
        Args:
            application: Заявка
            region: Регион
            years_range: Диапазон лет
            
        Returns:
            Словарь показателей устойчивости
        """
        from trials_app.models import TrialResult, TrialParticipant, Indicator
        
        # Найти участников заявки в регионе
        participants = TrialParticipant.objects.filter(
            application=application,
            trial__region=region,
            trial__year__in=years_range,
            is_deleted=False
        )
        
        if not participants.exists():
            return {}
        
        # Найти показатели устойчивости
        resistance_indicators = Indicator.objects.filter(
            name__icontains='устойчивость',
            is_deleted=False
        )
        
        # Получить результаты по устойчивости
        resistance_results = TrialResult.objects.filter(
            participant__in=participants,
            indicator__in=resistance_indicators,
            is_deleted=False
        ).select_related('indicator')
        
        # Сгруппировать по показателям и взять среднее значение
        indicators_data = {}
        for result in resistance_results:
            if result.value is not None:
                indicator_name = result.indicator.name
                if indicator_name not in indicators_data:
                    indicators_data[indicator_name] = []
                indicators_data[indicator_name].append(result.value)
        
        # Вычислить средние значения
        resistance_indicators = {}
        for indicator_name, values in indicators_data.items():
            if values:
                avg_value = sum(values) / len(values)
                # Преобразовать название для API
                api_name = self._convert_resistance_name(indicator_name)
                resistance_indicators[api_name] = round(avg_value, 1)
        
        return resistance_indicators
    
    def _convert_resistance_name(self, indicator_name):
        """
        Преобразовать название показателя устойчивости для API
        
        Args:
            indicator_name: Название показателя из базы
            
        Returns:
            Название для API
        """
        name_mapping = {
            'Устойчивость к болезням и вредителям': 'disease_resistance',
            'Устойчивость к полеганию': 'lodging_resistance', 
            'Устойчивость к засухе': 'drought_resistance',
            'Устойчивость к осыпанию': 'shattering_resistance',
            'Устойчивость к прорастанию на корню': 'sprouting_resistance',
            'Устойчивость к пониканию / ломкости колоса': 'lodging_resistance',
            'Устойчивость к цветушности': 'bolting_resistance'
        }
        
        return name_mapping.get(indicator_name, indicator_name.lower().replace(' ', '_'))
    
    def _get_maturity_group_name(self, group_code):
        """Получить название группы спелости по коду"""
        return self.maturity_groups.get(group_code, f'Группа {group_code}')

    def _get_predecessor_key(self, trial):
        """
        Получить ключ предшественника для группировки с нормализацией

        Args:
            trial: Объект испытания

        Returns:
            Строка-ключ предшественника (culture_name или predecessor_code)
        """
        if trial.predecessor_culture:
            return f"culture_{trial.predecessor_culture.id}"
        elif trial.predecessor_code:
            # Пытаемся найти культуру по названию для нормализации
            from trials_app.models import Culture
            culture = Culture.objects.filter(
                name__iexact=trial.predecessor_code.strip(),
                is_deleted=False
            ).first()
            if culture:
                return f"culture_{culture.id}"
            return f"code_{trial.predecessor_code}"
        return "unknown"

    def _get_predecessor_display(self, trial):
        """
        Получить отображаемое название предшественника

        Args:
            trial: Объект испытания

        Returns:
            Название предшественника для отображения
        """
        if trial.predecessor_culture:
            return trial.predecessor_culture.name
        elif trial.predecessor_code:
            return trial.predecessor_code
        return "Не указан"
