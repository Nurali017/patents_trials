"""
Annual Report ViewSets
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import (
    RequestValidatorService,
    MethodologyTableService,
    MethodologySummaryService
)


class AnnualReportViewSet(viewsets.ViewSet):
    """
    API для годовых отчетов по сортоиспытаниям

    Endpoints:
    - GET /api/annual-reports/methodology-table/ - получить таблицу по методике сортоиспытаний
    - GET /api/annual-reports/methodology-summary/ - получить summary/рекомендации для сортов
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Базовый endpoint (не используется)
        Возвращает список доступных endpoints
        """
        return Response({
            'message': 'Annual Reports API',
            'available_endpoints': {
                'methodology_table': '/api/annual-reports/methodology-table/?year=2025&oblast_id=17&patents_culture_id=5',
                'methodology_summary': '/api/annual-reports/methodology-summary/?year=2025&oblast_id=17&patents_culture_id=5',
                'evaluation_settings': '/api/annual-reports/evaluation-settings/'
            }
        })

    @action(detail=False, methods=['get'])
    def methodology_table(self, request):
        """
        Получить таблицу по методике сортоиспытаний (без рекомендаций)

        GET /api/annual-reports/methodology-table/?year=2025&oblast_id=17&patents_culture_id=720

        Query Parameters:
        - year (required): Год отчета
        - oblast_id (required): ID области
        - patents_culture_id (optional): ID культуры из Patents для фильтрации

        Returns: Таблица с группировкой по регионам и группам спелости
        """
        # Валидация параметров
        oblast, year_int, patents_culture_id_int, error = RequestValidatorService.validate_report_params(request)
        if error:
            return error

        # Генерация таблицы через сервис
        table_service = MethodologyTableService()
        methodology_data = table_service.generate_table(oblast, year_int, patents_culture_id_int)

        return Response(methodology_data)

    @action(detail=False, methods=['get'])
    def methodology_summary(self, request):
        """
        Получить summary/рекомендации для таблицы по методике сортоиспытаний

        GET /api/annual-reports/methodology-summary/?year=2025&oblast_id=17&patents_culture_id=720

        Query Parameters:
        - year (required): Год отчета
        - oblast_id (required): ID области
        - patents_culture_id (optional): ID культуры из Patents для фильтрации

        Returns: Рекомендации и оценки для сортов с привязкой к application_number
        """
        # Валидация параметров
        oblast, year_int, patents_culture_id_int, error = RequestValidatorService.validate_report_params(request)
        if error:
            return error

        # Генерация рекомендаций через сервис
        summary_service = MethodologySummaryService()
        summary_data = summary_service.generate_recommendations(oblast, year_int, patents_culture_id_int)

        return Response(summary_data)

    @action(detail=False, methods=['get'], url_path='evaluation-settings', permission_classes=[])
    def evaluation_settings(self, request):
        """
        Получить нормы и пороговые значения для оценки сортов

        GET /api/annual-reports/evaluation-settings/

        Returns: Конфигурация норм для балльной оценки (quality, resistance, yield, violations)
        """
        from django.conf import settings

        evaluation_settings = settings.EVALUATION_THRESHOLDS

        return Response({
            'evaluation_thresholds': evaluation_settings,
            'description': {
                'quality': 'Пороговые значения для показателей качества (белок, клейковина, стекловидность и др.)',
                'resistance': 'Пороговые значения для показателей устойчивости (болезни, полегание, зимостойкость и др.)',
                'yield': 'Пороговые значения для оценки урожайности и статистической значимости',
                'violations': 'Критические пороги для генерации нарушений'
            },
            'score_scale': {
                'yield_score': '1-5 баллов (1 - очень низкая урожайность, 5 - очень высокая)',
                'quality_score': '1-5 баллов (1 - очень низкое качество, 5 - отличное качество)',
                'resistance_score': '1-5 баллов (1 - очень низкая устойчивость, 5 - очень высокая)'
            }
        })
