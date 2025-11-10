"""
Сервис для генерации рекомендаций (summary) по сортам
"""
from collections import defaultdict
from django.db.models import Avg
from django.utils import timezone

from ...models import Region, Trial, TrialParticipant, TrialResult, Indicator, Culture
from .summary_service import SummaryService
from .culture_filter_service import CultureFilterService


class MethodologySummaryService:
    """
    Сервис для генерации рекомендаций по сортам

    Генерирует:
    - Рекомендации по application_number
    - Балльные оценки
    - Статусы решений (decision_status, latest_decision)
    - Статистический анализ

    Напрямую запрашивает данные из TrialParticipant/TrialResult
    для корректного расчета years_tested по всем регионам и предшественникам
    """

    def __init__(self):
        self.summary_service = SummaryService()

    def generate_recommendations(self, oblast, year, patents_culture_id=None):
        """
        Генерация рекомендаций для сортов

        Args:
            oblast: Объект области
            year: Год отчета
            patents_culture_id: ID культуры из Patents для фильтрации (опционально)

        Returns:
            dict: {
                'metadata': {...},
                'recommendations': {
                    'application_number': {
                        evaluation_scores, recommendation, decision_status, ...
                    }
                }
            }
        """
        # Получаем данные напрямую из БД
        years_range = [year - 2, year - 1, year]
        detailed_items = self._get_trial_data_for_summary(oblast, years_range, year, patents_culture_id)

        # Генерация summary items через SummaryService
        summary_items = self.summary_service.generate_summary_items(
            oblast,
            year,
            detailed_items
        )

        # Создать словарь рекомендаций по application_number
        recommendations_by_application = self._format_recommendations(summary_items)

        # Получить информацию о фильтре культуры
        culture_filter_info = CultureFilterService.get_culture_info(patents_culture_id)

        # Получить информацию об области и регионах
        regions = Region.objects.filter(oblast=oblast, is_deleted=False).order_by('name')

        return {
            'oblast': {
                'id': oblast.id,
                'name': oblast.name
            },
            'year': year,
            'generated_at': timezone.now(),
            'culture_filter': culture_filter_info,
            'recommendations': recommendations_by_application
        }

    def _get_trial_data_for_summary(self, oblast, years_range, current_year, patents_culture_id=None):
        """
        Получить данные испытаний напрямую из БД для summary

        Для каждого сорта собирает ВСЕ данные по всем регионам и предшественникам
        ВАЖНО: Собирает данные по sort_record, даже если раньше не было application

        Args:
            oblast: Объект области
            years_range: Список лет для анализа
            current_year: Текущий год отчета
            patents_culture_id: ID культуры для фильтрации (опционально)

        Returns:
            list: detailed_items с данными по всем комбинациям (application, region, predecessor)
        """
        # Получить все регионы области
        regions = Region.objects.filter(oblast=oblast, is_deleted=False)
        region_ids = list(regions.values_list('id', flat=True))

        # Шаг 1: Получить все заявки с данными в этой области
        from ...models import Application
        applications = Application.objects.filter(
            trial_participations__trial__region_id__in=region_ids,
            trial_participations__trial__year__in=years_range,
            trial_participations__is_deleted=False,
            is_deleted=False
        ).select_related('sort_record', 'sort_record__culture').distinct()

        # Фильтрация по культуре (если указан patents_culture_id)
        if patents_culture_id is not None:
            applications = applications.filter(
                sort_record__culture__culture_id=patents_culture_id
            )

        # Шаг 2: Для каждой заявки собрать ВСЕ данные по sort_record (даже без application)
        all_participants = []
        
        for application in applications:
            # Получить ВСЕХ участников с этим sort_record (включая записи без application)
            sort_participants = TrialParticipant.objects.filter(
                sort_record=application.sort_record,
                trial__region_id__in=region_ids,
                trial__year__in=years_range,
                is_deleted=False
            ).select_related(
                'application',
                'sort_record',
                'trial',
                'trial__region',
                'trial__region__climate_zone',
                'trial__predecessor_culture'
            )
            
            # Для каждого participant привязываем application
            for p in sort_participants:
                # Принудительно устанавливаем application для группировки
                p._summary_application = application
                all_participants.append(p)

        participants = all_participants

        # Группируем данные по (application, region, maturity_group, predecessor)
        # Для каждой комбинации собираем yields_by_year
        grouped_data = defaultdict(lambda: {
            'application': None,
            'region': None,
            'maturity_group_code': None,
            'predecessor_key': None,
            'predecessor_name': None,
            'yields_by_year': {}
        })

        yield_indicator = Indicator.objects.filter(code='yield').first()

        for participant in participants:
            # Используем _summary_application вместо application
            application = participant._summary_application if hasattr(participant, '_summary_application') else participant.application
            if not application:
                continue
                
            region = participant.trial.region
            maturity_group_code = participant.maturity_group_code or 'unknown'
            predecessor_key = self._get_predecessor_key(participant.trial)
            predecessor_name = self._get_predecessor_name(participant.trial)
            year = participant.trial.year

            # Ключ для группировки: (app_id, region_id, maturity_group, predecessor_key)
            group_key = (
                application.id,
                region.id,
                maturity_group_code,
                predecessor_key
            )

            # Сохраняем метаданные для этой группы
            if grouped_data[group_key]['application'] is None:
                grouped_data[group_key]['application'] = application
                grouped_data[group_key]['region'] = region
                grouped_data[group_key]['maturity_group_code'] = maturity_group_code
                grouped_data[group_key]['predecessor_key'] = predecessor_key
                grouped_data[group_key]['predecessor_name'] = predecessor_name
            
            # Добавляем год в список (пока без данных урожайности)
            if year not in grouped_data[group_key]['yields_by_year']:
                grouped_data[group_key]['yields_by_year'][year] = None

        # Теперь для каждой группы получаем урожайность по годам
        for group_key, data in grouped_data.items():
            application = data['application']
            region = data['region']
            maturity_group_code = data['maturity_group_code']
            predecessor_key = data['predecessor_key']
            
            # Для каждого года в yields_by_year получаем данные
            for year in list(data['yields_by_year'].keys()):
                # Найти всех участников для этой комбинации в данном году
                # ВАЖНО: Ищем по sort_record, а не по application!
                year_participants = TrialParticipant.objects.filter(
                    sort_record=application.sort_record,
                    trial__region=region,
                    trial__year=year,
                    maturity_group_code=maturity_group_code,
                    is_deleted=False
                ).select_related('trial', 'trial__predecessor_culture')

                # Фильтруем по predecessor_key
                trial_ids = []
                for p in year_participants:
                    if self._get_predecessor_key(p.trial) == predecessor_key:
                        trial_ids.append(p.trial_id)

                if trial_ids:
                    # Получить результаты урожайности для всех отфильтрованных trials
                    # ВАЖНО: Ищем по sort_record!
                    results = TrialResult.objects.filter(
                        trial_id__in=trial_ids,
                        participant__sort_record=application.sort_record,
                        indicator=yield_indicator,
                        is_deleted=False
                    )

                    if results.exists():
                        avg_yield = results.aggregate(avg=Avg('value'))['avg']
                        if avg_yield:
                            grouped_data[group_key]['yields_by_year'][year] = round(float(avg_yield), 1)
                        else:
                            # Удаляем год, если нет данных
                            del grouped_data[group_key]['yields_by_year'][year]
                    else:
                        # Удаляем год, если нет результатов
                        del grouped_data[group_key]['yields_by_year'][year]
                else:
                    # Удаляем год, если нет trials
                    del grouped_data[group_key]['yields_by_year'][year]

        # Преобразуем сгруппированные данные в detailed_items
        detailed_items = []

        for group_key, data in grouped_data.items():
            application = data['application']
            region = data['region']
            yields_by_year = data['yields_by_year']

            if not yields_by_year:
                # Нет данных по урожайности - пропускаем
                continue

            # Рассчитываем агрегированные метрики
            average_yield = round(sum(yields_by_year.values()) / len(yields_by_year), 1) if yields_by_year else None
            years_tested = len(yields_by_year)
            year_started = min(yields_by_year.keys()) if yields_by_year else None
            current_year_yield = yields_by_year.get(current_year)

            # Получить статусы решений
            decision_status = application.get_oblast_status(oblast)
            latest_decision = application.get_latest_decision(oblast)

            # Получить данные качества и устойчивости за весь период
            quality_indicators = self._get_quality_indicators(application, region, years_range)
            resistance_indicators = self._get_resistance_indicators(application, region, years_range)
            
            # Рассчитать отклонение от стандарта для текущего года
            deviation_data = self._calculate_deviation_from_standard(
                application, region, data['maturity_group_code'], 
                data['predecessor_key'], current_year, current_year_yield
            )

            detailed_items.append({
                'application_id': application.id,
                'application_number': application.application_number,
                'sort_record': {
                    'id': application.sort_record.id,
                    'name': application.sort_record.name,
                    'patents_status': application.sort_record.patents_status
                },
                'maturity_group_code': data['maturity_group_code'],
                'maturity_group_name': self._get_maturity_group_name(data['maturity_group_code']),
                'predecessor_key': data['predecessor_key'],
                'predecessor': data['predecessor_name'],
                'region': {
                    'id': region.id,
                    'name': region.name,
                    'climate_zone': {
                        'id': region.climate_zone.id if region.climate_zone else None,
                        'name': region.climate_zone.name if region.climate_zone else None,
                        'code': region.climate_zone.code if region.climate_zone else None
                    } if region.climate_zone else None
                },
                'trial_data': {
                    'yields_by_year': yields_by_year,
                    'average_yield': average_yield,
                    'years_tested': years_tested,
                    'year_started': year_started,
                    'current_year_yield': current_year_yield,
                    'has_data': years_tested > 0,
                    **deviation_data  # Добавляем данные отклонения от стандарта
                },
                'quality_indicators': quality_indicators,
                'resistance_indicators': resistance_indicators,
                'decision_status': decision_status,
                'latest_decision': {
                    'year': latest_decision.year,
                    'decision': latest_decision.decision,
                    'decision_display': latest_decision.get_decision_display(),
                    'date': str(latest_decision.decision_date)
                } if latest_decision else None
            })

        return detailed_items

    def _get_predecessor_key(self, trial):
        """
        Получить ключ предшественника из trial с нормализацией

        Args:
            trial: Объект испытания

        Returns:
            str: Ключ предшественника
        """
        if trial.predecessor_culture:
            return f"culture_{trial.predecessor_culture.id}"
        elif trial.predecessor_code:
            # Пытаемся найти культуру по названию для нормализации
            culture = Culture.objects.filter(
                name__iexact=trial.predecessor_code.strip(),
                is_deleted=False
            ).first()
            if culture:
                return f"culture_{culture.id}"
            return f"code_{trial.predecessor_code}"
        return "unknown"

    def _get_predecessor_name(self, trial):
        """
        Получить отображаемое название предшественника из trial

        Args:
            trial: Объект испытания

        Returns:
            str: Название предшественника
        """
        if trial.predecessor_culture:
            return trial.predecessor_culture.name
        elif trial.predecessor_code:
            # Пытаемся найти культуру для получения нормализованного названия
            culture = Culture.objects.filter(
                name__iexact=trial.predecessor_code.strip(),
                is_deleted=False
            ).first()
            if culture:
                return culture.name
            return trial.predecessor_code
        return "Неизвестно"

    def _get_maturity_group_name(self, group_code):
        """
        Получить название группы спелости по коду

        Args:
            group_code: Код группы спелости

        Returns:
            str: Название группы спелости
        """
        maturity_groups = {
            'D01': 'Ранняя группа',
            'D02': 'Среднеранняя группа',
            'D03': 'Средняя группа (среднеспелая)',
            'D04': 'Среднепоздняя группа',
            'D05': 'Поздняя группа',
            'D06': 'Очень ранняя группа',
            'D07': 'Среднеранняя',
            'unknown': 'Группа не указана'
        }
        return maturity_groups.get(group_code, f'Группа {group_code}')

    def _format_recommendations(self, summary_items):
        """
        Форматирование данных по application_number

        Args:
            summary_items: Список summary items

        Returns:
            dict: {application_number: {sort_name, evaluation_scores, violations, ...}}
        """
        recommendations_by_application = {}

        for item in summary_items:
            application_number = item.get('application_number')
            if application_number:
                recommendations_by_application[application_number] = {
                    'application_id': item['application_id'],
                    'application_number': application_number,
                    'sort_record': {
                        'id': item['sort_record']['id'],
                        'name': item['sort_record']['name'],
                        'patents_status': item['sort_record'].get('patents_status')
                    },
                    'evaluation_scores': item.get('evaluation_scores', {}),
                    'violations': item.get('violations', []),  # Заменяет recommendation
                    'summary': item.get('overall_summary', {}),
                    'decision_status': item.get('decision_status'),
                    'latest_decision': item.get('latest_decision')
                }

        return recommendations_by_application
    
    def _get_quality_indicators(self, application, region, years_range):
        """
        Получить показатели качества для заявки в регионе за весь период испытаний
        
        Args:
            application: Заявка
            region: Регион
            years_range: Диапазон лет
            
        Returns:
            Dict показателей качества (усредненные)
        """
        from ...models import TrialLaboratoryResult, TrialParticipant
        
        # Собираем все лабораторные результаты за весь период
        indicators_data = {}
        
        for year in years_range:
            participants = TrialParticipant.objects.filter(
                sort_record=application.sort_record,
                trial__region=region,
                trial__year=year,
                is_deleted=False
            ).values_list('trial_id', flat=True)
            
            if not participants:
                continue
            
            lab_results = TrialLaboratoryResult.objects.filter(
                trial_id__in=participants,
                participant__sort_record=application.sort_record,
                is_deleted=False
            ).select_related('indicator')
            
            for result in lab_results:
                if result.value is not None:
                    indicator_code = result.indicator.code
                    if indicator_code not in indicators_data:
                        indicators_data[indicator_code] = []
                    indicators_data[indicator_code].append(result.value)
        
        # Усредняем показатели за все годы
        quality_indicators = {}
        for indicator_code, values in indicators_data.items():
            if values:
                avg_value = sum(values) / len(values)
                quality_indicators[indicator_code] = round(avg_value, 1)
        
        return quality_indicators
    
    def _get_resistance_indicators(self, application, region, years_range):
        """
        Получить показатели устойчивости для заявки в регионе за весь период испытаний
        
        Args:
            application: Заявка
            region: Регион
            years_range: Диапазон лет
            
        Returns:
            Dict показателей устойчивости (усредненные)
        """
        from ...models import TrialResult, TrialParticipant, Indicator
        
        # Найти показатели устойчивости
        resistance_indicators = Indicator.objects.filter(
            name__icontains='устойчивость',
            is_deleted=False
        )
        
        # Собираем все результаты за весь период
        indicators_data = {}
        
        for year in years_range:
            participants = TrialParticipant.objects.filter(
                sort_record=application.sort_record,
                trial__region=region,
                trial__year=year,
                is_deleted=False
            ).values_list('id', flat=True)
            
            if not participants:
                continue
            
            resistance_results = TrialResult.objects.filter(
                participant_id__in=participants,
                indicator__in=resistance_indicators,
                is_deleted=False
            ).select_related('indicator')
            
            for result in resistance_results:
                # Фильтруем нулевые значения (0.0 = нет данных/не поражен)
                if result.value is not None and result.value > 0:
                    indicator_name = result.indicator.name
                    if indicator_name not in indicators_data:
                        indicators_data[indicator_name] = []
                    indicators_data[indicator_name].append(result.value)
        
        # Усредняем и конвертируем названия
        resistance_data = {}
        for indicator_name, values in indicators_data.items():
            if values:
                # Фильтруем выбросы (значения >10 на шкале 1-10)
                valid_values = [v for v in values if 0 <= v <= 10]
                
                if valid_values:
                    avg_value = sum(valid_values) / len(valid_values)
                    api_name = self._convert_resistance_name(indicator_name)
                    
                    # Если уже есть показатель с таким именем, усредняем
                    if api_name in resistance_data:
                        # Усредняем с существующим значением
                        resistance_data[api_name] = round((resistance_data[api_name] + avg_value) / 2, 1)
                    else:
                        resistance_data[api_name] = round(avg_value, 1)
        
        return resistance_data
    
    def _convert_resistance_name(self, indicator_name):
        """
        Преобразовать название показателя устойчивости для API
        
        Args:
            indicator_name: Название показателя из базы
            
        Returns:
            Название для API
        """
        # Нормализация: убираем детали в скобках для группировки
        base_name = indicator_name.split('(')[0].strip()
        
        name_mapping = {
            'Устойчивость к болезням и вредителям': 'disease_resistance',
            'Устойчивость к полеганию': 'lodging_resistance',
            'Устойчивость к засухе': 'drought_resistance',
            'Устойчивость к осыпанию': 'shattering_resistance',
            'Устойчивость к прорастанию на корню': 'sprouting_resistance',
            'Устойчивость к пониканию / ломкости колоса': 'lodging_resistance',
            'Устойчивость к цветушности': 'bolting_resistance',
            'Зимостойкость': 'winter_hardiness'
        }
        
        # Проверяем сначала базовое название
        if base_name in name_mapping:
            return name_mapping[base_name]
        
        return name_mapping.get(indicator_name, indicator_name.lower().replace(' ', '_'))
    
    def _calculate_deviation_from_standard(self, application, region, maturity_group_code, 
                                          predecessor_key, current_year, current_year_yield):
        """
        Рассчитать отклонение от стандарта для сорта в регионе
        
        Args:
            application: Заявка
            region: Регион
            maturity_group_code: Код группы спелости
            predecessor_key: Ключ предшественника
            current_year: Текущий год отчета
            current_year_yield: Урожайность сорта в текущем году
            
        Returns:
            Dict с данными отклонения от стандарта
        """
        if not current_year_yield:
            return {}
        
        # Найти стандарт для этой группы спелости и предшественника
        current_year_trials = Trial.objects.filter(
            region=region,
            year=current_year,
            is_deleted=False
        ).values_list('id', flat=True)
        
        standard_participants = TrialParticipant.objects.filter(
            trial__id__in=current_year_trials,
            statistical_group=0,  # Стандарт
            maturity_group_code=maturity_group_code,
            is_deleted=False
        ).select_related('sort_record', 'trial', 'trial__predecessor_culture')
        
        # Фильтруем по predecessor_key
        standard_sort = None
        for participant in standard_participants:
            if self._get_predecessor_key(participant.trial) == predecessor_key:
                standard_sort = participant.sort_record
                break
        
        if not standard_sort:
            return {}
        
        # Получить урожайность стандарта за текущий год
        standard_yield = self._get_standard_yield(standard_sort, region, current_year, 
                                                   maturity_group_code, predecessor_key)
        
        if not standard_yield:
            return {}
        
        # Вычислить отклонение
        deviation = current_year_yield - standard_yield
        deviation_percent = (deviation / standard_yield) * 100
        
        return {
            'deviation_from_standard': round(deviation, 1),
            'deviation_percent': round(deviation_percent, 1),
            'standard_name': standard_sort.name,
            'standard_current_year_yield': standard_yield
        }
    
    def _get_standard_yield(self, standard_sort, region, year, maturity_group_code, predecessor_key):
        """
        Получить урожайность стандарта для конкретного года
        
        Args:
            standard_sort: Сорт-стандарт
            region: Регион
            year: Год
            maturity_group_code: Код группы спелости
            predecessor_key: Ключ предшественника
            
        Returns:
            Урожайность стандарта или None
        """
        yield_indicator = Indicator.objects.filter(code='yield').first()
        
        # Найти участников стандарта
        participants = TrialParticipant.objects.filter(
            sort_record=standard_sort,
            trial__region=region,
            trial__year=year,
            maturity_group_code=maturity_group_code,
            statistical_group=0,
            is_deleted=False
        ).select_related('trial', 'trial__predecessor_culture')
        
        # Фильтруем по predecessor_key
        trial_ids = []
        for p in participants:
            if self._get_predecessor_key(p.trial) == predecessor_key:
                trial_ids.append(p.trial_id)
        
        if not trial_ids:
            return None
        
        # Получить результаты урожайности
        results = TrialResult.objects.filter(
            trial_id__in=trial_ids,
            participant__sort_record=standard_sort,
            indicator=yield_indicator,
            is_deleted=False
        )
        
        if results.exists():
            avg_yield = results.aggregate(avg=Avg('value'))['avg']
            if avg_yield:
                return round(float(avg_yield), 1)
        
        return None
