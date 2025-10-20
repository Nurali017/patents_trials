"""
Сервис для сводных данных годового отчета
"""
from ...models import Region


class SummaryService:
    """
    Сервис для генерации сводных данных годового отчета
    
    Включает:
    - Сводные данные по сортам (summary_items)
    - Агрегированную статистику по покрытию ГСУ
    - Рекомендации по зонам
    - Автоматические рекомендации решений
    """
    
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
        # Группировать по сортам/заявкам
        sorts_data = {}
        
        for item in detailed_items:
            if item['is_standard']:
                continue  # Стандарты не включаем в сводную
            
            app_id = item['application_id']
            
            if app_id not in sorts_data:
                sorts_data[app_id] = {
                    'application_id': app_id,
                    'application_number': item.get('application_number'),
                    'sort_record': item['sort_record'],
                    'maturity_group_code': item.get('maturity_group_code'),
                    'maturity_group_name': item.get('maturity_group_name'),
                    'standard_for_group': item.get('standard_for_group'),
                    'regions_data': [],
                    'decision_status': item.get('decision_status'),
                    'latest_decision': item.get('latest_decision')
                }
            
            # Добавить данные региона
            if item['trial_data']['has_data']:
                sorts_data[app_id]['regions_data'].append({
                    'region_id': item['region']['id'],
                    'region_name': item['region']['name'],
                    **item['trial_data']
                })
        
        # Агрегировать по сортам
        summary_items = []
        
        for app_id, data in sorts_data.items():
            regions_data = data['regions_data']
            
            if not regions_data:
                continue
            
            # Подсчитать покрытие ГСУ
            total_regions = Region.objects.filter(oblast=oblast, is_deleted=False).count()
            tested_regions = len(regions_data)
            coverage_percent = (tested_regions / total_regions * 100) if total_regions > 0 else 0
            
            # Вычислить среднюю урожайность по области
            all_avg_yields = [rd['average_yield'] for rd in regions_data if rd.get('average_yield')]
            oblast_avg_yield = sum(all_avg_yields) / len(all_avg_yields) if all_avg_yields else None
            
            # Вычислить среднее отклонение от стандарта (%)
            all_deviations = [rd.get('deviation_percent') for rd in regions_data if rd.get('deviation_percent') is not None]
            avg_deviation_percent = sum(all_deviations) / len(all_deviations) if all_deviations else None
            
            # Подсчитать на скольких ГСУ показал преимущество
            positive_regions = [rd for rd in regions_data if rd.get('deviation_percent', 0) > 0]
            advantage_on_majority = len(positive_regions) > len(regions_data) / 2
            advantage_percent = (len(positive_regions) / len(regions_data) * 100) if regions_data else 0
            
            # Минимальное количество лет испытаний
            min_years_tested = min([rd['years_tested'] for rd in regions_data]) if regions_data else 0
            
            # Автоматическая рекомендация
            recommendation = self._make_recommendation(
                tested_regions=tested_regions,
                total_regions=total_regions,
                avg_deviation_percent=avg_deviation_percent,
                advantage_on_majority=advantage_on_majority,
                advantage_percent=advantage_percent,
                min_years_tested=min_years_tested,
                positive_regions_count=len(positive_regions),
                total_regions_with_data=len(regions_data)
            )
            
            summary_items.append({
                'application_id': app_id,
                'application_number': data['application_number'],
                'sort_record': data['sort_record'],
                'maturity_group_code': data['maturity_group_code'],
                'maturity_group_name': data['maturity_group_name'],
                'standard_for_group': data['standard_for_group'],
                'summary': {
                    'gsu_tested': tested_regions,
                    'gsu_total': total_regions,
                    'coverage_percent': round(coverage_percent, 1),
                    'oblast_avg_yield': round(oblast_avg_yield, 1) if oblast_avg_yield else None,
                    'avg_deviation_percent': round(avg_deviation_percent, 1) if avg_deviation_percent else None,
                    'advantage_on_majority': advantage_on_majority,
                    'advantage_percent': round(advantage_percent, 1),
                    'min_years_tested': min_years_tested,
                    'positive_regions': len(positive_regions),
                    'total_regions_with_data': len(regions_data)
                },
                'regions_data': regions_data,
                'zones_recommended': [rd['region_name'] for rd in positive_regions],
                'zones_not_recommended': [rd['region_name'] for rd in regions_data if rd not in positive_regions],
                'decision_status': data['decision_status'],
                'latest_decision': data['latest_decision'],
                'recommendation': recommendation
            })
        
        return summary_items
    
    def _make_recommendation(self, tested_regions, total_regions, avg_deviation_percent, 
                            advantage_on_majority, advantage_percent, min_years_tested,
                            positive_regions_count, total_regions_with_data):
        """Автоматическая рекомендация решения по Методике"""
        
        # Проверка 1: Покрытие ГСУ (большинство)
        if tested_regions < total_regions / 2:
            return {
                'decision': 'rejected',
                'reason': f'Испытан только в {tested_regions}/{total_regions} ГСУ (нужно большинство)',
                'confidence': 'high',
                'can_approve': False
            }
        
        # Проверка 2: Минимум лет испытаний
        if min_years_tested < 2:
            # Исключение: значительно выделившиеся сорта (>15%)
            if avg_deviation_percent and avg_deviation_percent > 15:
                pass  # Можно рассмотреть
            else:
                return {
                    'decision': 'continue',
                    'reason': f'Недостаточно лет испытаний (минимум 2 года, сейчас {min_years_tested})',
                    'confidence': 'high',
                    'can_approve': False
                }
        
        # Проверка 3: Преимущество на большинстве ГСУ
        if not advantage_on_majority:
            return {
                'decision': 'rejected',
                'reason': f'Преимущество только в {positive_regions_count}/{total_regions_with_data} ГСУ ({advantage_percent:.0f}%) - нужно большинство',
                'confidence': 'high',
                'can_approve': False
            }
        
        # Проверка 4: Среднее отклонение
        if avg_deviation_percent is None:
            return {
                'decision': 'continue',
                'reason': 'Недостаточно данных для принятия решения',
                'confidence': 'medium',
                'can_approve': False
            }
        
        if avg_deviation_percent > 5:
            return {
                'decision': 'approved',
                'reason': f'Превышает стандарт на {avg_deviation_percent:.1f}% в среднем. Преимущество на {advantage_percent:.0f}% ГСУ.',
                'confidence': 'high',
                'can_approve': True
            }
        elif avg_deviation_percent > 0:
            return {
                'decision': 'continue',
                'reason': f'Отклонение {avg_deviation_percent:.1f}% недостаточно для допуска (рекомендуется >5%)',
                'confidence': 'medium',
                'can_approve': False
            }
        else:
            return {
                'decision': 'rejected',
                'reason': f'Урожайность ниже стандарта на {abs(avg_deviation_percent):.1f}%',
                'confidence': 'high',
                'can_approve': False
            }
