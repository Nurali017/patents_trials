"""
Проверка устойчивости к болезням и стрессам
"""
from typing import Dict, List, Optional


class ResistanceChecker:
    """
    Оценка устойчивости сортов к болезням и неблагоприятным факторам
    """
    
    def __init__(self):
        # Критерии устойчивости по Методике ГСИ (1-10 баллов)
        self.resistance_standards = {
            'disease_resistance': {
                'excellent': 9.0,      # 5 баллов
                'good': 7.0,          # 4 балла
                'satisfactory': 5.0,  # 3 балла
                'poor': 3.0           # 2 балла
            },
            'lodging_resistance': {
                'excellent': 7.0,      # 5 баллов - ≥7.0
                'good': 5.0,           # 4 балла - ≥5.0
                'satisfactory': 3.0,   # 3 балла - ≥3.0
                'poor': 1.0            # 2 балла - ≥1.0
            },
            'drought_resistance': {
                'excellent': 7.0,      # 5 баллов - ≥7.0
                'good': 5.0,           # 4 балла - ≥5.0
                'satisfactory': 3.0,   # 3 балла - ≥3.0
                'poor': 1.0            # 2 балла - ≥1.0
            },
            'winter_hardiness': {
                'excellent': 7.0,      # 5 баллов - ≥7.0
                'good': 5.0,           # 4 балла - ≥5.0
                'satisfactory': 3.0,   # 3 балла - ≥3.0
                'poor': 1.0            # 2 балла - ≥1.0
            },
            'shattering_resistance': {
                'excellent': 7.0,      # 5 баллов - ≥7.0
                'good': 5.0,           # 4 балла - ≥5.0
                'satisfactory': 3.0,   # 3 балла - ≥3.0
                'poor': 1.0            # 2 балла - ≥1.0
            },
            'sprouting_resistance': {
                'excellent': 7.0,      # 5 баллов - ≥7.0
                'good': 5.0,           # 4 балла - ≥5.0
                'satisfactory': 3.0,   # 3 балла - ≥3.0
                'poor': 1.0            # 2 балла - ≥1.0
            }
        }
    
    def calculate_resistance_score(self, sort_data: Dict) -> Dict:
        """
        Расчет балла по устойчивости
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Балл и детали по устойчивости
        """
        # Получаем показатели устойчивости
        resistance_indicators = self._extract_resistance_indicators(sort_data)
        
        if not resistance_indicators:
            return {
                'score': None,  # Явно указываем отсутствие данных
                'interpretation': 'Данные по устойчивости отсутствуют',
                'indicators': {},
                'sufficient_data': False,
                'data_available': False
            }
        
        # Расчет баллов по каждому показателю
        indicator_scores = {}
        total_score = 0
        valid_indicators = 0
        
        for indicator, value in resistance_indicators.items():
            if value is not None:
                score = self._get_resistance_score(indicator, value)
                indicator_scores[indicator] = {
                    'value': value,
                    'score': score,
                    'interpretation': self._get_resistance_interpretation(score)
                }
                total_score += score
                valid_indicators += 1
        
        # Средний балл по устойчивости
        avg_score = total_score / valid_indicators if valid_indicators > 0 else 3
        
        return {
            'score': round(avg_score, 1),
            'interpretation': self._get_overall_resistance_interpretation(avg_score),
            'indicators': indicator_scores,
            'sufficient_data': valid_indicators >= 2  # Минимум 2 показателя
        }
    
    def _extract_resistance_indicators(self, sort_data: Dict) -> Dict:
        """
        Извлечение показателей устойчивости из данных сорта
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Словарь показателей устойчивости
        """
        resistance_indicators = {}
        
        # Ищем показатели устойчивости в регионах и усредняем
        regions_data = sort_data.get('regions_data', [])
        indicator_values = {}  # Словарь для накопления значений по показателям
        
        for region in regions_data:
            region_resistance = region.get('resistance_indicators', {})
            for indicator, value in region_resistance.items():
                if value is not None:
                    if indicator not in indicator_values:
                        indicator_values[indicator] = []
                    indicator_values[indicator].append(value)
        
        # Вычисляем средние значения
        for indicator, values in indicator_values.items():
            if values:
                avg_value = sum(values) / len(values)
                resistance_indicators[indicator] = round(avg_value, 1)
        
        # Ищем в общих данных сорта
        summary_resistance = sort_data.get('summary', {}).get('resistance_indicators', {})
        for indicator, value in summary_resistance.items():
            if value is not None and indicator not in resistance_indicators:
                resistance_indicators[indicator] = value
        
        return resistance_indicators
    
    def _get_resistance_score(self, indicator: str, value: float) -> int:
        """
        Получение балла для показателя устойчивости
        
        Args:
            indicator: Название показателя
            value: Значение показателя (1-10)
            
        Returns:
            Балл (1-5)
        """
        if indicator not in self.resistance_standards:
            return 3  # Средний балл для неизвестных показателей
        
        standards = self.resistance_standards[indicator]
        
        if value >= standards['excellent']:
            return 5
        elif value >= standards['good']:
            return 4
        elif value >= standards['satisfactory']:
            return 3
        elif value >= standards['poor']:
            return 2
        else:
            return 1
    
    def _get_resistance_interpretation(self, score: int) -> str:
        """
        Интерпретация балла устойчивости
        
        Args:
            score: Балл (1-5)
            
        Returns:
            Текстовая интерпретация
        """
        interpretations = {
            5: "Отличная устойчивость",
            4: "Хорошая устойчивость",
            3: "Удовлетворительная устойчивость",
            2: "Слабая устойчивость",
            1: "Очень слабая устойчивость"
        }
        return interpretations.get(score, "Неизвестно")
    
    def _get_overall_resistance_interpretation(self, avg_score: float) -> str:
        """
        Общая интерпретация устойчивости
        
        Args:
            avg_score: Средний балл устойчивости
            
        Returns:
            Общая интерпретация
        """
        if avg_score >= 4.5:
            return "Отличная устойчивость к болезням и стрессам"
        elif avg_score >= 3.5:
            return "Хорошая устойчивость"
        elif avg_score >= 2.5:
            return "Удовлетворительная устойчивость"
        elif avg_score >= 1.5:
            return "Слабая устойчивость"
        else:
            return "Очень слабая устойчивость"
    
    def check_critical_resistance(self, sort_data: Dict) -> Dict:
        """
        Проверка критических показателей устойчивости
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Результаты проверки критических показателей
        """
        resistance_indicators = self._extract_resistance_indicators(sort_data)
        
        critical_checks = {
            'disease_resistance_critical': False,
            'lodging_resistance_critical': False,
            'winter_hardiness_critical': False,
            'overall_critical': False
        }
        
        # Проверка критических показателей
        if 'disease_resistance' in resistance_indicators:
            disease_value = resistance_indicators['disease_resistance']
            critical_checks['disease_resistance_critical'] = disease_value < 3.0
        
        if 'lodging_resistance' in resistance_indicators:
            lodging_value = resistance_indicators['lodging_resistance']
            critical_checks['lodging_resistance_critical'] = lodging_value < 3.0
        
        if 'winter_hardiness' in resistance_indicators:
            winter_value = resistance_indicators['winter_hardiness']
            critical_checks['winter_hardiness_critical'] = winter_value < 3.0
        
        # Общая критическая оценка
        critical_checks['overall_critical'] = any([
            critical_checks['disease_resistance_critical'],
            critical_checks['lodging_resistance_critical'],
            critical_checks['winter_hardiness_critical']
        ])
        
        return critical_checks
    
    def get_resistance_requirements(self) -> Dict:
        """
        Получение требований к устойчивости по Методике
        
        Returns:
            Словарь требований
        """
        return {
            'minimum_requirements': {
                'disease_resistance': 5.0,     # Минимум для допуска
                'lodging_resistance': 4.0,     # Минимум для допуска
                'drought_resistance': 4.0,     # Минимум для допуска
                'winter_hardiness': 4.0        # Минимум для допуска
            },
            'excellent_standards': {
                'disease_resistance': 9.0,     # Отличный уровень
                'lodging_resistance': 8.0,     # Отличный уровень
                'drought_resistance': 8.0,     # Отличный уровень
                'winter_hardiness': 8.0        # Отличный уровень
            }
        }
