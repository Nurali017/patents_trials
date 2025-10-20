"""
Модуль статистических расчетов для ГСИ
"""
from .nsr_calculator import NSRCalculator
from .significance_test import SignificanceTest
from .variance_analysis import VarianceAnalysis

__all__ = ['NSRCalculator', 'SignificanceTest', 'VarianceAnalysis']