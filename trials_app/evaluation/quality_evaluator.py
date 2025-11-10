"""
Оценка качества продукции по Методике ГСИ
"""
from typing import Dict, List, Optional


class QualityEvaluator:
    """
    Оценка качества зерна и продукции
    Использует конфигурируемые пороги из Django settings
    """
    
    def __init__(self):
        from django.conf import settings
        config = settings.EVALUATION_THRESHOLDS['quality']
        
        # Извлекаем стандарты качества и служебные параметры
        self.quality_standards = {k: v for k, v in config.items() 
                                  if isinstance(v, dict)}
        self.minimum_indicators = config.get('minimum_indicators', 2)
        self.minimum_years_tested = config.get('minimum_years_tested', 2)
    
    def calculate_quality_score(self, sort_data: Dict) -> Dict:
        """
        Расчет балла по качеству продукции с валидацией данных
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Балл и детали по качеству
        """
        # Получаем показатели качества
        quality_indicators = self._extract_quality_indicators(sort_data)
        
        if not quality_indicators:
            return {
                'score': None,
                'interpretation': 'Данные по качеству отсутствуют',
                'indicators': {},
                'sufficient_data': False,
                'data_available': False,
                'validation_warnings': []
            }
        
        # Валидация данных
        validation_warnings = []
        validated_indicators = {}
        
        for indicator, value in quality_indicators.items():
            if value is not None:
                # Проверка на выбросы и разумность значений
                validation_result = self._validate_indicator_value(indicator, value)
                if validation_result['is_valid']:
                    validated_indicators[indicator] = value
                else:
                    validation_warnings.append(validation_result['warning'])
        
        if not validated_indicators:
            return {
                'score': None,
                'interpretation': 'Данные не прошли валидацию',
                'indicators': {},
                'sufficient_data': False,
                'data_available': True,
                'validation_warnings': validation_warnings
            }
        
        # Расчет баллов по каждому показателю
        indicator_scores = {}
        total_score = 0
        valid_indicators = 0

        for indicator, value in validated_indicators.items():
            score = self._get_indicator_score(indicator, value)
            # Упрощенная структура: только значение
            indicator_scores[indicator] = value
            total_score += score
            valid_indicators += 1
        
        # Проверка достаточности данных
        years_tested = sort_data.get('overall_summary', {}).get('overall_min_years_tested', 0)
        sufficient_data = (valid_indicators >= self.minimum_indicators and 
                          years_tested >= self.minimum_years_tested)
        
        # Средний балл по качеству
        if valid_indicators > 0:
            avg_score = total_score / valid_indicators
            score_value = round(avg_score, 1)
        else:
            score_value = None
        
        return {
            'score': score_value,
            'interpretation': self._get_quality_interpretation(avg_score) if score_value else 'Недостаточно данных',
            'indicators': indicator_scores,
            'sufficient_data': sufficient_data,
            'data_available': True,
            'validation_warnings': validation_warnings
        }
    
    def _extract_quality_indicators(self, sort_data: Dict) -> Dict:
        """
        Извлечение показателей качества из данных сорта

        Args:
            sort_data: Данные о сорте

        Returns:
            Словарь показателей качества
        """
        quality_indicators = {}

        # Ищем показатели качества в регионах и усредняем
        regions_data = sort_data.get('regions_data', [])
        indicator_values = {}  # Словарь для накопления значений по показателям

        for region in regions_data:
            region_quality = region.get('quality_indicators', {})
            for indicator, value in region_quality.items():
                if value is not None:
                    if indicator not in indicator_values:
                        indicator_values[indicator] = []
                    indicator_values[indicator].append(value)

        # Вычисляем средние значения
        for indicator, values in indicator_values.items():
            if values:
                avg_value = sum(values) / len(values)
                quality_indicators[indicator] = round(avg_value, 1)

        # Ищем в общих данных сорта
        summary_quality = sort_data.get('summary', {}).get('quality_indicators', {})
        for indicator, value in summary_quality.items():
            if value is not None and indicator not in quality_indicators:
                quality_indicators[indicator] = value

        return quality_indicators
    
    def _validate_indicator_value(self, indicator: str, value: float) -> Dict:
        """
        Валидация значения показателя качества
        
        Args:
            indicator: Название показателя
            value: Значение показателя
            
        Returns:
            Dict с результатом валидации: {'is_valid': bool, 'warning': str}
        """
        # Проверка на отрицательные значения
        if value < 0:
            return {
                'is_valid': False,
                'warning': f'{indicator}: отрицательное значение ({value})'
            }
        
        # Проверка на выбросы (значение > 200% от excellent порога)
        if indicator in self.quality_standards:
            excellent_threshold = self.quality_standards[indicator].get('excellent', 100)
            max_reasonable = excellent_threshold * 2
            
            if value > max_reasonable:
                return {
                    'is_valid': False,
                    'warning': f'{indicator}: значение ({value}) превышает разумный максимум ({max_reasonable})'
                }
        
        return {'is_valid': True, 'warning': None}
    
    def _get_indicator_score(self, indicator: str, value: float) -> int:
        """
        Получение балла для конкретного показателя
        
        Args:
            indicator: Название показателя
            value: Значение показателя
            
        Returns:
            Балл (1-5)
        """
        if indicator not in self.quality_standards:
            return 3  # Средний балл для неизвестных показателей
        
        standards = self.quality_standards[indicator]
        
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
    
    def _get_score_interpretation(self, score: int) -> str:
        """
        Интерпретация балла показателя
        
        Args:
            score: Балл (1-5)
            
        Returns:
            Текстовая интерпретация
        """
        interpretations = {
            5: "Отличный",
            4: "Хороший",
            3: "Удовлетворительный",
            2: "Посредственный",
            1: "Плохой"
        }
        return interpretations.get(score, "Неизвестно")
    
    def _get_quality_interpretation(self, avg_score: float) -> str:
        """
        Общая интерпретация качества
        
        Args:
            avg_score: Средний балл качества
            
        Returns:
            Общая интерпретация
        """
        if avg_score >= 4.5:
            return "Отличное качество продукции"
        elif avg_score >= 3.5:
            return "Хорошее качество продукции"
        elif avg_score >= 2.5:
            return "Удовлетворительное качество"
        elif avg_score >= 1.5:
            return "Посредственное качество"
        else:
            return "Плохое качество продукции"
    
    def get_quality_requirements(self) -> Dict:
        """
        Получение требований к качеству по Методике
        
        Returns:
            Словарь требований
        """
        return {
            'minimum_requirements': {
                'protein_content': 11.0,      # Минимум для допуска
                'gluten_content': 20.0,       # Минимум для допуска
                'vitreousness': 70.0,        # Минимум для допуска
                'thousand_seed_weight': 40.0  # Минимум для допуска
            },
            'excellent_standards': {
                'protein_content': 15.0,      # Отличный уровень
                'gluten_content': 30.0,       # Отличный уровень
                'vitreousness': 90.0,        # Отличный уровень
                'thousand_seed_weight': 50.0  # Отличный уровень
            }
        }
