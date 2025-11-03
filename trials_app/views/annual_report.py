"""
Annual Report ViewSets
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from ..models import Oblast
from .services import BasicReportService, StatisticsService, SummaryService


class AnnualReportViewSet(viewsets.ViewSet):
    """
    API для годовых отчетов по сортоиспытаниям
    
    Endpoints:
    - GET /api/annual-reports/ - получить основной годовой отчет (базовые данные)
    - GET /api/annual-reports/statistics/ - получить статистику по решениям
    - GET /api/annual-reports/summary/ - получить сводные данные для принятия решений
    - GET /api/annual-reports/methodology-table/ - получить таблицу по методике сортоиспытаний
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        Получить основной годовой отчет (базовые данные)
        
        GET /api/annual-reports/?year=2024&oblast_id=17
        
        Returns: Основной отчет с детальными данными по сортам и стандартам
        """
        year = request.query_params.get('year')
        oblast_id = request.query_params.get('oblast_id')
        
        if not year or not oblast_id:
            return Response({
                'success': False,
                'error': 'year and oblast_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            oblast = Oblast.objects.get(id=oblast_id)
            year_int = int(year)
        except Oblast.DoesNotExist:
            return Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'success': False,
                'error': 'Invalid year format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Сгенерировать отчет
        report_data = self._generate_annual_report(oblast, year_int)
        
        return Response(report_data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Получить статистику по решениям
        
        GET /api/annual-reports/statistics/?year=2024&oblast_id=17
        
        Returns: Статистика по решениям
        """
        year = request.query_params.get('year')
        oblast_id = request.query_params.get('oblast_id')
        
        if not year or not oblast_id:
            return Response({
                'success': False,
                'error': 'year and oblast_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            oblast = Oblast.objects.get(id=oblast_id)
            year_int = int(year)
        except Oblast.DoesNotExist:
            return Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'success': False,
                'error': 'Invalid year format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Получить статистику
        statistics_service = StatisticsService()
        statistics = statistics_service.get_statistics_by_oblast(oblast, year_int)
        
        return Response(statistics)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Получить сводные данные
        
        GET /api/annual-reports/summary/?year=2024&oblast_id=17
        
        Returns: Сводные данные по сортам
        """
        year = request.query_params.get('year')
        oblast_id = request.query_params.get('oblast_id')
        
        if not year or not oblast_id:
            return Response({
                'success': False,
                'error': 'year and oblast_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            oblast = Oblast.objects.get(id=oblast_id)
            year_int = int(year)
        except Oblast.DoesNotExist:
            return Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'success': False,
                'error': 'Invalid year format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Получить основные данные для сводки
        basic_service = BasicReportService()
        basic_data = basic_service.generate_basic_report(oblast, year_int)
        
        # Получить сводные данные
        summary_service = SummaryService()
        summary_items = summary_service.generate_summary_items(oblast, year_int, basic_data['detailed_items'])
        
        return Response({
            'oblast': basic_data['oblast'],
            'year': basic_data['year'],
            'summary_items': summary_items
        })
    
    @action(detail=False, methods=['get'])
    def methodology_table(self, request):
        """
        Получить таблицу по методике сортоиспытаний

        GET /api/annual-reports/methodology-table/?year=2025&oblast_id=17&patents_culture_id=720

        Query Parameters:
        - year (required): Год отчета
        - oblast_id (required): ID области
        - patents_culture_id (optional): ID культуры из Patents для фильтрации

        Returns: Таблица с группировкой по регионам и группам спелости
        """
        year = request.query_params.get('year')
        oblast_id = request.query_params.get('oblast_id')
        patents_culture_id = request.query_params.get('patents_culture_id')  # Опциональный параметр

        if not year or not oblast_id:
            return Response({
                'success': False,
                'error': 'year and oblast_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            oblast = Oblast.objects.get(id=oblast_id)
            year_int = int(year)

            # Валидация patents_culture_id (если указан)
            patents_culture_id_int = None
            if patents_culture_id:
                try:
                    patents_culture_id_int = int(patents_culture_id)
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Invalid patents_culture_id format'
                    }, status=status.HTTP_400_BAD_REQUEST)

        except Oblast.DoesNotExist:
            return Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'success': False,
                'error': 'Invalid year format'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Получить данные для таблицы по методике с фильтрацией по культуре
        methodology_data = self._generate_methodology_table(oblast, year_int, patents_culture_id_int)

        # Добавить рекомендации из SummaryService
        methodology_data = self._add_summary_recommendations(methodology_data, oblast, year_int)

        return Response(methodology_data)
    
    def _generate_methodology_table(self, oblast, year, patents_culture_id=None):
        """
        Генерация таблицы по методике сортоиспытаний

        Args:
            oblast: Объект области
            year: Год отчета
            patents_culture_id: ID культуры из Patents для фильтрации (опционально)

        Структура:
        - Группировка по регионам
        - Внутри региона группировка по группам спелости
        - Для каждой группы сорта с показателями качества
        """
        from collections import defaultdict

        # Получаем базовые данные
        basic_service = BasicReportService()
        basic_data = basic_service.generate_basic_report(oblast, year)

        # Фильтрация по культуре (если указан patents_culture_id)
        if patents_culture_id is not None:
            filtered_items = []
            for item in basic_data['detailed_items']:
                # Проверяем culture_id через sort_record
                if (item.get('sort_record', {}).get('culture_id') == patents_culture_id or
                    item.get('culture', {}).get('culture_id') == patents_culture_id):
                    filtered_items.append(item)
            basic_data['detailed_items'] = filtered_items

        # Группируем данные: регион -> группа спелости -> сорта
        regions_groups = defaultdict(lambda: defaultdict(list))

        for item in basic_data['detailed_items']:
            # Все сорта в конкретных регионах (включая стандарты и испытываемые)
            if item.get('region', {}).get('id'):
                region_name = item['region']['name']
                group_code = item['maturity_group_code']
                regions_groups[region_name][group_code].append(item)
        
        # Сначала формируем standards_by_group
        standards_by_group = defaultdict(list)
        for item in basic_data['detailed_items']:
            if item['is_standard']:
                group_code = item['maturity_group_code']
                standards_by_group[group_code].append({
                    'sort_name': item['sort_record']['name'],
                    'average_yield': item['trial_data']['average_yield'],
                    'is_comparison_standard': item['is_comparison_standard'],
                    'region': item['region']['name']
                })
        
        # Получить название культуры (если фильтр применен)
        culture_filter_info = None
        if patents_culture_id is not None:
            from trials_app.models import Culture
            try:
                culture = Culture.objects.get(culture_id=patents_culture_id, is_deleted=False)
                culture_filter_info = {
                    'patents_culture_id': patents_culture_id,
                    'culture_name': culture.name
                }
            except Culture.DoesNotExist:
                culture_filter_info = {
                    'patents_culture_id': patents_culture_id,
                    'culture_name': f'Culture ID {patents_culture_id}'
                }

        # Формируем структуру таблицы
        methodology_table = {
            'oblast': basic_data['oblast'],
            'year': basic_data['year'],
            'years_range': basic_data['years_range'],
            'generated_at': basic_data['generated_at'],
            'regions': basic_data['regions'],
            'methodology_table': {},
            'standards_by_group': dict(standards_by_group),
            'quality_indicators': self._get_quality_indicators(),
            'warnings': basic_data['warnings'],
            'has_warnings': basic_data['has_warnings'],
            'culture_filter': culture_filter_info  # Информация о примененном фильтре
        }
        
        # Заполняем таблицу по регионам и группам
        for region_name, groups in regions_groups.items():
            methodology_table['methodology_table'][region_name] = {}
            
            for group_code, sorts in groups.items():
                # Формируем данные сортов в группе
                group_data = {
                    'group_code': group_code,
                    'group_name': sorts[0]['maturity_group_name'] if sorts else '',
                    'sorts': []
                }
                
                # Добавляем сорта в группу
                for sort_item in sorts:
                    # Добавляем год в данные сорта для получения качественных показателей
                    sort_item_with_year = sort_item.copy()
                    sort_item_with_year['year'] = year
                    
                    # Определяем, является ли сорт стандартом для данной группы
                    sort_name = sort_item['sort_record']['name']
                    is_sort_standard = sort_item.get('is_standard', False)
                    
                    # Если сорт не помечен как стандарт, проверяем в standards_by_group
                    if not is_sort_standard:
                        # Проверяем, есть ли этот сорт в стандартах группы
                        if group_code in methodology_table.get('standards_by_group', {}):
                            for std in methodology_table['standards_by_group'][group_code]:
                                if std['sort_name'] == sort_name:
                                    is_sort_standard = True
                                    break
                    
                    # Определяем is_comparison_standard из standards_by_group
                    is_comparison_standard = sort_item.get('is_comparison_standard', False)
                    if group_code in methodology_table.get('standards_by_group', {}):
                        for std in methodology_table['standards_by_group'][group_code]:
                            if std['sort_name'] == sort_name:
                                is_comparison_standard = std['is_comparison_standard']
                                break
                    
                    # Для стандартов deviation_percent должен быть пустой строкой
                    deviation_percent = sort_item['trial_data'].get('deviation_percent')
                    if is_sort_standard:
                        deviation_percent = ""
                    elif deviation_percent is None:
                        deviation_percent = None
                    
                    sort_data = {
                        'sort_name': sort_item['sort_record']['name'],
                        'application_number': sort_item['application_number'],
                        'is_standard': is_sort_standard,
                        'is_comparison_standard': is_comparison_standard,
                        'yields_by_year': sort_item['trial_data']['yields_by_year'],
                        'average_yield': sort_item['trial_data']['average_yield'],
                        'deviation_percent': deviation_percent,
                        'years_tested': sort_item['trial_data']['years_tested'],
                        'year_started': sort_item['trial_data']['year_started'],
                        'main_indicators': self._get_sort_main_indicators(sort_item_with_year),
                        'quality_indicators': self._get_sort_quality_indicators(sort_item_with_year),
                        'decision_status': sort_item.get('decision_status'),
                        'latest_decision': sort_item.get('latest_decision')
                    }
                    group_data['sorts'].append(sort_data)
                
                methodology_table['methodology_table'][region_name][group_code] = group_data
        
        
        return methodology_table
    
    def _get_standard_for_group(self, group_code, detailed_items):
        """Получить стандарт для группы спелости"""
        for item in detailed_items:
            if (item['is_standard'] and 
                item['maturity_group_code'] == group_code and 
                item['is_comparison_standard']):
                return {
                    'sort_name': item['sort_record']['name'],
                    'average_yield': item['trial_data']['average_yield'],
                    'yields_by_year': item['trial_data']['yields_by_year']
                }
        return None
    
    def _get_quality_indicators(self):
        """Получить список показателей качества из базы данных"""
        from trials_app.models import Indicator
        
        quality_indicators = Indicator.objects.filter(is_quality=True).order_by('sort_order', 'name')
        
        indicators_dict = {}
        for indicator in quality_indicators:
            indicators_dict[indicator.code] = {
                'name': indicator.name,
                'unit': indicator.unit,
                'description': indicator.description
            }
        
        return indicators_dict
    
    def _get_sort_quality_indicators(self, sort_item):
        """
        Получить показатели качества для конкретного сорта из TrialLaboratoryResult
        """
        from trials_app.models import TrialLaboratoryResult, Indicator, TrialParticipant
        
        sort_record_id = sort_item['sort_record']['id']
        region_id = sort_item['region']['id']
        
        # Если нет region_id (стандарт), пропускаем
        if not region_id:
            return {}
        
        # Получаем trial_id через TrialParticipant для данного сорта в регионе
        # Только за текущий год отчета
        year = sort_item.get('year', 2025)
        
        participants = TrialParticipant.objects.filter(
            sort_record_id=sort_record_id,
            trial__region_id=region_id,
            trial__year=year,
            is_deleted=False
        ).values_list('trial_id', flat=True)
        
        if not participants:
            return {}
        
        # Получаем лабораторные результаты для найденных trials
        lab_results = TrialLaboratoryResult.objects.filter(
            trial_id__in=participants,
            participant__sort_record_id=sort_record_id
        ).select_related('indicator')
        
        quality_data = {}
        for result in lab_results:
            # Передаем только показатели с реальными значениями (не null)
            if result.value is not None:
                indicator_code = result.indicator.code
                quality_data[indicator_code] = {
                    'value': result.value,
                    'unit': result.indicator.unit,
                    'name': result.indicator.name
                }
        
        return quality_data
    
    def _get_sort_main_indicators(self, sort_item):
        """
        Получить основные показатели для конкретного сорта из TrialResult
        Только за текущий год отчета
        """
        from trials_app.models import TrialResult, TrialParticipant
        
        sort_record_id = sort_item['sort_record']['id']
        region_id = sort_item['region']['id']
        
        # Если нет region_id (стандарт), пропускаем
        if not region_id:
            return {}
        
        # Получаем trial_id через TrialParticipant для данного сорта в регионе
        # Только за текущий год отчета
        year = sort_item.get('year', 2025)
        
        participants = TrialParticipant.objects.filter(
            sort_record_id=sort_record_id,
            trial__region_id=region_id,
            trial__year=year,
            is_deleted=False
        ).values_list('trial_id', flat=True)
        
        if not participants:
            return {}
        
        # Получаем основные результаты для найденных trials
        # Исключаем показатели качества (is_quality=True) и урожайность (yield)
        main_results = TrialResult.objects.filter(
            trial_id__in=participants,
            participant__sort_record_id=sort_record_id,
            indicator__is_quality=False,  # Только основные показатели
            indicator__code__in=['plant_height', 'vegetation_period', 'thousand_seed_weight', 'emergence_completeness', 'lodging_resistance', 'drought_resistance', 'germination_resistance', 'tillering', 'grain_output', 'shedding_resistance'],  # Только нужные показатели
            is_deleted=False
        ).select_related('indicator')
        
        main_data = {}
        for result in main_results:
            # Передаем только показатели с реальными значениями (не null)
            if result.value is not None:
                indicator_code = result.indicator.code
                main_data[indicator_code] = {
                    'value': result.value,
                    'unit': result.indicator.unit,
                    'name': result.indicator.name,
                    'description': result.indicator.description
                }
        
        return main_data
    
    def _generate_annual_report(self, oblast, year):
        """
        Генерация основного годового отчета
        
        Возвращает только базовые данные:
        - Основная информация об области и годах
        - Список регионов (ГСУ)
        - Детальные данные по сортам и стандартам
        - Предупреждения
        """
        # Основная информация и детальные данные
        basic_service = BasicReportService()
        basic_data = basic_service.generate_basic_report(oblast, year)
        
        return {
            # Основная информация и детальные данные
            'oblast': basic_data['oblast'],
            'year': basic_data['year'],
            'years_range': basic_data['years_range'],
            'generated_at': basic_data['generated_at'],
            'regions': basic_data['regions'],
            'detailed_items': basic_data['detailed_items'],
            'warnings': basic_data['warnings'],
            'has_warnings': basic_data['has_warnings']
        }
    
    def _add_summary_recommendations(self, methodology_data, oblast, year):
        """
        Добавить рекомендации из SummaryService в methodology_table
        
        Args:
            methodology_data: Данные таблицы по методике
            oblast: Область
            year: Год
            
        Returns:
            Обновленные данные с рекомендациями
        """
        from .services import SummaryService, BasicReportService
        
        # Получить базовые данные для SummaryService
        basic_service = BasicReportService()
        basic_data = basic_service.generate_basic_report(oblast, year)
        
        # Получить рекомендации из SummaryService
        summary_service = SummaryService()
        summary_items = summary_service.generate_summary_items(oblast, year, basic_data['detailed_items'])
        
        # Создать словарь рекомендаций по application_id
        recommendations_map = {}
        for item in summary_items:
            recommendations_map[item['application_id']] = {
                'statistical_analysis': item.get('statistical_analysis', {}),
                'evaluation_scores': item.get('evaluation_scores', {}),
                'recommendation': item.get('recommendation', {}),
                'summary': item.get('summary', {})
            }
        
        # Добавить рекомендации к каждому сорту в methodology_table
        for region_name, groups in methodology_data['methodology_table'].items():
            for group_code, group_data in groups.items():
                for sort_data in group_data['sorts']:
                    # Найти рекомендации для данного сорта
                    application_number = sort_data.get('application_number')
                    if application_number:
                        # Найти application_id по номеру заявки
                        for item in basic_data['detailed_items']:
                            if (item.get('application_number') == application_number and 
                                not item.get('is_standard', False)):
                                app_id = item.get('application_id')
                                if app_id and app_id in recommendations_map:
                                    sort_data['recommendations'] = recommendations_map[app_id]
                                    break
        
        return methodology_data