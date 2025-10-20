"""
Балльная система оценки сортов по Методике ГСИ
"""
from typing import Dict, List, Optional
from .quality_evaluator import QualityEvaluator
from .resistance_checker import ResistanceChecker


class BallScorer:
    """
    Система балльной оценки сортов (1-5 баллов)
    """
    
    def __init__(self):
        self.quality_evaluator = QualityEvaluator()
        self.resistance_checker = ResistanceChecker()
        
        # Веса по Методике ГСИ
        self.weights = {
            'yield': 0.4,      # 40% - урожайность
            'quality': 0.3,    # 30% - качество
            'resistance': 0.3  # 30% - устойчивость
        }
    
    def calculate_overall_score(self, sort_data: Dict) -> Dict:
        """
        Расчет общего балла сорта
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Полная балльная оценка
        """
        # Расчет баллов по компонентам
        yield_score = self._calculate_yield_score(sort_data)
        quality_score = self.quality_evaluator.calculate_quality_score(sort_data)
        resistance_score = self.resistance_checker.calculate_resistance_score(sort_data)
        
        # Общий балл с весами (только для доступных данных)
        total_weight = 0
        weighted_sum = 0
        
        # Урожайность (всегда есть)
        if yield_score['score'] is not None:
            weighted_sum += yield_score['score'] * self.weights['yield']
            total_weight += self.weights['yield']
        
        # Качество
        if quality_score['score'] is not None:
            weighted_sum += quality_score['score'] * self.weights['quality']
            total_weight += self.weights['quality']
        
        # Устойчивость
        if resistance_score['score'] is not None:
            weighted_sum += resistance_score['score'] * self.weights['resistance']
            total_weight += self.weights['resistance']
        
        # Рассчитываем общий балл только по доступным данным
        if total_weight > 0:
            overall_score = weighted_sum / total_weight
        else:
            overall_score = yield_score['score'] if yield_score['score'] is not None else 3
        
        return {
            'yield_score': yield_score['score'],
            'quality_score': quality_score['score'],
            'resistance_score': resistance_score['score'],
            'overall_score': round(overall_score, 1),
            'score_interpretation': self._get_interpretation(overall_score),
            'detailed_scores': {
                'yield': yield_score,
                'quality': quality_score,
                'resistance': resistance_score
            }
        }
    
    def _calculate_yield_score(self, sort_data: Dict) -> Dict:
        """
        Расчет балла по урожайности
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Балл и интерпретация по урожайности
        """
        # Получаем данные урожайности
        regions_data = sort_data.get('regions_data', [])
        if not regions_data:
            return {
                'score': 3,
                'interpretation': 'Недостаточно данных для оценки',
                'deviation_from_standard': 0,
                'statistical_significance': False
            }
        
        # Анализируем статистическую значимость
        significant_regions = 0
        total_deviation = 0
        total_regions = len(regions_data)
        
        for region in regions_data:
            if region.get('statistical_significance', False):
                significant_regions += 1
            total_deviation += region.get('deviation_from_standard', 0)
        
        avg_deviation = total_deviation / total_regions if total_regions > 0 else 0
        significance_percent = (significant_regions / total_regions * 100) if total_regions > 0 else 0
        
        # Определение балла по урожайности
        # Сначала проверяем фактическое превышение, затем статистическую значимость
        if avg_deviation > 0:
            # Сорт превышает стандарт
            if significance_percent >= 75:
                score = 5
                interpretation = "Значительно превышает стандарт (статистически значимо)"
            elif significance_percent >= 50:
                score = 4
                interpretation = "Статистически значимо превышает стандарт"
            else:
                # Превышает, но без статистической значимости (мало данных)
                if avg_deviation >= 5.0:  # Большое превышение
                    score = 4
                    interpretation = "Значительно превышает стандарт (требует подтверждения)"
                elif avg_deviation >= 2.0:  # Среднее превышение
                    score = 3
                    interpretation = "Превышает стандарт (требует подтверждения)"
                else:  # Небольшое превышение
                    score = 3
                    interpretation = "Незначительно превышает стандарт"
        elif avg_deviation < 0:
            # Сорт уступает стандарту
            if significance_percent >= 50:
                score = 2
                interpretation = "Статистически значимо уступает стандарту"
            else:
                if abs(avg_deviation) >= 5.0:  # Большое отставание
                    score = 2
                    interpretation = "Значительно уступает стандарту"
                elif abs(avg_deviation) >= 2.0:  # Среднее отставание
                    score = 2
                    interpretation = "Уступает стандарту"
                else:  # Небольшое отставание
                    score = 3
                    interpretation = "Незначительно уступает стандарту"
        else:
            # avg_deviation == 0 или очень близко к 0
            score = 3
            interpretation = "Не отличается от стандарта"
        
        return {
            'score': score,
            'interpretation': interpretation,
            'deviation_from_standard': round(avg_deviation, 2),
            'statistical_significance': significance_percent >= 50,
            'significant_regions_percent': round(significance_percent, 1)
        }
    
    def _get_interpretation(self, score: float) -> str:
        """
        Интерпретация общего балла по Методике ГСИ
        
        Args:
            score: Общий балл (1-5)
            
        Returns:
            Текстовая интерпретация
        """
        if score >= 4.5:
            return "Отличный сорт"
        elif score >= 3.5:
            return "Хороший, не уступает большинству сортов"
        elif score >= 2.5:
            return "Удовлетворительный, требует дополнительного изучения"
        elif score >= 1.5:
            return "Посредственный, возможный кандидат к снятию"
        else:
            return "Плохой, рекомендуется к снятию"
    
    def get_decision_criteria(self, score_data: Dict) -> Dict:
        """
        Определение критериев для принятия решения
        
        Args:
            score_data: Данные балльной оценки
            
        Returns:
            Критерии для решения
        """
        overall_score = score_data['overall_score']
        yield_score = score_data['yield_score']
        quality_score = score_data['quality_score']
        resistance_score = score_data['resistance_score']
        
        # Критерии одобрения (обрабатываем None значения)
        approved_criteria = {
            'overall_score_met': overall_score >= 4.0 if overall_score is not None else False,
            'yield_score_met': yield_score >= 4 if yield_score is not None else False,
            'quality_score_met': quality_score >= 3 if quality_score is not None else False,
            'resistance_score_met': resistance_score >= 3 if resistance_score is not None else False,
            'all_criteria_met': (
                (overall_score >= 4.0 if overall_score is not None else False) and 
                (yield_score >= 4 if yield_score is not None else False) and 
                (quality_score >= 3 if quality_score is not None else False) and 
                (resistance_score >= 3 if resistance_score is not None else False)
            )
        }
        
        # Критерии отклонения (обрабатываем None значения)
        rejected_criteria = {
            'overall_score_low': overall_score <= 2.0 if overall_score is not None else False,
            'yield_score_low': yield_score <= 2 if yield_score is not None else False,
            'quality_score_low': quality_score <= 2 if quality_score is not None else False,
            'resistance_score_low': resistance_score <= 2 if resistance_score is not None else False,
            'any_criteria_failed': (
                (overall_score <= 2.0 if overall_score is not None else False) or 
                (yield_score <= 2 if yield_score is not None else False) or 
                (quality_score <= 2 if quality_score is not None else False) or 
                (resistance_score <= 2 if resistance_score is not None else False)
            )
        }
        
        return {
            'approved_criteria': approved_criteria,
            'rejected_criteria': rejected_criteria,
            'recommendation': self._get_recommendation(approved_criteria, rejected_criteria)
        }
    
    def _get_recommendation(self, approved: Dict, rejected: Dict) -> str:
        """
        Получение рекомендации на основе критериев
        
        Args:
            approved: Критерии одобрения
            rejected: Критерии отклонения
            
        Returns:
            Рекомендация
        """
        if approved['all_criteria_met']:
            return 'approved'
        elif rejected['any_criteria_failed']:
            return 'rejected'
        else:
            return 'continue'
