"""
Балльная система оценки сортов по Методике ГСИ
"""
from typing import Dict, List, Optional
from .quality_evaluator import QualityEvaluator
from .resistance_checker import ResistanceChecker


class BallScorer:
    """
    Система балльной оценки сортов (1-5 баллов)
    
    Возвращает три независимых балла без взвешенного общего балла
    """
    
    def __init__(self):
        self.quality_evaluator = QualityEvaluator()
        self.resistance_checker = ResistanceChecker()
    
    def calculate_scores(self, sort_data: Dict) -> Dict:
        """
        Расчет трех независимых баллов (1-5)
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Dict с yield_score, quality_score, resistance_score (без overall_score)
        """
        # Расчет баллов по компонентам
        yield_score = self._calculate_yield_score(sort_data)
        quality_score = self.quality_evaluator.calculate_quality_score(sort_data)
        resistance_score = self.resistance_checker.calculate_resistance_score(sort_data)
        
        return {
            'yield_score': yield_score['score'],
            'quality_score': quality_score['score'],
            'resistance_score': resistance_score['score'],
            'detailed_scores': {
                'yield': yield_score,
                'quality': quality_score,
                'resistance': resistance_score
            }
        }
    
    def calculate_overall_score(self, sort_data: Dict) -> Dict:
        """
        Deprecated: использовать calculate_scores()
        
        Оставлено для обратной совместимости
        """
        return self.calculate_scores(sort_data)
    
    def _calculate_yield_score(self, sort_data: Dict) -> Dict:
        """
        Расчет балла по урожайности с использованием конфигурируемых порогов
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Балл и интерпретация по урожайности + детали по регионам
        """
        from django.conf import settings
        config = settings.EVALUATION_THRESHOLDS['yield']
        
        # Получаем данные урожайности
        regions_data = sort_data.get('regions_data', [])
        if not regions_data:
            return {
                'score': 3,
                'interpretation': 'Недостаточно данных для оценки',
                'deviation_from_standard': 0,
                'statistical_significance': False,
                'significant_regions_percent': 0,
                'regions_breakdown': []
            }
        
        # Анализируем статистическую значимость
        significant_regions = 0
        total_deviation = 0
        total_regions = len(regions_data)
        
        # Собираем детали по регионам
        regions_breakdown = []
        
        for region in regions_data:
            if region.get('statistical_significance', False):
                significant_regions += 1
            
            deviation = region.get('deviation_from_standard', 0) or region.get('deviation_percent', 0)
            total_deviation += deviation
            
            # Добавляем полные данные региона
            region_info = region.get('region', {})
            climate_zone = region_info.get('climate_zone')
            
            regions_breakdown.append({
                'region_id': region.get('region_id'),
                'region_name': region.get('region_name'),
                'climate_zone': {
                    'id': climate_zone.get('id') if climate_zone else None,
                    'name': climate_zone.get('name') if climate_zone else None,
                    'code': climate_zone.get('code') if climate_zone else None
                } if climate_zone else None,
                'yields_by_year': region.get('yields_by_year', {}),
                'average_yield': region.get('average_yield'),
                'years_tested': region.get('years_tested', 0),
                'current_year_yield': region.get('current_year_yield'),
                'deviation_from_standard': region.get('deviation_from_standard'),
                'deviation_percent': region.get('deviation_percent'),
                'standard_name': region.get('standard_name'),
                'standard_current_year_yield': region.get('standard_current_year_yield'),
                'statistical_significance': region.get('statistical_significance', False),
                'predecessor': region.get('predecessor', 'Неизвестно')
            })
        
        avg_deviation = total_deviation / total_regions if total_regions > 0 else 0
        significance_percent = (significant_regions / total_regions * 100) if total_regions > 0 else 0
        
        # Используем конфигурируемые пороги
        sig_threshold = config['statistical_significance_threshold']
        dev_sig_pos = config['deviation_significant_positive']
        dev_mod_pos = config['deviation_moderate_positive']
        dev_mod_neg = config['deviation_moderate_negative']
        dev_sig_neg = config['deviation_significant_negative']
        
        # Определение балла по урожайности
        if avg_deviation > 0:
            # Сорт превышает стандарт
            if significance_percent >= 75:
                score = 5
                interpretation = "Значительно превышает стандарт (статистически значимо)"
            elif significance_percent >= sig_threshold:
                score = 4
                interpretation = "Статистически значимо превышает стандарт"
            else:
                # Превышает, но без статистической значимости
                if avg_deviation >= dev_sig_pos:
                    score = 4
                    interpretation = "Значительно превышает стандарт (требует подтверждения)"
                elif avg_deviation >= dev_mod_pos:
                    score = 3
                    interpretation = "Превышает стандарт (требует подтверждения)"
                else:
                    score = 3
                    interpretation = "Незначительно превышает стандарт"
        elif avg_deviation < 0:
            # Сорт уступает стандарту
            if significance_percent >= sig_threshold:
                score = 2
                interpretation = "Статистически значимо уступает стандарту"
            else:
                if avg_deviation <= dev_sig_neg:
                    score = 2
                    interpretation = "Значительно уступает стандарту"
                elif avg_deviation <= dev_mod_neg:
                    score = 2
                    interpretation = "Уступает стандарту"
                else:
                    score = 3
                    interpretation = "Незначительно уступает стандарту"
        else:
            # avg_deviation == 0 или очень близко к 0
            score = 3
            interpretation = "Не отличается от стандарта"
        
        # Подсчет регионов по отклонениям от стандарта
        regions_exceeding = sum(1 for r in regions_breakdown if r.get('deviation_percent', 0) > 0)
        regions_below = sum(1 for r in regions_breakdown if r.get('deviation_percent', 0) < 0)
        regions_neutral = len(regions_breakdown) - regions_exceeding - regions_below

        return {
            'score': score,
            'interpretation': interpretation,
            'deviation_from_standard': round(avg_deviation, 2),
            'statistical_significance': significance_percent >= sig_threshold,
            'significant_regions_percent': round(significance_percent, 1),
            'regions_exceeding': regions_exceeding,
            'regions_below': regions_below,
            'regions_neutral': regions_neutral,
            'regions_breakdown': regions_breakdown
        }
    
