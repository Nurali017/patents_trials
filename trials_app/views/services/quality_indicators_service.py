"""
Сервис для получения показателей качества и основных показателей
"""
from ...models import TrialLaboratoryResult, TrialResult, TrialParticipant, Indicator


class QualityIndicatorsService:
    """
    Сервис для работы с показателями качества и основными показателями

    Предоставляет методы:
    - Получение показателей качества (из TrialLaboratoryResult)
    - Получение основных показателей (из TrialResult)
    - Список всех доступных показателей качества
    """

    @staticmethod
    def get_all_quality_indicators():
        """
        Получить список всех показателей качества из базы данных

        Returns:
            dict: Словарь показателей {code: {name, unit, description}}
        """
        quality_indicators = Indicator.objects.filter(is_quality=True).order_by('sort_order', 'name')

        indicators_dict = {}
        for indicator in quality_indicators:
            indicators_dict[indicator.code] = {
                'name': indicator.name,
                'unit': indicator.unit,
                'description': indicator.description
            }

        return indicators_dict

    @staticmethod
    def get_quality_indicators(sort_item, years_range):
        """
        Получить показатели качества для конкретного сорта из TrialLaboratoryResult

        Собирает данные за все годы из диапазона (как урожайность)

        Args:
            sort_item: Данные сорта с region_id и sort_record_id
            years_range: Список годов для сбора данных

        Returns:
            dict: {indicator_code: {name, unit, years: {2023: value, 2024: value}}}
        """
        sort_record_id = sort_item['sort_record']['id']
        region_id = sort_item['region']['id']

        # Если нет region_id, пропускаем
        if not region_id:
            return {}

        # Словарь для хранения данных по годам
        indicators_by_year = {}

        # Собираем лабораторные данные за все годы
        for y in years_range:
            participants = TrialParticipant.objects.filter(
                sort_record_id=sort_record_id,
                trial__region_id=region_id,
                trial__year=y,
                is_deleted=False
            ).values_list('trial_id', flat=True)

            if not participants:
                continue

            # Получаем лабораторные результаты для найденных trials
            lab_results = TrialLaboratoryResult.objects.filter(
                trial_id__in=participants,
                participant__sort_record_id=sort_record_id
            ).select_related('indicator')

            for result in lab_results:
                # Только показатели с реальными значениями
                if result.value is not None:
                    indicator_code = result.indicator.code

                    # Инициализируем структуру для этого показателя
                    if indicator_code not in indicators_by_year:
                        indicators_by_year[indicator_code] = {
                            'name': result.indicator.name,
                            'unit': result.indicator.unit,
                            'years': {}
                        }

                    # Добавляем значение за этот год
                    indicators_by_year[indicator_code]['years'][y] = result.value

        return indicators_by_year

    @staticmethod
    def get_main_indicators(sort_item, years_range):
        """
        Получить основные показатели для конкретного сорта из TrialResult

        Собирает данные за все годы из диапазона
        Исключает показатели качества (is_quality=True) и урожайность (yield)

        Args:
            sort_item: Данные сорта с region_id и sort_record_id
            years_range: Список годов для сбора данных

        Returns:
            dict: {indicator_code: {name, unit, description, years: {2023: value}}}
        """
        sort_record_id = sort_item['sort_record']['id']
        region_id = sort_item['region']['id']

        # Если нет region_id, пропускаем
        if not region_id:
            return {}

        # Словарь для хранения данных по годам
        indicators_by_year = {}

        # Собираем основные показатели за все годы
        for y in years_range:
            participants = TrialParticipant.objects.filter(
                sort_record_id=sort_record_id,
                trial__region_id=region_id,
                trial__year=y,
                is_deleted=False
            ).values_list('trial_id', flat=True)

            if not participants:
                continue

            # Получаем основные результаты для найденных trials
            # Исключаем показатели качества (is_quality=True) и урожайность (yield)
            main_results = TrialResult.objects.filter(
                trial_id__in=participants,
                participant__sort_record_id=sort_record_id,
                indicator__is_quality=False,  # Только основные показатели
                indicator__code__in=[
                    'plant_height',
                    'vegetation_period',
                    'thousand_seed_weight',
                    'emergence_completeness',
                    'lodging_resistance',
                    'drought_resistance',
                    'germination_resistance',
                    'tillering',
                    'grain_output',
                    'shedding_resistance'
                ],
                is_deleted=False
            ).select_related('indicator')

            for result in main_results:
                # Только показатели с реальными значениями
                if result.value is not None:
                    indicator_code = result.indicator.code

                    # Инициализируем структуру для этого показателя
                    if indicator_code not in indicators_by_year:
                        indicators_by_year[indicator_code] = {
                            'name': result.indicator.name,
                            'unit': result.indicator.unit,
                            'description': result.indicator.description,
                            'years': {}
                        }

                    # Добавляем значение за этот год
                    indicators_by_year[indicator_code]['years'][y] = result.value

        return indicators_by_year
