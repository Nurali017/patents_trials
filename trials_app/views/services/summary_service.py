"""
Сервис для сводных данных годового отчета
"""
from ...models import Region, GroupCulture, Culture
from ...evaluation import BallScorer, AlertService, CommissionRecommendationService


class SummaryService:
    """
    Сервис для генерации сводных данных годового отчета

    Включает:
    - Сводные данные по сортам (summary_items)
    - Агрегированную статистику по покрытию ГСУ
    - Балльную систему оценки (три независимых балла 1-5)
    - Генерацию нарушений (violations) вместо автоматических решений
    """

    def __init__(self):
        self.ball_scorer = BallScorer()
        self.alert_service = AlertService()
        self.commission_service = CommissionRecommendationService()

    def generate_summary_items(self, oblast, year, detailed_items):
        """
        Сгенерировать сводную таблицу для принятия решений

        Args:
            oblast: объект области
            year: год отчета
            detailed_items: детальные данные

        Returns:
            list: сводные данные по сортам
        """
        # НОВАЯ СТРУКТУРА: Группировать БЕЗ predecessor_key в ключе
        sorts_data = {}

        for item in detailed_items:
            app_id = item.get('application_id')
            maturity_group_code = item.get('maturity_group_code')
            predecessor_key = item.get('predecessor_key')
            predecessor = item.get('predecessor')

            if not app_id:
                # Если нет application_id - пропускаем (включая стандарты без заявки)
                continue

            # ИЗМЕНЕНИЕ №1: Новый composite_key БЕЗ predecessor_key
            composite_key = (app_id, maturity_group_code)

            if composite_key not in sorts_data:
                sorts_data[composite_key] = {
                    'application_id': app_id,
                    'application_number': item.get('application_number'),
                    'sort_record': item['sort_record'],
                    'maturity_group_code': maturity_group_code,
                    'maturity_group_name': item.get('maturity_group_name'),
                    'standard_for_group': item.get('standard_for_group'),
                    'decision_status': item.get('decision_status'),
                    'latest_decision': item.get('latest_decision'),
                    # ИЗМЕНЕНИЕ №2: Вложенная структура по предшественникам
                    'trials_by_predecessor': {}
                }

            # Создать запись для этого предшественника, если её еще нет
            if predecessor_key not in sorts_data[composite_key]['trials_by_predecessor']:
                sorts_data[composite_key]['trials_by_predecessor'][predecessor_key] = {
                    'predecessor': predecessor,
                    'predecessor_key': predecessor_key,
                    'regions_data': []
                }

            # Добавить данные региона к соответствующему предшественнику
            if item['trial_data']['has_data']:
                sorts_data[composite_key]['trials_by_predecessor'][predecessor_key]['regions_data'].append({
                    'region_id': item['region']['id'],
                    'region_name': item['region']['name'],
                    'region': item['region'],  # Полные данные региона с climate_zone
                    **item['trial_data'],
                    'quality_indicators': item.get('quality_indicators', {}),
                    'resistance_indicators': item.get('resistance_indicators', {})
                })

        # Агрегировать по сортам
        summary_items = []

        for composite_key, data in sorts_data.items():
            # Получаем total_regions для конкретной группы культуры
            # Путь: sort_record -> culture -> group_culture -> regions
            sort_record = data.get('sort_record')

            # По умолчанию - все регионы области
            total_regions = Region.objects.filter(oblast=oblast, is_deleted=False).count()

            # Получаем группу культуры через сорт
            if sort_record:
                # sort_record может быть объектом модели или словарем из сериализатора
                if hasattr(sort_record, 'culture'):
                    # Это объект модели
                    culture = sort_record.culture
                elif isinstance(sort_record, dict) and 'culture' in sort_record:
                    # Это словарь, получаем culture_id
                    culture_data = sort_record['culture']
                    culture_id = culture_data.get('id') if isinstance(culture_data, dict) else culture_data

                    try:
                        culture = Culture.objects.select_related('group_culture').get(
                            id=culture_id,
                            is_deleted=False
                        )
                    except (Culture.DoesNotExist, TypeError):
                        culture = None
                else:
                    culture = None

                # Получаем регионы из группы культуры
                if culture and culture.group_culture:
                    group_regions_count = culture.group_culture.regions.filter(
                        oblast=oblast,
                        is_deleted=False
                    ).count()

                    if group_regions_count > 0:
                        total_regions = group_regions_count

            # ИЗМЕНЕНИЕ №3: Рассчитать overall_summary по всем предшественникам
            overall_summary = self._calculate_overall_summary(data['trials_by_predecessor'], total_regions)

            if overall_summary['gsu_tested_total'] == 0:
                # Нет данных вообще
                continue

            # Подготовка данных для балльной оценки (используем все регионы со всех предшественников)
            all_regions_data = []
            for pred_key, pred_data in data['trials_by_predecessor'].items():
                # Добавляем predecessor к каждому региону
                for region in pred_data['regions_data']:
                    region_with_predecessor = region.copy()
                    region_with_predecessor['predecessor'] = pred_data['predecessor']
                    region_with_predecessor['predecessor_key'] = pred_key
                    all_regions_data.append(region_with_predecessor)

            sort_data = {
                'application_id': data['application_id'],
                'sort_record': data['sort_record'],
                'regions_data': all_regions_data,
                'overall_summary': overall_summary
            }

            # Балльная оценка (три независимых балла 1-5, без overall_score)
            evaluation_scores = self.ball_scorer.calculate_scores(sort_data)

            # Подготовка полной сводки для проверки нарушений
            full_summary = {
                **overall_summary,
                'gsu_total': total_regions
            }

            # Генерация нарушений вместо автоматических рекомендаций
            violations = self.alert_service.generate_violations(
                evaluation_scores, full_summary, data['sort_record']
            )

            # Генерация решения комиссии с обоснованием
            commission_recommendation = self.commission_service.generate_recommendation(
                evaluation_scores=evaluation_scores,
                violations=violations,
                overall_summary=full_summary,
                sort_record=data['sort_record']
            )

            summary_items.append({
                'application_id': data['application_id'],
                'application_number': data['application_number'],
                'sort_record': data['sort_record'],
                'maturity_group_code': data['maturity_group_code'],
                'maturity_group_name': data['maturity_group_name'],
                'standard_for_group': data['standard_for_group'],

                # Балльная оценка
                'evaluation_scores': evaluation_scores,

                # Общая сводка
                'overall_summary': {
                    'gsu_tested_total': overall_summary['gsu_tested_total'],
                    'gsu_total': total_regions,
                    'overall_coverage_percent': round(overall_summary['overall_coverage_percent'], 1),
                    'overall_avg_yield': round(overall_summary['overall_avg_yield'], 1) if overall_summary['overall_avg_yield'] else None,
                    'overall_min_years_tested': overall_summary['overall_min_years_tested'],
                    'quality_indicators': evaluation_scores.get('detailed_scores', {}).get('quality', {}).get('indicators', {}),
                    'resistance_indicators': evaluation_scores.get('detailed_scores', {}).get('resistance', {}).get('indicators', {})
                },

                # Детализация по предшественникам
                'trials_by_predecessor': self._format_trials_by_predecessor(data['trials_by_predecessor']),

                # Нарушения (заменяет recommendation)
                'violations': violations,

                # Решение комиссии с обоснованием
                'commission_recommendation': commission_recommendation,

                'decision_status': data['decision_status'],
                'latest_decision': data['latest_decision']
            })

        return summary_items

    def _calculate_overall_summary(self, trials_by_predecessor, total_regions):
        """
        Рассчитать общую сводку по всем предшественникам

        Args:
            trials_by_predecessor: Словарь {predecessor_key: {'regions_data': [...]}}
            total_regions: Общее количество ГСУ в области

        Returns:
            dict: overall_summary с агрегированными метриками
        """
        # Собираем все уникальные region_id
        unique_region_ids = set()
        # ИСПРАВЛЕНО: Для каждого региона берем МАКСИМУМ years_tested
        # (учитывая все предшественники)
        years_by_region = {}  # region_id -> max years_tested
        all_avg_yields = []

        for pred_key, pred_data in trials_by_predecessor.items():
            for region in pred_data['regions_data']:
                region_id = region.get('region_id')

                if region_id:
                    unique_region_ids.add(region_id)

                    # Для каждого региона берем максимум years_tested
                    years = region.get('years_tested', 0)
                    if years > 0:
                        if region_id not in years_by_region:
                            years_by_region[region_id] = years
                        else:
                            years_by_region[region_id] = max(years_by_region[region_id], years)

                # Собираем урожайность
                avg_yield = region.get('average_yield')
                if avg_yield:
                    all_avg_yields.append(avg_yield)

        # Берем минимум из максимальных years_tested по регионам
        all_years_tested = list(years_by_region.values())

        gsu_tested_total = len(unique_region_ids)
        overall_coverage_percent = (gsu_tested_total / total_regions * 100) if total_regions > 0 else 0
        # ИСПРАВЛЕНО: Для каждого региона берется max years_tested (среди предшественников),
        # затем берется min из этих значений (минимальная продолжительность среди регионов)
        overall_min_years_tested = min(all_years_tested) if all_years_tested else 0
        overall_avg_yield = sum(all_avg_yields) / len(all_avg_yields) if all_avg_yields else None

        return {
            'gsu_tested_total': gsu_tested_total,
            'overall_coverage_percent': overall_coverage_percent,
            'overall_min_years_tested': overall_min_years_tested,
            'overall_avg_yield': overall_avg_yield
        }

    def _format_trials_by_predecessor(self, trials_by_predecessor):
        """
        Форматировать данные по предшественникам для JSON ответа

        Args:
            trials_by_predecessor: Словарь с данными по предшественникам

        Returns:
            dict: Отформатированные данные
        """
        formatted = {}

        for pred_key, pred_data in trials_by_predecessor.items():
            regions_data = pred_data['regions_data']

            if not regions_data:
                continue

            # Локальная статистика для этого предшественника
            tested_regions = len(regions_data)
            all_avg_yields = [rd['average_yield'] for rd in regions_data if rd.get('average_yield')]
            local_avg_yield = sum(all_avg_yields) / len(all_avg_yields) if all_avg_yields else None
            min_years = min([rd['years_tested'] for rd in regions_data]) if regions_data else 0

            positive_regions = [rd for rd in regions_data if rd.get('deviation_percent', 0) > 0]

            formatted[pred_key] = {
                'predecessor': pred_data['predecessor'],
                'predecessor_key': pred_key,
                'local_summary': {
                    'gsu_tested': tested_regions,
                    'local_avg_yield': round(local_avg_yield, 1) if local_avg_yield else None,
                    'min_years_tested': min_years,
                    'positive_regions_count': len(positive_regions)
                },
                'regions_data': regions_data
            }

        return formatted

