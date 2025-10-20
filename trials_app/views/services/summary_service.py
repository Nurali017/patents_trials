"""
Сервис для сводных данных годового отчета
"""
from ...models import Region
from ...statistics import NSRCalculator
from ...evaluation import BallScorer


class SummaryService:
    """
    Сервис для генерации сводных данных годового отчета
    
    Включает:
    - Сводные данные по сортам (summary_items)
    - Агрегированную статистику по покрытию ГСУ
    - Рекомендации по зонам
    - Автоматические рекомендации решений
    - Статистические расчеты (НСР₀.₉₅)
    - Балльную систему оценки
    """
    
    def __init__(self):
        self.nsr_calculator = NSRCalculator()
        self.ball_scorer = BallScorer()
    
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
            
            # Подготовка данных для новой логики
            sort_data = {
                'application_id': app_id,
                'sort_record': data['sort_record'],
                'regions_data': regions_data,
                'summary': {
                    'gsu_tested': tested_regions,
                    'gsu_total': total_regions,
                    'coverage_percent': coverage_percent,
                    'oblast_avg_yield': oblast_avg_yield,
                    'min_years_tested': min_years_tested
                }
            }
            
            # Статистический анализ
            statistical_analysis = self._calculate_statistical_analysis(regions_data)
            
            # Балльная оценка
            evaluation_scores = self.ball_scorer.calculate_overall_score(sort_data)
            
            # Новая логика рекомендаций
            recommendation = self._make_recommendation_new(
                sort_data, statistical_analysis, evaluation_scores
            )
            
            summary_items.append({
                'application_id': app_id,
                'application_number': data['application_number'],
                'sort_record': data['sort_record'],
                'maturity_group_code': data['maturity_group_code'],
                'maturity_group_name': data['maturity_group_name'],
                'standard_for_group': data['standard_for_group'],
                
                # Статистический анализ
                'statistical_analysis': statistical_analysis,
                
                # Балльная оценка
                'evaluation_scores': evaluation_scores,
                
                # Обновленная сводка
                'summary': {
                    'gsu_tested': tested_regions,
                    'gsu_total': total_regions,
                    'coverage_percent': round(coverage_percent, 1),
                    'oblast_avg_yield': round(oblast_avg_yield, 1) if oblast_avg_yield else None,
                    'min_years_tested': min_years_tested,
                    'total_regions_with_data': len(regions_data),
                    'statistically_significant_regions': statistical_analysis.get('significant_regions', 0),
                    'significant_regions_percent': statistical_analysis.get('significant_percent', 0),
                    'quality_indicators': evaluation_scores.get('detailed_scores', {}).get('quality', {}).get('indicators', {}),
                    'resistance_indicators': evaluation_scores.get('detailed_scores', {}).get('resistance', {}).get('indicators', {})
                },
                
                'regions_data': regions_data,
                'zones_recommended': self._get_climate_zones_from_regions(positive_regions),
                'zones_not_recommended': self._get_climate_zones_from_regions([rd for rd in regions_data if rd not in positive_regions]),
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
    
    def _calculate_statistical_analysis(self, regions_data):
        """
        Расчет статистического анализа по регионам
        
        Args:
            regions_data: Данные по регионам
            
        Returns:
            Статистический анализ
        """
        if not regions_data:
            return {
                'nsr_095': None,
                'statistical_significance': False,
                'confidence_level': 0.95,
                'degrees_of_freedom': 0,
                'error_variance': None,
                'repetitions_count': 0,
                'sufficient_data': False,
                'significant_regions': 0,
                'significant_percent': 0
            }
        
        # Расчет НСР для каждого региона
        region_nsr_data = []
        significant_regions = 0
        
        for region in regions_data:
            # Получаем данные урожайности для расчета НСР
            yields_data = list(region.get('yields_by_year', {}).values())
            
            if len(yields_data) >= 2:  # Минимум 2 года для расчета
                nsr_result = self.nsr_calculator.calculate_nsr(yields_data)
                
                # Проверяем статистическую значимость
                deviation = region.get('deviation_from_standard', 0)
                is_significant = self.nsr_calculator.is_significant(
                    deviation, nsr_result.get('nsr_value')
                )
                
                if is_significant:
                    significant_regions += 1
                
                region_nsr_data.append({
                    'region_id': region.get('region_id'),
                    'region_name': region.get('region_name'),
                    'nsr_value': nsr_result.get('nsr_value'),
                    'statistical_significance': is_significant,
                    'deviation_from_standard': deviation,
                    'confidence_interval': self.nsr_calculator.calculate_confidence_interval(
                        region.get('average_yield', 0), nsr_result.get('nsr_value')
                    )
                })
        
        # Объединенный НСР
        combined_nsr = self.nsr_calculator.calculate_combined_nsr(region_nsr_data)
        
        return {
            'nsr_095': combined_nsr.get('combined_nsr'),
            'statistical_significance': combined_nsr.get('significant_regions', 0) > 0,
            'confidence_level': 0.95,
            'degrees_of_freedom': sum(rd.get('degrees_of_freedom', 0) for rd in region_nsr_data),
            'error_variance': sum(rd.get('error_variance', 0) for rd in region_nsr_data) / len(region_nsr_data) if region_nsr_data else None,
            'repetitions_count': sum(rd.get('repetitions', 0) for rd in region_nsr_data),
            'sufficient_data': combined_nsr.get('sufficient_data', False),
            'significant_regions': combined_nsr.get('significant_regions', 0),
            'significant_percent': combined_nsr.get('significant_percent', 0),
            'regions_analysis': region_nsr_data
        }
    
    def _make_recommendation_new(self, sort_data, statistical_analysis, evaluation_scores):
        """
        Новая логика рекомендаций по Методике ГСИ
        
        Args:
            sort_data: Данные о сорте
            statistical_analysis: Статистический анализ
            evaluation_scores: Балльная оценка
            
        Returns:
            Рекомендация с обоснованием
        """
        # Получаем критерии решения
        decision_criteria = self.ball_scorer.get_decision_criteria(evaluation_scores)
        
        # Проверяем покрытие ГСУ
        coverage_percent = sort_data['summary']['coverage_percent']
        min_years_tested = sort_data['summary']['min_years_tested']
        
        # Извлекаем баллы
        overall_score = evaluation_scores.get('overall_score', 3.0)
        yield_score = evaluation_scores.get('yield_score')
        quality_score = evaluation_scores.get('quality_score')
        resistance_score = evaluation_scores.get('resistance_score')
        
        # Проверяем только доступные критерии (не учитываем отсутствующие данные)
        available_criteria = []
        if yield_score is not None:
            available_criteria.append(('yield', yield_score >= 4))
        if quality_score is not None:
            available_criteria.append(('quality', quality_score >= 3))
        if resistance_score is not None:
            available_criteria.append(('resistance', resistance_score >= 3))
        
        # Критерии одобрения (только если есть достаточно данных)
        can_approve = (
            coverage_percent >= 50 and 
            min_years_tested >= 2 and
            statistical_analysis.get('statistical_significance', False) and
            overall_score >= 4.0 and
            yield_score is not None and yield_score >= 4 and
            (quality_score is None or quality_score >= 3) and
            (resistance_score is None or resistance_score >= 3)
        )
        
        if can_approve:
            return {
                'decision': 'approved',
                'reason': f'Балльная оценка: {overall_score}/5. Статистически значимое преимущество. Покрытие ГСУ: {coverage_percent}%.',
                'confidence': 'high',
                'can_approve': True,
                'justification': {
                    'statistical_criteria': {
                        'met': True,
                        'description': self._get_statistical_description(statistical_analysis, min_years_tested)
                    },
                    'quality_criteria': {
                        'met': quality_score is None or quality_score >= 3,
                        'description': f'Качество: {quality_score}/5' if quality_score is not None else 'Качество: данные отсутствуют'
                    },
                    'resistance_criteria': {
                        'met': resistance_score is None or resistance_score >= 3,
                        'description': f'Устойчивость: {resistance_score}/5' if resistance_score is not None else 'Устойчивость: данные отсутствуют'
                    },
                    'coverage_criteria': {
                        'met': coverage_percent >= 50,
                        'description': f'Покрытие ГСУ: {coverage_percent}%'
                    }
                },
                'improvement_recommendations': []
            }
        
        # Критерии отклонения (только при явно плохих показателях)
        should_reject = (
            overall_score <= 2.0 or
            (yield_score is not None and yield_score <= 2) or
            (quality_score is not None and quality_score <= 2) or
            (resistance_score is not None and resistance_score <= 2) or
            coverage_percent < 20  # Минимальный порог для продолжения
        )
        
        if should_reject:
            reasons = []
            if coverage_percent < 20:
                reasons.append(f'Недостаточное покрытие ГСУ ({coverage_percent}%)')
            if min_years_tested < 1:
                reasons.append(f'Недостаточно лет испытаний ({min_years_tested})')
            if overall_score <= 2.0:
                reasons.append(f'Низкий общий балл ({overall_score}/5)')
            if yield_score is not None and yield_score <= 2:
                reasons.append(f'Низкий балл по урожайности ({yield_score}/5)')
            if quality_score is not None and quality_score <= 2:
                reasons.append(f'Низкий балл по качеству ({quality_score}/5)')
            if resistance_score is not None and resistance_score <= 2:
                reasons.append(f'Низкий балл по устойчивости ({resistance_score}/5)')
            
            return {
                'decision': 'rejected',
                'reason': f'Балльная оценка: {overall_score}/5. {"; ".join(reasons)}.',
                'confidence': 'high',
                'can_approve': False,
                'justification': {
                    'statistical_criteria': {
                        'met': statistical_analysis.get('statistical_significance', False),
                        'description': self._get_statistical_description(statistical_analysis, min_years_tested)
                    },
                    'quality_criteria': {
                        'met': quality_score is None or quality_score >= 3,
                        'description': f'Качество: {quality_score}/5' if quality_score is not None else 'Качество: данные отсутствуют'
                    },
                    'resistance_criteria': {
                        'met': resistance_score is None or resistance_score >= 3,
                        'description': f'Устойчивость: {resistance_score}/5' if resistance_score is not None else 'Устойчивость: данные отсутствуют'
                    },
                    'coverage_criteria': {
                        'met': coverage_percent >= 20,
                        'description': f'Покрытие ГСУ: {coverage_percent}%'
                    }
                },
                'improvement_recommendations': [
                    'Продолжить испытания для накопления статистически значимых данных',
                    'Обратить внимание на повышение качества продукции',
                    'Улучшить устойчивость к болезням и стрессам',
                    'Расширить географию испытаний для увеличения покрытия ГСУ'
                ]
            }
        
        # Продолжить испытания (по умолчанию для большинства случаев)
        return {
            'decision': 'continue',
            'reason': f'Балльная оценка: {overall_score}/5. Требуется дополнительное изучение для принятия окончательного решения.',
            'confidence': 'medium',
            'can_approve': False,
                'justification': {
                    'statistical_criteria': {
                        'met': statistical_analysis.get('statistical_significance', False),
                        'description': self._get_statistical_description(statistical_analysis, min_years_tested)
                    },
                'quality_criteria': {
                    'met': quality_score is None or quality_score >= 3,
                    'description': f'Качество: {quality_score}/5' if quality_score is not None else 'Качество: данные отсутствуют'
                },
                'resistance_criteria': {
                    'met': resistance_score is None or resistance_score >= 3,
                    'description': f'Устойчивость: {resistance_score}/5' if resistance_score is not None else 'Устойчивость: данные отсутствуют'
                },
                'coverage_criteria': {
                    'met': coverage_percent >= 20,
                    'description': f'Покрытие ГСУ: {coverage_percent}%'
                }
            },
            'improvement_recommendations': [
                'Продолжить испытания для накопления статистически значимых данных',
                'Обратить внимание на повышение показателей качества',
                'Улучшить устойчивость к болезням и стрессам',
                'Расширить географию испытаний для увеличения покрытия ГСУ'
            ]
        }
    
    def _get_statistical_description(self, statistical_analysis, min_years_tested):
        """
        Создание понятного описания статистического анализа
        
        Args:
            statistical_analysis: Результаты статистического анализа
            min_years_tested: Минимальное количество лет испытаний
            
        Returns:
            Понятное описание статистической ситуации
        """
        significant_regions = statistical_analysis.get('significant_regions', 0)
        regions_count = statistical_analysis.get('regions_count', 0)
        sufficient_data = statistical_analysis.get('sufficient_data', False)
        
        # Если недостаточно данных для анализа
        if not sufficient_data or min_years_tested < 2:
            if min_years_tested == 1:
                return f'Недостаточно данных для статистического анализа (испытания только 1 год, требуется минимум 2 года)'
            elif min_years_tested == 0:
                return f'Данные по испытаниям отсутствуют'
            else:
                return f'Недостаточно данных для статистического анализа (испытания {min_years_tested} года, требуется минимум 2 года)'
        
        # Если есть данные для анализа
        if regions_count == 0:
            return f'Статистический анализ не проводился'
        elif significant_regions == 0:
            return f'Статистически значимых различий не выявлено (0 из {regions_count} ГСУ)'
        elif significant_regions == regions_count:
            return f'Статистически значимые различия выявлены во всех ГСУ ({significant_regions} из {regions_count})'
        else:
            return f'Статистически значимые различия выявлены в {significant_regions} из {regions_count} ГСУ'
    
    def _get_climate_zones_from_regions(self, regions_data):
        """
        Получить уникальные климатические зоны из данных регионов
        
        Args:
            regions_data: Список данных регионов
            
        Returns:
            Список названий климатических зон
        """
        climate_zones = set()
        
        for region in regions_data:
            # Получаем климатическую зону из данных региона
            region_info = region.get('region', {})
            climate_zone = region_info.get('climate_zone')
            
            if climate_zone and climate_zone.get('name'):
                climate_zones.add(climate_zone['name'])
            else:
                # Если климатическая зона не указана, используем название ГСУ
                climate_zones.add(region.get('region_name', 'Неизвестная зона'))
        
        return list(climate_zones)
