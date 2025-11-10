"""
Проверка устойчивости к болезням и стрессам
"""
from typing import Dict, List, Optional


class ResistanceChecker:
    """
    Оценка устойчивости сортов к болезням и неблагоприятным факторам
    Использует конфигурируемые пороги из Django settings
    """
    
    def __init__(self):
        from django.conf import settings
        config = settings.EVALUATION_THRESHOLDS['resistance']
        
        # Извлекаем стандарты устойчивости и служебные параметры
        self.resistance_standards = {k: v for k, v in config.items() 
                                     if isinstance(v, dict)}
        self.minimum_indicators = config.get('minimum_indicators', 2)
        self.minimum_years_tested = config.get('minimum_years_tested', 2)
        self.critical_indicators = config.get('critical_indicators', [])
    
    def calculate_resistance_score(self, sort_data: Dict) -> Dict:
        """
        Расчет балла по устойчивости с проверкой критических показателей
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Балл и детали по устойчивости, включая критические провалы
        """
        # Получаем показатели устойчивости
        resistance_indicators = self._extract_resistance_indicators(sort_data)
        
        if not resistance_indicators:
            return {
                'score': None,
                'interpretation': 'Данные по устойчивости отсутствуют',
                'indicators': {},
                'sufficient_data': False,
                'data_available': False,
                'critical_failures': []
            }
        
        # Расчет баллов по каждому показателю
        indicator_scores = {}
        total_score = 0
        valid_indicators = 0
        critical_failures = []

        for indicator, value in resistance_indicators.items():
            if value is not None:
                score = self._get_resistance_score(indicator, value)
                # Упрощенная структура: только значение
                indicator_scores[indicator] = value
                total_score += score
                valid_indicators += 1

                # Проверка критических показателей
                if indicator in self.critical_indicators:
                    critical_threshold = self.resistance_standards[indicator].get('critical', 3.0)
                    if value < critical_threshold:
                        critical_failures.append({
                            'indicator': indicator,
                            'value': value,
                            'threshold': critical_threshold
                        })
        
        # Проверка достаточности данных
        years_tested = sort_data.get('overall_summary', {}).get('overall_min_years_tested', 0)
        sufficient_data = (valid_indicators >= self.minimum_indicators and 
                          years_tested >= self.minimum_years_tested)
        
        # Средний балл по устойчивости
        if valid_indicators > 0:
            avg_score = total_score / valid_indicators
            score_value = round(avg_score, 1)
        else:
            score_value = None
        
        return {
            'score': score_value,
            'interpretation': self._get_overall_resistance_interpretation(avg_score) if score_value else 'Недостаточно данных',
            'indicators': indicator_scores,
            'sufficient_data': sufficient_data,
            'data_available': True,
            'critical_failures': critical_failures
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
        # Если показатель не в стандартах, используем универсальные пороги
        if indicator not in self.resistance_standards:
            # Универсальные пороги для шкалы 1-10
            if value >= 5.0:
                return 5
            elif value >= 4.0:
                return 4
            elif value >= 3.0:
                return 3
            elif value >= 2.0:
                return 2
            else:
                return 1
        
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
