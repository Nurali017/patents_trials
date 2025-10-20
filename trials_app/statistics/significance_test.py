"""
Тесты статистической значимости
"""
from typing import List, Dict, Optional
import math


class SignificanceTest:
    """
    Тесты статистической значимости для ГСИ
    """
    
    def __init__(self):
        self.alpha = 0.05  # Уровень значимости
    
    def t_test(self, sample1: List[float], sample2: List[float]) -> Dict:
        """
        t-тест для сравнения двух выборок
        
        Args:
            sample1: Первая выборка
            sample2: Вторая выборка
            
        Returns:
            Результаты t-теста
        """
        if len(sample1) < 2 or len(sample2) < 2:
            return {
                'significant': False,
                'p_value': None,
                't_statistic': None,
                'error': 'Недостаточно данных для t-теста'
            }
        
        # Вычисляем средние
        mean1 = sum(sample1) / len(sample1)
        mean2 = sum(sample2) / len(sample2)
        
        # Вычисляем дисперсии
        var1 = sum((x - mean1) ** 2 for x in sample1) / (len(sample1) - 1)
        var2 = sum((x - mean2) ** 2 for x in sample2) / (len(sample2) - 1)
        
        # Объединенная дисперсия
        pooled_var = ((len(sample1) - 1) * var1 + (len(sample2) - 1) * var2) / (len(sample1) + len(sample2) - 2)
        
        # Стандартная ошибка разности
        se_diff = math.sqrt(pooled_var * (1/len(sample1) + 1/len(sample2)))
        
        # t-статистика
        t_stat = (mean1 - mean2) / se_diff
        
        # Степени свободы
        df = len(sample1) + len(sample2) - 2
        
        # Критическое значение t
        from scipy import stats
        t_critical = stats.t.ppf(1 - self.alpha/2, df)
        
        # p-значение
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
        
        return {
            'significant': abs(t_stat) > t_critical,
            'p_value': p_value,
            't_statistic': t_stat,
            't_critical': t_critical,
            'degrees_of_freedom': df,
            'mean_difference': mean1 - mean2,
            'standard_error': se_diff
        }
    
    def f_test(self, groups: List[List[float]]) -> Dict:
        """
        F-тест для дисперсионного анализа
        
        Args:
            groups: Группы данных для сравнения
            
        Returns:
            Результаты F-теста
        """
        if len(groups) < 2:
            return {
                'significant': False,
                'p_value': None,
                'f_statistic': None,
                'error': 'Недостаточно групп для F-теста'
            }
        
        # Общее среднее
        all_values = [val for group in groups for val in group]
        grand_mean = sum(all_values) / len(all_values)
        
        # Сумма квадратов между группами
        ss_between = sum(len(group) * (sum(group) / len(group) - grand_mean) ** 2 for group in groups)
        
        # Сумма квадратов внутри групп
        ss_within = sum(sum((val - sum(group) / len(group)) ** 2 for val in group) for group in groups)
        
        # Степени свободы
        df_between = len(groups) - 1
        df_within = sum(len(group) - 1 for group in groups)
        
        # Средние квадраты
        ms_between = ss_between / df_between if df_between > 0 else 0
        ms_within = ss_within / df_within if df_within > 0 else 0
        
        # F-статистика
        f_stat = ms_between / ms_within if ms_within > 0 else 0
        
        # Критическое значение F
        from scipy import stats
        f_critical = stats.f.ppf(1 - self.alpha, df_between, df_within)
        
        # p-значение
        p_value = 1 - stats.f.cdf(f_stat, df_between, df_within)
        
        return {
            'significant': f_stat > f_critical,
            'p_value': p_value,
            'f_statistic': f_stat,
            'f_critical': f_critical,
            'degrees_of_freedom_between': df_between,
            'degrees_of_freedom_within': df_within,
            'mean_square_between': ms_between,
            'mean_square_within': ms_within
        }
    
    def chi_square_test(self, observed: List[List[float]], expected: List[List[float]] = None) -> Dict:
        """
        Критерий хи-квадрат
        
        Args:
            observed: Наблюдаемые частоты
            expected: Ожидаемые частоты (опционально)
            
        Returns:
            Результаты критерия хи-квадрат
        """
        if not observed or not observed[0]:
            return {
                'significant': False,
                'p_value': None,
                'chi_square': None,
                'error': 'Недостаточно данных для критерия хи-квадрат'
            }
        
        # Если ожидаемые частоты не заданы, вычисляем их
        if expected is None:
            total = sum(sum(row) for row in observed)
            row_totals = [sum(row) for row in observed]
            col_totals = [sum(observed[i][j] for i in range(len(observed))) for j in range(len(observed[0]))]
            
            expected = []
            for i in range(len(observed)):
                expected_row = []
                for j in range(len(observed[i])):
                    expected_val = (row_totals[i] * col_totals[j]) / total
                    expected_row.append(expected_val)
                expected.append(expected_row)
        
        # Вычисляем хи-квадрат
        chi_square = 0
        for i in range(len(observed)):
            for j in range(len(observed[i])):
                if expected[i][j] > 0:
                    chi_square += (observed[i][j] - expected[i][j]) ** 2 / expected[i][j]
        
        # Степени свободы
        df = (len(observed) - 1) * (len(observed[0]) - 1)
        
        # Критическое значение хи-квадрат
        from scipy import stats
        chi_critical = stats.chi2.ppf(1 - self.alpha, df)
        
        # p-значение
        p_value = 1 - stats.chi2.cdf(chi_square, df)
        
        return {
            'significant': chi_square > chi_critical,
            'p_value': p_value,
            'chi_square': chi_square,
            'chi_critical': chi_critical,
            'degrees_of_freedom': df
        }
