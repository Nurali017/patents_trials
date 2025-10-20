"""
Оценка качества продукции по Методике ГСИ
"""
from typing import Dict, List, Optional


class QualityEvaluator:
    """
    Оценка качества зерна и продукции
    """
    
    def __init__(self):
        # Критерии качества по Методике ГСИ
        self.quality_standards = {
            'protein_content': {
                'excellent': 15.0,      # 5 баллов
                'good': 13.0,          # 4 балла  
                'satisfactory': 11.0,  # 3 балла
                'poor': 9.0            # 2 балла
            },
            'gluten_content': {
                'excellent': 30.0,
                'good': 25.0,
                'satisfactory': 20.0,
                'poor': 15.0
            },
            'vitreousness': {
                'excellent': 90.0,
                'good': 80.0,
                'satisfactory': 70.0,
                'poor': 60.0
            },
            'thousand_seed_weight': {
                'excellent': 50.0,
                'good': 45.0,
                'satisfactory': 40.0,
                'poor': 35.0
            }
        }
    
    def calculate_quality_score(self, sort_data: Dict) -> Dict:
        """
        Расчет балла по качеству продукции
        
        Args:
            sort_data: Данные о сорте
            
        Returns:
            Балл и детали по качеству
        """
        # Получаем показатели качества
        quality_indicators = self._extract_quality_indicators(sort_data)
        
        if not quality_indicators:
            return {
                'score': None,  # Явно указываем отсутствие данных
                'interpretation': 'Данные по качеству отсутствуют',
                'indicators': {},
                'sufficient_data': False,
                'data_available': False
            }
        
        # Расчет баллов по каждому показателю
        indicator_scores = {}
        total_score = 0
        valid_indicators = 0
        
        for indicator, value in quality_indicators.items():
            if value is not None:
                score = self._get_indicator_score(indicator, value)
                indicator_scores[indicator] = {
                    'value': value,
                    'score': score,
                    'interpretation': self._get_score_interpretation(score)
                }
                total_score += score
                valid_indicators += 1
        
        # Средний балл по качеству
        avg_score = total_score / valid_indicators if valid_indicators > 0 else 3
        
        return {
            'score': round(avg_score, 1),
            'interpretation': self._get_quality_interpretation(avg_score),
            'indicators': indicator_scores,
            'sufficient_data': valid_indicators >= 2  # Минимум 2 показателя
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
        
        # Ищем показатели качества в регионах
        regions_data = sort_data.get('regions_data', [])
        for region in regions_data:
            region_quality = region.get('quality_indicators', {})
            for indicator, value in region_quality.items():
                if value is not None and indicator not in quality_indicators:
                    quality_indicators[indicator] = value
        
        # Ищем в общих данных сорта
        summary_quality = sort_data.get('summary', {}).get('quality_indicators', {})
        for indicator, value in summary_quality.items():
            if value is not None and indicator not in quality_indicators:
                quality_indicators[indicator] = value
        
        return quality_indicators
    
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
