"""
Сервисы для годового отчета
"""
from .basic_report_service import BasicReportService
from .statistics_service import StatisticsService
from .summary_service import SummaryService
from .request_validator_service import RequestValidatorService
from .culture_filter_service import CultureFilterService
from .quality_indicators_service import QualityIndicatorsService
from .methodology_table_service import MethodologyTableService
from .methodology_summary_service import MethodologySummaryService

__all__ = [
    'BasicReportService',
    'StatisticsService',
    'SummaryService',
    'RequestValidatorService',
    'CultureFilterService',
    'QualityIndicatorsService',
    'MethodologyTableService',
    'MethodologySummaryService'
]
