"""
Сервисы для годового отчета
"""
from .basic_report_service import BasicReportService
from .statistics_service import StatisticsService
from .summary_service import SummaryService

__all__ = [
    'BasicReportService',
    'StatisticsService', 
    'SummaryService'
]
