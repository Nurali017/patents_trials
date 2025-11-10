"""
Сервис генерации нарушений (Violations) вместо автоматических решений
"""
from django.conf import settings
from typing import Dict, List


class AlertService:
    """
    Генерация нарушений (Violations) на основе балльной оценки
    
    Заменяет логику автоматических решений (approved/rejected/continue)
    на систему оповещений о нарушениях требований Методики ГСИ
    """
    
    def __init__(self):
        self.config = settings.EVALUATION_THRESHOLDS['violations']
        self.critical_score_threshold = self.config['critical_score_threshold']
        self.minimum_years_tested = self.config['minimum_years_tested']
        self.minimum_coverage_percent = self.config['minimum_coverage_percent']
    
    def generate_violations(self, evaluation_scores: Dict, overall_summary: Dict, sort_record: Dict = None) -> List[Dict]:
        """
        Генерация списка нарушений по результатам оценки

        Args:
            evaluation_scores: Балльные оценки (yield/quality/resistance scores)
            overall_summary: Общая сводка (coverage, years_tested, etc.)
            sort_record: Данные о сорте (id, name, patents_status)

        Returns:
            List of violations: [{'code': str, 'severity': str, 'message': str, 'details': dict}]
        """
        violations = []

        # 1. Критические провалы баллов (≤2.0)
        violations.extend(self._check_critical_scores(evaluation_scores))

        # 2. Критические показатели устойчивости (<3.0 на шкале 1-10)
        violations.extend(self._check_critical_resistance(evaluation_scores))

        # 3. Недостаточность данных
        violations.extend(self._check_data_sufficiency(evaluation_scores, overall_summary))

        # 4. Покрытие и продолжительность испытаний
        violations.extend(self._check_coverage_duration(overall_summary))

        # 5. Проверка статуса сорта в Patents Service
        violations.extend(self._check_patents_status(sort_record))

        return violations
    
    def _check_critical_scores(self, evaluation_scores: Dict) -> List[Dict]:
        """
        Проверка критических провалов баллов (≤2.0)
        """
        violations = []
        
        yield_score = evaluation_scores.get('yield_score')
        quality_score = evaluation_scores.get('quality_score')
        resistance_score = evaluation_scores.get('resistance_score')
        
        if yield_score is not None and yield_score <= self.critical_score_threshold:
            violations.append({
                'code': 'CRITICAL_YIELD_FAILURE',
                'severity': 'critical',
                'message': f'Критически низкий балл урожайности: {yield_score}/5 (требуется > {self.critical_score_threshold})',
                'details': {
                    'component': 'yield',
                    'score': yield_score,
                    'threshold': self.critical_score_threshold
                }
            })
        
        if quality_score is not None and quality_score <= self.critical_score_threshold:
            violations.append({
                'code': 'CRITICAL_QUALITY_FAILURE',
                'severity': 'critical',
                'message': f'Критически низкий балл качества: {quality_score}/5 (требуется > {self.critical_score_threshold})',
                'details': {
                    'component': 'quality',
                    'score': quality_score,
                    'threshold': self.critical_score_threshold
                }
            })
        
        if resistance_score is not None and resistance_score <= self.critical_score_threshold:
            violations.append({
                'code': 'CRITICAL_RESISTANCE_SCORE_FAILURE',
                'severity': 'critical',
                'message': f'Критически низкий балл устойчивости: {resistance_score}/5 (требуется > {self.critical_score_threshold})',
                'details': {
                    'component': 'resistance',
                    'score': resistance_score,
                    'threshold': self.critical_score_threshold
                }
            })
        
        return violations
    
    def _check_critical_resistance(self, evaluation_scores: Dict) -> List[Dict]:
        """
        Проверка критических показателей устойчивости
        
        Если любой критический показатель (disease_resistance, lodging_resistance, winter_hardiness)
        имеет исходное значение < 3.0 на шкале 1-10
        """
        violations = []
        
        detailed_resistance = evaluation_scores.get('detailed_scores', {}).get('resistance', {})
        critical_failures = detailed_resistance.get('critical_failures', [])
        
        for failure in critical_failures:
            indicator = failure['indicator']
            value = failure['value']
            threshold = failure['threshold']
            
            violations.append({
                'code': 'CRITICAL_RESISTANCE_INDICATOR_FAILURE',
                'severity': 'critical',
                'message': f'Критический провал показателя устойчивости "{indicator}": {value} < {threshold} (шкала 1-10)',
                'details': {
                    'indicator': indicator,
                    'raw_value': value,
                    'threshold': threshold,
                    'scale': '1-10'
                }
            })
        
        return violations
    
    def _check_data_sufficiency(self, evaluation_scores: Dict, overall_summary: Dict) -> List[Dict]:
        """
        Проверка достаточности данных для оценки
        """
        violations = []
        
        quality_score = evaluation_scores.get('quality_score')
        resistance_score = evaluation_scores.get('resistance_score')
        
        detailed_quality = evaluation_scores.get('detailed_scores', {}).get('quality', {})
        detailed_resistance = evaluation_scores.get('detailed_scores', {}).get('resistance', {})
        
        # Проверка качества
        if quality_score is None:
            if not detailed_quality.get('data_available', False):
                violations.append({
                    'code': 'INSUFFICIENT_QUALITY_DATA',
                    'severity': 'warning',
                    'message': 'Отсутствуют данные по показателям качества',
                    'details': {
                        'component': 'quality',
                        'reason': 'no_data_available'
                    }
                })
            elif not detailed_quality.get('sufficient_data', False):
                years_tested = overall_summary.get('overall_min_years_tested', 0)
                violations.append({
                    'code': 'INSUFFICIENT_QUALITY_DATA',
                    'severity': 'warning',
                    'message': f'Недостаточно данных по качеству (годы: {years_tested}, требуется ≥ {self.minimum_years_tested})',
                    'details': {
                        'component': 'quality',
                        'years_tested': years_tested,
                        'minimum_years_required': self.minimum_years_tested,
                        'reason': 'insufficient_years_or_indicators'
                    }
                })
        
        # Проверка устойчивости
        if resistance_score is None:
            if not detailed_resistance.get('data_available', False):
                violations.append({
                    'code': 'INSUFFICIENT_RESISTANCE_DATA',
                    'severity': 'warning',
                    'message': 'Отсутствуют данные по показателям устойчивости',
                    'details': {
                        'component': 'resistance',
                        'reason': 'no_data_available'
                    }
                })
            elif not detailed_resistance.get('sufficient_data', False):
                years_tested = overall_summary.get('overall_min_years_tested', 0)
                violations.append({
                    'code': 'INSUFFICIENT_RESISTANCE_DATA',
                    'severity': 'warning',
                    'message': f'Недостаточно данных по устойчивости (годы: {years_tested}, требуется ≥ {self.minimum_years_tested})',
                    'details': {
                        'component': 'resistance',
                        'years_tested': years_tested,
                        'minimum_years_required': self.minimum_years_tested,
                        'reason': 'insufficient_years_or_indicators'
                    }
                })
        
        return violations
    
    def _check_coverage_duration(self, overall_summary: Dict) -> List[Dict]:
        """
        Проверка покрытия ГСУ и продолжительности испытаний
        """
        violations = []
        
        coverage_percent = overall_summary.get('overall_coverage_percent', 0)
        years_tested = overall_summary.get('overall_min_years_tested', 0)
        
        # Проверка покрытия
        if coverage_percent < self.minimum_coverage_percent:
            violations.append({
                'code': 'INSUFFICIENT_COVERAGE',
                'severity': 'high',
                'message': f'Недостаточное покрытие ГСУ: {coverage_percent:.1f}% (требуется ≥ {self.minimum_coverage_percent}%)',
                'details': {
                    'current_coverage': round(coverage_percent, 1),
                    'required_coverage': self.minimum_coverage_percent,
                    'gsu_tested': overall_summary.get('gsu_tested_total', 0),
                    'gsu_total': overall_summary.get('gsu_total', 0)
                }
            })
        
        # Проверка продолжительности
        if years_tested < self.minimum_years_tested:
            violations.append({
                'code': 'INSUFFICIENT_DURATION',
                'severity': 'high',
                'message': f'Недостаточная продолжительность испытаний: {years_tested} лет (требуется ≥ {self.minimum_years_tested})',
                'details': {
                    'years_tested': years_tested,
                    'minimum_years_required': self.minimum_years_tested
                }
            })

        return violations

    def _check_patents_status(self, sort_record: Dict) -> List[Dict]:
        """
        Проверка статуса сорта в Patents Service

        Сорт должен быть в основном реестре (patents_status = 1)

        Args:
            sort_record: Данные о сорте (id, name, patents_status)

        Returns:
            List of violations (включая info-уровень для валидных статусов)
        """
        violations = []

        if not sort_record:
            return violations

        patents_status = sort_record.get('patents_status')
        sort_name = sort_record.get('name', 'Неизвестный сорт')

        if patents_status == 1:
            # Статус MAIN (Основной реестр) - всё ОК, нет violations
            pass
        elif patents_status == 2:
            # Статус TESTING - предупреждение
            violations.append({
                'code': 'TESTING_PATENTS_STATUS',
                'severity': 'warning',
                'message': 'Сорт находится на стадии испытаний (TESTING)',
                'details': {
                    'sort_name': sort_name,
                    'current_status': patents_status,
                    'status_display': 'TESTING (Испытания)'
                }
            })
        elif patents_status == 3:
            # Статус ARCHIVE - предупреждение
            violations.append({
                'code': 'ARCHIVE_PATENTS_STATUS',
                'severity': 'warning',
                'message': 'Сорт находится в архиве (ARCHIVE)',
                'details': {
                    'sort_name': sort_name,
                    'current_status': patents_status,
                    'status_display': 'ARCHIVE (Архив)'
                }
            })
        elif patents_status is None:
            # Статус не определен - предупреждение
            violations.append({
                'code': 'UNKNOWN_PATENTS_STATUS',
                'severity': 'warning',
                'message': 'Статус сорта в реестре ООС не определен',
                'details': {
                    'sort_name': sort_name,
                    'current_status': None,
                    'status_display': 'Не определен'
                }
            })
        else:
            # Неизвестный статус - предупреждение
            violations.append({
                'code': 'INVALID_PATENTS_STATUS',
                'severity': 'warning',
                'message': f'Неизвестный статус сорта в реестре ООС: {patents_status}',
                'details': {
                    'sort_name': sort_name,
                    'current_status': patents_status,
                    'status_display': f'Неизвестный статус ({patents_status})'
                }
            })

        return violations

