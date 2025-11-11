"""
Сервис для генерации таблицы по методике сортоиспытаний
"""
from collections import defaultdict
from django.db.models import Avg
from django.utils import timezone

from ...models import Region, TrialParticipant, TrialResult, Indicator, Culture
from .basic_report_service import BasicReportService
from .quality_indicators_service import QualityIndicatorsService
from .culture_filter_service import CultureFilterService


class MethodologyTableService:
    """
    Сервис для генерации таблицы по методике сортоиспытаний

    Генерирует:
    - Таблицу с группировкой по регионам, группам спелости и предшественникам
    - Показатели урожайности с пересчетом
    - Основные и качественные показатели
    - Стандарты по группам

    НЕ включает: decision_status, latest_decision (это в summary)
    """

    def __init__(self):
        self.basic_service = BasicReportService()
        self.quality_service = QualityIndicatorsService()

    def generate_table(self, oblast, year, patents_culture_id=None):
        """
        Генерация таблицы по методике сортоиспытаний

        Args:
            oblast: Объект области
            year: Год отчета
            patents_culture_id: ID культуры из Patents для фильтрации (опционально)

        Returns:
            dict: Полная таблица с metadata, methodology_table, standards_by_group
        """
        # Получаем базовые данные
        basic_data = self.basic_service.generate_basic_report(oblast, year)
        years_range = basic_data['years_range']

        # Фильтрация по культуре (если указан patents_culture_id)
        filtered_items = CultureFilterService.filter_items(
            basic_data['detailed_items'],
            patents_culture_id
        )

        # Группируем данные: регион -> группа спелости -> predecessor -> сорта
        regions_groups = self._group_by_regions_and_groups(filtered_items)

        # Пересчитываем trial_data для каждой комбинации (сорт + predecessor)
        self._recalculate_trial_data(regions_groups, years_range, year)

        # Формируем standards_by_group
        standards_by_group = self._build_standards_by_group(filtered_items)

        # Формируем структуру таблицы
        methodology_table = self._build_table_structure(
            regions_groups,
            years_range,
            year
        )

        # Получить информацию о фильтре культуры
        culture_filter_info = CultureFilterService.get_culture_info(patents_culture_id)

        return {
            'oblast': basic_data['oblast'],
            'year': basic_data['year'],
            'years_range': years_range,
            'generated_at': timezone.now(),
            'regions': basic_data['regions'],
            'methodology_table': methodology_table,
            'standards_by_group': standards_by_group,
            'quality_indicators': self.quality_service.get_all_quality_indicators(),
            'warnings': basic_data['warnings'],
            'has_warnings': basic_data['has_warnings'],
            'culture_filter': culture_filter_info
        }

    def _group_by_regions_and_groups(self, detailed_items):
        """
        Группировка данных по регионам, группам спелости и предшественникам

        Args:
            detailed_items: Список детальных элементов

        Returns:
            defaultdict: Структура regions_groups[region][group][predecessor][sort_id]
        """
        regions_groups = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

        for item in detailed_items:
            if item.get('region', {}).get('id'):
                region_name = item['region']['name']
                group_code = item['maturity_group_code']
                sort_id = item['sort_record']['id']
                predecessor_key = item.get('predecessor_key', 'unknown')

                # Группируем: region -> group -> predecessor -> sort
                if sort_id not in regions_groups[region_name][group_code][predecessor_key]:
                    regions_groups[region_name][group_code][predecessor_key][sort_id] = item

        return regions_groups

    def _recalculate_trial_data(self, regions_groups, years_range, current_year):
        """
        Пересчет trial_data для каждой комбинации сорта и предшественника

        Args:
            regions_groups: Структура с группированными данными
            years_range: Диапазон лет
            current_year: Текущий год отчета
        """
        yield_indicator = Indicator.objects.filter(code='yield').first()

        for region_name, groups in regions_groups.items():
            # Найти region object
            try:
                region_obj = Region.objects.get(name=region_name, is_deleted=False)
            except Region.DoesNotExist:
                continue

            for group_code, predecessors_dict in groups.items():
                for predecessor_key, sorts_dict in predecessors_dict.items():
                    # Получаем predecessor_name для этой группы
                    predecessor_name = "Неизвестно"

                    for sort_id, item in sorts_dict.items():
                        # Пересчитываем trial_data напрямую из БД с фильтрацией по predecessor
                        yields_by_year = {}

                        for y in years_range:
                            # Найти всех участников для этого сорта
                            participants = TrialParticipant.objects.filter(
                                sort_record_id=sort_id,
                                trial__region=region_obj,
                                trial__year=y,
                                maturity_group_code=group_code,
                                is_deleted=False
                            ).select_related('trial', 'trial__predecessor_culture')

                            # Фильтруем по predecessor_key
                            trial_ids = []
                            for participant in participants:
                                if self._get_predecessor_key_from_trial(participant.trial) == predecessor_key:
                                    trial_ids.append(participant.trial_id)
                                    # Получаем predecessor_name из первого найденного trial
                                    if predecessor_name == "Неизвестно":
                                        predecessor_name = self._get_predecessor_name_from_trial(participant.trial)

                            if trial_ids:
                                # Получить результаты урожайности для отфильтрованных trials
                                results = TrialResult.objects.filter(
                                    trial_id__in=trial_ids,
                                    participant__sort_record_id=sort_id,
                                    indicator=yield_indicator,
                                    is_deleted=False
                                )

                                if results.exists():
                                    avg_yield = results.aggregate(avg=Avg('value'))['avg']
                                    if avg_yield:
                                        yields_by_year[y] = round(float(avg_yield), 1)

                        # Пересчитываем агрегированные данные
                        average_yield = None
                        if yields_by_year:
                            average_yield = round(sum(yields_by_year.values()) / len(yields_by_year), 1)

                        current_year_yield = yields_by_year.get(current_year) if yields_by_year else None

                        # Обновляем trial_data
                        item['trial_data']['yields_by_year'] = yields_by_year
                        item['trial_data']['average_yield'] = average_yield
                        item['trial_data']['years_tested'] = len(yields_by_year)
                        item['trial_data']['year_started'] = min(yields_by_year.keys()) if yields_by_year else None
                        item['trial_data']['current_year_yield'] = current_year_yield

                        # Сохраняем predecessor_name в item
                        item['predecessor_name'] = predecessor_name

    def _build_standards_by_group(self, detailed_items):
        """
        Построение словаря стандартов по группам спелости

        Args:
            detailed_items: Список детальных элементов

        Returns:
            dict: {group_code: [{sort_name, average_yield, is_comparison_standard, region}]}
        """
        standards_by_group = defaultdict(list)

        for item in detailed_items:
            if item['is_standard']:
                group_code = item['maturity_group_code']
                standards_by_group[group_code].append({
                    'sort_name': item['sort_record']['name'],
                    'average_yield': item['trial_data']['average_yield'],
                    'is_comparison_standard': item['is_comparison_standard'],
                    'region': item['region']['name']
                })

        return dict(standards_by_group)

    def _build_table_structure(self, regions_groups, years_range, current_year):
        """
        Построение структуры таблицы методики

        Args:
            regions_groups: Группированные данные
            years_range: Диапазон лет
            current_year: Текущий год

        Returns:
            dict: Структура таблицы {region: {group: {predecessor: {sorts: [...]}}}}
        """
        methodology_table = {}

        for region_name, groups in regions_groups.items():
            methodology_table[region_name] = {}

            for group_code, predecessors_dict in groups.items():
                methodology_table[region_name][group_code] = {}

                for predecessor_key, sorts_dict in predecessors_dict.items():
                    # Преобразуем dict в list
                    sorts = list(sorts_dict.values())

                    # Формируем данные сортов в подгруппе predecessor
                    predecessor_data = {
                        'group_code': group_code,
                        'group_name': sorts[0]['maturity_group_name'] if sorts else '',
                        'predecessor_key': predecessor_key,
                        'predecessor_name': sorts[0].get('predecessor_name', 'Неизвестно') if sorts else 'Неизвестно',
                        'sorts': []
                    }

                    # Добавляем сорта в подгруппу
                    for sort_item in sorts:
                        # Добавляем год и years_range для получения показателей
                        sort_item_with_year = sort_item.copy()
                        sort_item_with_year['year'] = current_year
                        sort_item_with_year['years_range'] = years_range

                        # Определяем is_standard
                        is_sort_standard = sort_item.get('is_standard', False)

                        # Для стандартов deviation_percent и deviation_from_standard должны быть пустой строкой
                        deviation_percent = sort_item['trial_data'].get('deviation_percent')
                        deviation_from_standard = sort_item['trial_data'].get('deviation_from_standard')
                        if is_sort_standard:
                            deviation_percent = ""
                            deviation_from_standard = ""
                        elif deviation_percent is None:
                            deviation_percent = None
                            deviation_from_standard = None

                        sort_data = {
                            'sort_name': sort_item['sort_record']['name'],
                            'application_number': sort_item['application_number'],
                            'is_standard': is_sort_standard,
                            'is_comparison_standard': sort_item.get('is_comparison_standard', False),
                            'yields_by_year': sort_item['trial_data']['yields_by_year'],
                            'average_yield': sort_item['trial_data']['average_yield'],
                            'deviation_from_standard': deviation_from_standard,
                            'deviation_percent': deviation_percent,
                            'years_tested': sort_item['trial_data']['years_tested'],
                            'year_started': sort_item['trial_data']['year_started'],
                            'main_indicators': self.quality_service.get_main_indicators(sort_item_with_year, years_range),
                            'quality_indicators': self.quality_service.get_quality_indicators(sort_item_with_year, years_range)
                            # НЕ ВКЛЮЧАЕМ: decision_status, latest_decision
                        }
                        predecessor_data['sorts'].append(sort_data)

                    methodology_table[region_name][group_code][predecessor_key] = predecessor_data

        return methodology_table

    def _get_predecessor_key_from_trial(self, trial):
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

    def _get_predecessor_name_from_trial(self, trial):
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
