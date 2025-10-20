"""
Расчет НСР₀.₉₅ (Наименьшая существенная разность)
"""
import math
from scipy import stats
from typing import List, Dict, Optional, Tuple


class NSRCalculator:
    """
    Калькулятор НСР₀.₉₅ для статистической оценки сортов
    """
    
    def __init__(self):
        self.confidence_level = 0.95
        self.alpha = 1 - self.confidence_level
    
    def calculate_nsr(self, yields_data: List[float], standard_yields: List[float] = None) -> Dict:
        """
        Расчет НСР₀.₉₅ для сравнения сортов
        
        Args:
            yields_data: Урожайности испытываемого сорта
            standard_yields: Урожайности стандарта (опционально)
            
        Returns:
            Dict с результатами расчета НСР
        """
        if len(yields_data) < 2:
            return {
                'nsr_value': None,
                'sufficient_data': False,
                'error': 'Недостаточно данных для расчета НСР'
            }
        
        try:
            # Расчет дисперсии ошибки
            error_variance = self._calculate_error_variance(yields_data)
            
            # Количество повторностей
            repetitions = len(yields_data)
            
            # Степени свободы
            degrees_of_freedom = repetitions - 1
            
            # Критическое значение t-критерия Стьюдента
            t_critical = stats.t.ppf(1 - self.alpha/2, degrees_of_freedom)
            
            # Расчет НСР₀.₉₅
            nsr_value = t_critical * math.sqrt(2 * error_variance / repetitions)
            
            return {
                'nsr_value': round(nsr_value, 2),
                'error_variance': round(error_variance, 2),
                'degrees_of_freedom': degrees_of_freedom,
                'repetitions': repetitions,
                't_critical': round(t_critical, 3),
                'confidence_level': self.confidence_level,
                'sufficient_data': True
            }
            
        except Exception as e:
            return {
                'nsr_value': None,
                'sufficient_data': False,
                'error': f'Ошибка расчета НСР: {str(e)}'
            }
    
    def is_significant(self, difference: float, nsr_value: float) -> bool:
        """
        Проверка статистической значимости различия
        
        Args:
            difference: Разность между сортом и стандартом
            nsr_value: Значение НСР₀.₉₅
            
        Returns:
            True если разность статистически значима
        """
        if nsr_value is None:
            return False
        
        return abs(difference) >= nsr_value
    
    def get_significance_level(self, difference: float, nsr_value: float) -> str:
        """
        Определение уровня значимости различия
        
        Args:
            difference: Разность между сортом и стандартом
            nsr_value: Значение НСР₀.₉₅
            
        Returns:
            Уровень значимости: 'high', 'medium', 'low', 'none'
        """
        if nsr_value is None:
            return 'none'
        
        ratio = abs(difference) / nsr_value
        
        if ratio >= 1.5:
            return 'high'      # >1.5 НСР - высокая значимость
        elif ratio >= 1.0:
            return 'medium'    # >1.0 НСР - средняя значимость
        elif ratio >= 0.5:
            return 'low'       # >0.5 НСР - низкая значимость
        else:
            return 'none'      # <0.5 НСР - незначимо
    
    def _calculate_error_variance(self, yields_data: List[float]) -> float:
        """
        Расчет дисперсии ошибки опыта
        
        Args:
            yields_data: Данные по урожайности
            
        Returns:
            Дисперсия ошибки
        """
        if len(yields_data) < 2:
            return 0.0
        
        # Среднее значение
        mean_yield = sum(yields_data) / len(yields_data)
        
        # Сумма квадратов отклонений
        sum_squares = sum((yield_val - mean_yield) ** 2 for yield_val in yields_data)
        
        # Дисперсия ошибки
        error_variance = sum_squares / (len(yields_data) - 1)
        
        return error_variance
    
    def calculate_confidence_interval(self, mean_value: float, nsr_value: float) -> Tuple[float, float]:
        """
        Расчет доверительного интервала
        
        Args:
            mean_value: Среднее значение
            nsr_value: Значение НСР₀.₉₅
            
        Returns:
            Кортеж (нижняя граница, верхняя граница)
        """
        if nsr_value is None:
            return (mean_value, mean_value)
        
        margin = nsr_value / 2  # Половина НСР для доверительного интервала
        lower_bound = mean_value - margin
        upper_bound = mean_value + margin
        
        return (round(lower_bound, 2), round(upper_bound, 2))
    
    def calculate_combined_nsr(self, regions_data: List[Dict]) -> Dict:
        """
        Расчет объединенного НСР по всем регионам
        
        Args:
            regions_data: Данные по регионам с НСР
            
        Returns:
            Объединенные статистические показатели
        """
        valid_nsr = [region.get('nsr_value') for region in regions_data 
                    if region.get('nsr_value') is not None]
        
        if not valid_nsr:
            return {
                'combined_nsr': None,
                'regions_count': 0,
                'sufficient_data': False
            }
        
        # Средневзвешенное НСР
        combined_nsr = sum(valid_nsr) / len(valid_nsr)
        
        # Количество регионов со значимыми различиями
        significant_regions = sum(1 for region in regions_data 
                                if region.get('statistical_significance', False))
        
        return {
            'combined_nsr': round(combined_nsr, 2),
            'regions_count': len(valid_nsr),
            'significant_regions': significant_regions,
            'significant_percent': round(significant_regions / len(valid_nsr) * 100, 1),
            'sufficient_data': True
        }
