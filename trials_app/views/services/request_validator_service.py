"""
Сервис для валидации параметров запросов годовых отчетов
"""
from rest_framework import status
from rest_framework.response import Response
from ...models import Oblast


class RequestValidatorService:
    """
    Сервис для валидации параметров запросов

    Предоставляет методы валидации:
    - Валидация года и области
    - Валидация ID культуры
    - Общая валидация параметров отчета
    """

    @staticmethod
    def validate_report_params(request):
        """
        Валидация параметров для генерации отчета

        Args:
            request: HTTP запрос с параметрами year, oblast_id, patents_culture_id

        Returns:
            tuple: (oblast, year_int, patents_culture_id_int, error_response)
            - Если валидация успешна: (oblast, year, culture_id, None)
            - Если ошибка: (None, None, None, Response с ошибкой)
        """
        year = request.query_params.get('year')
        oblast_id = request.query_params.get('oblast_id')
        patents_culture_id = request.query_params.get('patents_culture_id')

        # Проверка обязательных параметров
        if not year or not oblast_id:
            return None, None, None, Response({
                'success': False,
                'error': 'year and oblast_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Валидация года
        try:
            year_int = int(year)
        except ValueError:
            return None, None, None, Response({
                'success': False,
                'error': 'Invalid year format'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Валидация области
        try:
            oblast = Oblast.objects.get(id=oblast_id)
        except Oblast.DoesNotExist:
            return None, None, None, Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Валидация ID культуры (опционально)
        patents_culture_id_int = None
        if patents_culture_id:
            try:
                patents_culture_id_int = int(patents_culture_id)
            except ValueError:
                return None, None, None, Response({
                    'success': False,
                    'error': 'Invalid patents_culture_id format'
                }, status=status.HTTP_400_BAD_REQUEST)

        return oblast, year_int, patents_culture_id_int, None

    @staticmethod
    def validate_oblast_and_year(oblast_id, year):
        """
        Простая валидация области и года

        Args:
            oblast_id: ID области
            year: Год отчета (строка или число)

        Returns:
            tuple: (oblast, year_int, error_response)
        """
        try:
            oblast = Oblast.objects.get(id=oblast_id)
            year_int = int(year)
            return oblast, year_int, None
        except Oblast.DoesNotExist:
            return None, None, Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return None, None, Response({
                'success': False,
                'error': 'Invalid year format'
            }, status=status.HTTP_400_BAD_REQUEST)
