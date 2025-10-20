"""
Дисперсионный анализ для ГСИ
"""
from typing import List, Dict, Optional
import math


class VarianceAnalysis:
    """
    Дисперсионный анализ для сортоиспытаний
    """
    
    def __init__(self):
        self.alpha = 0.05  # Уровень значимости
    
    def one_way_anova(self, groups: List[List[float]]) -> Dict:
        """
        Однофакторный дисперсионный анализ
        
        Args:
            groups: Группы данных (сорта, варианты)
            
        Returns:
            Результаты однофакторного ANOVA
        """
        if len(groups) < 2:
            return {
                'significant': False,
                'p_value': None,
                'f_statistic': None,
                'error': 'Недостаточно групп для ANOVA'
            }
        
        # Общее количество наблюдений
        n_total = sum(len(group) for group in groups)
        k = len(groups)  # Количество групп
        
        # Общее среднее
        all_values = [val for group in groups for val in group]
        grand_mean = sum(all_values) / len(all_values)
        
        # Сумма квадратов между группами (SS Between)
        ss_between = 0
        for group in groups:
            group_mean = sum(group) / len(group)
            ss_between += len(group) * (group_mean - grand_mean) ** 2
        
        # Сумма квадратов внутри групп (SS Within)
        ss_within = 0
        for group in groups:
            group_mean = sum(group) / len(group)
            for value in group:
                ss_within += (value - group_mean) ** 2
        
        # Общая сумма квадратов (SS Total)
        ss_total = ss_between + ss_within
        
        # Степени свободы
        df_between = k - 1
        df_within = n_total - k
        df_total = n_total - 1
        
        # Средние квадраты
        ms_between = ss_between / df_between if df_between > 0 else 0
        ms_within = ss_within / df_within if df_within > 0 else 0
        
        # F-статистика
        f_statistic = ms_between / ms_within if ms_within > 0 else 0
        
        # Критическое значение F
        from scipy import stats
        f_critical = stats.f.ppf(1 - self.alpha, df_between, df_within)
        
        # p-значение
        p_value = 1 - stats.f.cdf(f_statistic, df_between, df_within)
        
        return {
            'significant': f_statistic > f_critical,
            'p_value': p_value,
            'f_statistic': f_statistic,
            'f_critical': f_critical,
            'ss_between': ss_between,
            'ss_within': ss_within,
            'ss_total': ss_total,
            'ms_between': ms_between,
            'ms_within': ms_within,
            'df_between': df_between,
            'df_within': df_within,
            'df_total': df_total,
            'eta_squared': ss_between / ss_total if ss_total > 0 else 0  # Доля объясненной дисперсии
        }
    
    def two_way_anova(self, data: List[List[List[float]]]) -> Dict:
        """
        Двухфакторный дисперсионный анализ
        
        Args:
            data: Данные в формате [фактор_A][фактор_B][наблюдения]
            
        Returns:
            Результаты двухфакторного ANOVA
        """
        if len(data) < 2 or len(data[0]) < 2:
            return {
                'significant': False,
                'p_value': None,
                'f_statistic': None,
                'error': 'Недостаточно данных для двухфакторного ANOVA'
            }
        
        # Количество уровней факторов
        a = len(data)  # Фактор A
        b = len(data[0])  # Фактор B
        
        # Общее количество наблюдений
        n_total = sum(sum(len(cell) for cell in row) for row in data)
        
        # Общее среднее
        all_values = [val for row in data for cell in row for val in cell]
        grand_mean = sum(all_values) / len(all_values)
        
        # Средние по строкам (фактор A)
        row_means = []
        for row in data:
            row_values = [val for cell in row for val in cell]
            row_means.append(sum(row_values) / len(row_values))
        
        # Средние по столбцам (фактор B)
        col_means = []
        for j in range(b):
            col_values = [val for row in data for val in row[j]]
            col_means.append(sum(col_values) / len(col_values))
        
        # Сумма квадратов
        ss_total = sum((val - grand_mean) ** 2 for val in all_values)
        
        # SS для фактора A
        ss_a = 0
        for i, row_mean in enumerate(row_means):
            n_row = sum(len(cell) for cell in data[i])
            ss_a += n_row * (row_mean - grand_mean) ** 2
        
        # SS для фактора B
        ss_b = 0
        for j, col_mean in enumerate(col_means):
            n_col = sum(len(data[i][j]) for i in range(a))
            ss_b += n_col * (col_mean - grand_mean) ** 2
        
        # SS для взаимодействия
        ss_ab = 0
        for i in range(a):
            for j in range(b):
                cell_values = data[i][j]
                cell_mean = sum(cell_values) / len(cell_values)
                ss_ab += len(cell_values) * (cell_mean - row_means[i] - col_means[j] + grand_mean) ** 2
        
        # SS ошибки
        ss_error = 0
        for i in range(a):
            for j in range(b):
                cell_values = data[i][j]
                cell_mean = sum(cell_values) / len(cell_values)
                for val in cell_values:
                    ss_error += (val - cell_mean) ** 2
        
        # Степени свободы
        df_a = a - 1
        df_b = b - 1
        df_ab = (a - 1) * (b - 1)
        df_error = n_total - a * b
        df_total = n_total - 1
        
        # Средние квадраты
        ms_a = ss_a / df_a if df_a > 0 else 0
        ms_b = ss_b / df_b if df_b > 0 else 0
        ms_ab = ss_ab / df_ab if df_ab > 0 else 0
        ms_error = ss_error / df_error if df_error > 0 else 0
        
        # F-статистики
        f_a = ms_a / ms_error if ms_error > 0 else 0
        f_b = ms_b / ms_error if ms_error > 0 else 0
        f_ab = ms_ab / ms_error if ms_error > 0 else 0
        
        # Критические значения F
        from scipy import stats
        f_critical_a = stats.f.ppf(1 - self.alpha, df_a, df_error)
        f_critical_b = stats.f.ppf(1 - self.alpha, df_b, df_error)
        f_critical_ab = stats.f.ppf(1 - self.alpha, df_ab, df_error)
        
        # p-значения
        p_value_a = 1 - stats.f.cdf(f_a, df_a, df_error)
        p_value_b = 1 - stats.f.cdf(f_b, df_b, df_error)
        p_value_ab = 1 - stats.f.cdf(f_ab, df_ab, df_error)
        
        return {
            'factor_a': {
                'significant': f_a > f_critical_a,
                'p_value': p_value_a,
                'f_statistic': f_a,
                'f_critical': f_critical_a,
                'ss': ss_a,
                'ms': ms_a,
                'df': df_a
            },
            'factor_b': {
                'significant': f_b > f_critical_b,
                'p_value': p_value_b,
                'f_statistic': f_b,
                'f_critical': f_critical_b,
                'ss': ss_b,
                'ms': ms_b,
                'df': df_b
            },
            'interaction': {
                'significant': f_ab > f_critical_ab,
                'p_value': p_value_ab,
                'f_statistic': f_ab,
                'f_critical': f_critical_ab,
                'ss': ss_ab,
                'ms': ms_ab,
                'df': df_ab
            },
            'error': {
                'ss': ss_error,
                'ms': ms_error,
                'df': df_error
            },
            'total': {
                'ss': ss_total,
                'df': df_total
            }
        }
    
    def calculate_coefficient_of_variation(self, data: List[float]) -> float:
        """
        Расчет коэффициента вариации
        
        Args:
            data: Данные для расчета
            
        Returns:
            Коэффициент вариации в процентах
        """
        if not data:
            return 0.0
        
        mean = sum(data) / len(data)
        if mean == 0:
            return 0.0
        
        variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
        std_dev = math.sqrt(variance)
        
        cv = (std_dev / mean) * 100
        return round(cv, 2)
    
    def calculate_heritability(self, genetic_variance: float, phenotypic_variance: float) -> float:
        """
        Расчет наследуемости признака
        
        Args:
            genetic_variance: Генетическая дисперсия
            phenotypic_variance: Фенотипическая дисперсия
            
        Returns:
            Коэффициент наследуемости
        """
        if phenotypic_variance == 0:
            return 0.0
        
        heritability = genetic_variance / phenotypic_variance
        return round(heritability, 3)
