"""
Application ViewSets
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models as django_models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from ..models import (
    Oblast, Region, ClimateZone, Indicator, GroupCulture, Culture,
    Originator, SortRecord, Application, ApplicationDecisionHistory,
    PlannedDistribution, TrialType, Trial, TrialParticipant, TrialResult,
    TrialLaboratoryResult, Document, TrialPlan, TrialPlanParticipant,
    TrialPlanTrial, TrialPlanCulture, TrialPlanCultureTrialType
)
from ..serializers import (
    OblastSerializer, RegionSerializer, ClimateZoneSerializer,
    IndicatorSerializer, GroupCultureSerializer, CultureSerializer,
    OriginatorSerializer, SortRecordSerializer, ApplicationSerializer,
    TrialTypeSerializer, TrialSerializer, TrialParticipantSerializer,
    TrialResultSerializer, TrialLaboratoryResultSerializer,
    DocumentSerializer, TrialPlanSerializer, TrialPlanWriteSerializer,
    TrialPlanAddParticipantsSerializer, TrialPlanCultureSerializer,
    TrialPlanAddCultureSerializer, create_basic_trial_results,
    create_quality_trial_results
)
from ..filters import ApplicationFilter
from ..patents_integration import patents_api


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Управление заявками на сортоиспытания
    
    Заявка → Распределение по областям → Испытания → Решения → Реестр
    
    Поддерживает расширенную фильтрацию и пагинацию:
    - Фильтрация по группе культур (culture_group) - локальный ID группы культур
    - Фильтрация по названию группы культур (culture_group_name) - поиск по названию
    - Фильтрация по культуре (culture) - локальный ID культуры  
    - Фильтрация по культуре из Patents Service (patents_culture_id) - ID культуры в Patents Service
    - Фильтрация по группе культур из Patents Service (patents_group_id) - ID группы культур в Patents Service
    - Фильтрация по статусу (status)
    - Фильтрация по области (oblast) - ID области
    - Фильтрация по году подачи заявки (year)
    - Поиск по номеру заявки или названию сорта (search)
    - Поиск по группе культур (group_search) - поиск по названию или коду группы
    - Пагинация с настраиваемым размером страницы
    
    Примеры использования:
    - GET /api/applications/?patents_culture_id=720&page=1&page_size=20
    - GET /api/applications/?patents_group_id=1&search=пшеница
    - GET /api/applications/?status=submitted&patents_culture_id=749
    - GET /api/applications/?culture_group_name=зерновые
    - GET /api/applications/?group_search=пшеница&year=2025
    - GET /api/applications/?oblast=1&culture_group=2
    - GET /api/applications/?patents_group_id=1&patents_culture_id=720
    """
    queryset = Application.objects.filter(is_deleted=False).select_related(
        'sort_record__culture__group_culture'
    ).prefetch_related('target_oblasts')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Требуется авторизация
    
    # Фильтрация
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter
    
    # Пагинация
    pagination_class = PageNumberPagination
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def perform_create(self, serializer):
        """При создании заявки устанавливаем created_by"""
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
    
    @action(detail=True, methods=['post'], url_path='distribute')
    def distribute(self, request, pk=None):
        """
        Распределить заявку по ГСУ
        
        Сохраняет параметры распределения в Application.
        Trial создается ВРУЧНУЮ сортопытом позже!
        
        POST /api/v1/applications/{id}/distribute/
        Body: {
            "distributions": [
                {
                    "region": 1,                    # ID ГСУ (обязательно)
                    "trial_type": "competitive",    # Код типа испытания
                    "planting_season": "spring"     # Опционально
                }
            ]
        }
        """
        application = self.get_object()
        
        if application.status not in ['draft', 'submitted']:
            return Response({
                'error': 'Application already distributed'
            }, status=400)
        
        distributions = request.data.get('distributions', [])
        if not distributions:
            return Response({
                'error': 'No distributions provided'
            }, status=400)
        
        # Валидация параметров
        validated_distributions = []
        for dist in distributions:
            # Проверка ГСУ
            try:
                region = Region.objects.get(id=dist['region'])
            except Region.DoesNotExist:
                return Response({
                    'error': f'Region with ID {dist["region"]} not found'
                }, status=400)
            
            # ПРОВЕРКА: ГСУ должен быть в одной из целевых областей
            target_oblast_ids = application.target_oblasts.values_list('id', flat=True)
            if region.oblast_id not in target_oblast_ids:
                return Response({
                    'error': f'Region "{region.name}" is not in target oblasts. '
                            f'Application targets: {", ".join(application.target_oblasts.values_list("name", flat=True))}'
                }, status=400)
            
            # Проверка типа испытания
            trial_type_obj = None
            if 'trial_type' in dist:
                try:
                    trial_type_obj = TrialType.objects.get(code=dist['trial_type'])
                except TrialType.DoesNotExist:
                    return Response({
                        'error': f'Trial type "{dist["trial_type"]}" not found'
                    }, status=400)
            
            validated_distributions.append({
                'region': region,
                'trial_type': trial_type_obj,
                'planting_season': dist.get('planting_season'),
                'raw_data': dist  # Сохраняем оригинальные данные для JSON
            })
        
        # Удаляем старые распределения (если переделывают)
        PlannedDistribution.objects.filter(application=application).delete()
        
        # Создаем записи в таблице PlannedDistribution
        created_distributions = []
        for validated in validated_distributions:
            planned_dist = PlannedDistribution.objects.create(
                application=application,
                region=validated['region'],
                trial_type=validated['trial_type'],
                planting_season=validated['planting_season'],
                created_by=request.user
            )
            created_distributions.append(planned_dist)
        
        # Обновляем статус заявки
        application.status = 'distributed'
        application.save()
        
        return Response({
            'success': True,
            'message': f'Application distributed with {len(distributions)} planned trial(s)',
            'planned_distributions': distributions,
            'application': ApplicationSerializer(application).data
        })
    
    @action(detail=True, methods=['get'], url_path='regional-trials')
    def regional_trials(self, request, pk=None):
        """
        Получить все испытания для заявки
        
        GET /api/v1/applications/{id}/regional-trials/
        
        Находит испытания через TrialParticipant, где application=данная заявка
        """
        application = self.get_object()
        
        # Найти все уникальные испытания через участников этой заявки
        from trials_app.models import TrialParticipant
        trial_ids = TrialParticipant.objects.filter(
            application=application,
            is_deleted=False
        ).values_list('trial_id', flat=True).distinct()
        
        trials = Trial.objects.filter(
            id__in=trial_ids,
            is_deleted=False
        )
        
        serializer = TrialSerializer(trials, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='decisions')
    def decisions(self, request, pk=None):
        """
        Получить все решения по испытаниям заявки
        
        GET /api/v1/applications/{id}/decisions/
        """
        application = self.get_object()
        
        # Найти все уникальные испытания через участников этой заявки
        from trials_app.models import TrialParticipant
        trial_ids = TrialParticipant.objects.filter(
            application=application,
            is_deleted=False
        ).values_list('trial_id', flat=True).distinct()
        
        trials = Trial.objects.filter(
            id__in=trial_ids,
            is_deleted=False
        ).exclude(
            decision__isnull=True
        ).exclude(decision='')
        
        decisions_data = []
        for trial in trials:
            decisions_data.append({
                'trial_id': trial.id,
                'region': trial.region.name,
                'oblast': trial.region.oblast.name,
                'decision': trial.decision,
                'decision_display': trial.get_decision_display(),
                'justification': trial.decision_justification,
                'recommendations': trial.decision_recommendations,
                'decision_date': trial.decision_date,
                'decided_by': trial.decided_by.username if trial.decided_by else None,
            })
        
        return Response(decisions_data)
    
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """
        Статистика по заявкам
        
        GET /api/v1/applications/statistics/
        """
        applications = self.get_queryset()
        
        return Response({
            'total': applications.count(),
            'by_status': {
                'draft': applications.filter(status='draft').count(),
                'submitted': applications.filter(status='submitted').count(),
                'distributed': applications.filter(status='distributed').count(),
                'in_progress': applications.filter(status='in_progress').count(),
                'completed': applications.filter(status='completed').count(),
                'registered': applications.filter(status='registered').count(),
                'rejected': applications.filter(status='rejected').count(),
            },
            'current_year': applications.filter(
                submission_date__year=timezone.now().year
            ).count(),
        })
    
    @action(detail=False, methods=['get'], url_path='cultures-for-region')
    def cultures_for_region(self, request):
        """
        Получить список культур с заявками для ГСУ
        
        Показывает какие культуры доступны в выбранном ГСУ
        с количеством заявок по каждой культуре.
        
        GET /api/v1/applications/cultures-for-region/?region_id=5
        
        Response:
        {
            "region_id": 5,
            "region_name": "Алматинский ГСУ",
            "oblast_id": 2,
            "oblast_name": "Алматинская область",
            "cultures": [
                {
                    "culture_id": 10,
                    "culture_name": "Пшеница яровая",
                    "applications_count": 3,
                    "pending_count": 3,
                    "in_trial_count": 1,
                    "sample_applications": ["APP-2025-001", "APP-2025-005"]
                }
            ]
        }
        """
        region_id = request.query_params.get('region_id')
        
        if not region_id:
            return Response({
                'error': 'region_id is required'
            }, status=400)
        
        try:
            region = Region.objects.get(id=region_id, is_deleted=False)
        except Region.DoesNotExist:
            return Response({'error': 'Region not found'}, status=404)
        
        # Найти все распределенные заявки для этого региона
        # Используем PlannedDistribution для точности
        planned_distributions = PlannedDistribution.objects.filter(
            region=region,
            status='planned',
            is_deleted=False
        ).select_related('application__sort_record__culture')
        
        # Сгруппировать по культурам
        cultures_data = {}
        for dist in planned_distributions:
            app = dist.application
            if not app or not app.sort_record or not app.sort_record.culture:
                continue
            
            culture = app.sort_record.culture
            culture_id = culture.id
            
            if culture_id not in cultures_data:
                cultures_data[culture_id] = {
                    'culture_id': culture.id,
                    'culture_name': culture.name,
                    'applications': [],
                    'sample_applications': []
                }
            
            cultures_data[culture_id]['applications'].append(app)
            if len(cultures_data[culture_id]['sample_applications']) < 3:
                cultures_data[culture_id]['sample_applications'].append(
                    app.application_number
                )
        
        # Подсчитать статистику
        result = []
        for culture_id, data in cultures_data.items():
            apps = data['applications']
            
            # Проверить сколько уже в испытаниях
            in_trial_count = 0
            for app in apps:
                if TrialParticipant.objects.filter(
                    application=app,
                    trial__region=region,
                    is_deleted=False
                ).exists():
                    in_trial_count += 1
            
            result.append({
                'culture_id': culture_id,
                'culture_name': data['culture_name'],
                'applications_count': len(apps),
                'pending_count': len(apps) - in_trial_count,
                'in_trial_count': in_trial_count,
                'sample_applications': data['sample_applications']
            })
        
        # Сортировать по количеству заявок (больше заявок → выше)
        result.sort(key=lambda x: x['applications_count'], reverse=True)
        
        return Response({
            'region_id': region.id,
            'region_name': region.name,
            'oblast_id': region.oblast.id,
            'oblast_name': region.oblast.name,
            'cultures': result
        })
    
    @action(detail=True, methods=['get'], url_path='regional-status')
    def regional_status(self, request, pk=None):
        """
        Получить статусы испытаний по каждой области для заявки
        
        GET /api/v1/applications/{id}/regional-status/
        
        Response:
        {
          "application_id": 5,
          "application_status": "in_progress",
          "regions": [
            {
              "planned_distribution_id": 1,
              "region_id": 1,
              "region_name": "Алматинский ГСУ",
              "oblast_name": "Алматинская",
              "status": "trial_created",
              "trial_id": 15,
              "trial_status": "active"
            },
            {
              "planned_distribution_id": 2,
              "region_id": 5,
              "region_name": "Акмолинский ГСУ",
              "oblast_name": "Акмолинская",
              "status": "planned",
              "trial_id": null,
              "trial_status": null
            }
          ]
        }
        """
        application = self.get_object()
        
        distributions = PlannedDistribution.objects.filter(
            application=application,
            is_deleted=False
        ).select_related('region__oblast')
        
        regions_data = []
        for dist in distributions:
            # Получаем все Trial для этого PlannedDistribution (многолетние)
            trials = dist.get_trials()
            latest_trial = dist.get_latest_trial()
            
            region_info = {
                'planned_distribution_id': dist.id,
                'region_id': dist.region.id,
                'region_name': dist.region.name,
                'oblast_name': dist.region.oblast.name,
                
                # Статус PlannedDistribution
                'status': dist.status,
                'status_display': dist.get_status_display(),
                
                # Многолетняя информация
                'year_started': dist.year_started,
                'year_completed': dist.year_completed,
                'years_count': dist.get_years_count(),
                
                # Последний Trial (если есть)
                'latest_trial_id': latest_trial.id if latest_trial else None,
                'latest_trial_status': latest_trial.status if latest_trial else None,
                'latest_decision': dist.get_latest_decision(),
                
                # Все Trial (список по годам)
                'trials': []
            }
            
            # Добавляем информацию о всех Trial
            for trial in trials:
                trial_info = {
                    'trial_id': trial.id,
                    'year': trial.year or (trial.start_date.year if trial.start_date else None),
                    'start_date': trial.start_date,
                    'status': trial.status,
                    'status_display': trial.get_status_display(),
                    'decision': trial.decision,
                    'decision_display': trial.get_decision_display() if trial.decision else None,
                    'participants_count': trial.participants.filter(is_deleted=False).count(),
                    'laboratory_status': trial.laboratory_status,
                    'responsible_person': trial.responsible_person,
                }
                region_info['trials'].append(trial_info)
            
            regions_data.append(region_info)
        
        return Response({
            'application_id': application.id,
            'application_number': application.application_number,
            'application_status': application.status,
            'total_regions': len(regions_data),
            'regions': regions_data
        })
    
    @action(detail=False, methods=['get'], url_path='culture-groups-stats')
    def culture_groups_stats(self, request):
        """
        Получить статистику заявок по группам культур
        
        GET /api/v1/applications/culture-groups-stats/
        GET /api/v1/applications/culture-groups-stats/?year=2025
        GET /api/v1/applications/culture-groups-stats/?status=submitted
        """
        from django.db.models import Count, Q
        
        # Базовый queryset
        queryset = self.get_queryset()
        
        # Фильтры
        year = request.query_params.get('year')
        status = request.query_params.get('status')
        
        if year:
            queryset = queryset.filter(created_at__year=year)
        if status:
            queryset = queryset.filter(status=status)
        
        # Статистика по группам культур
        stats = queryset.values(
            'sort_record__culture__group_culture__id',
            'sort_record__culture__group_culture__name',
            'sort_record__culture__group_culture__code',
            'sort_record__culture__group_culture__group_culture_id'
        ).annotate(
            applications_count=Count('id'),
            cultures_count=Count('sort_record__culture', distinct=True)
        ).order_by('-applications_count')
        
        # Общая статистика
        total_applications = queryset.count()
        total_culture_groups = stats.count()
        
        return Response({
            'total_applications': total_applications,
            'total_culture_groups': total_culture_groups,
            'filters_applied': {
                'year': year,
                'status': status
            },
            'culture_groups': [
                {
                    'id': stat['sort_record__culture__group_culture__id'],
                    'name': stat['sort_record__culture__group_culture__name'],
                    'code': stat['sort_record__culture__group_culture__code'],
                    'patents_group_id': stat['sort_record__culture__group_culture__group_culture_id'],
                    'applications_count': stat['applications_count'],
                    'cultures_count': stat['cultures_count']
                }
                for stat in stats
            ]
        })
    
    @action(detail=False, methods=['get'], url_path='pending-for-region')
    def pending_for_region(self, request):
        """
        Получить распределенные заявки для ГСУ по культуре
        
        Используется сортопытом при добавлении участников.
        
        GET /api/v1/applications/pending-for-region/?region_id=1&culture_id=1
        GET /api/v1/applications/pending-for-region/?region_id=1  (все культуры)
        """
        culture_id = request.query_params.get('culture_id')
        region_id = request.query_params.get('region_id')
        trial_id = request.query_params.get('trial_id')
        
        # region_id обязателен, culture_id - опционально
        if not region_id:
            return Response({
                'error': 'region_id is required'
            }, status=400)
        
        try:
            region = Region.objects.get(id=region_id, is_deleted=False)
        except Region.DoesNotExist:
            return Response({'error': 'Region not found'}, status=404)
        
        # Базовый фильтр - распределенные заявки для этой области
        applications_qs = Application.objects.filter(
            status__in=['distributed', 'in_progress'],
            target_oblasts__id=region.oblast_id,
            is_deleted=False
        )
        
        # Фильтр по культуре (если указана)
        if culture_id:
            applications_qs = applications_qs.filter(
                sort_record__culture_id=culture_id
            )
        
        applications_qs = applications_qs.distinct()
        
        result = []
        for app in applications_qs:
            app_data = {
                'id': app.id,
                'application_number': app.application_number,
                'sort_record': SortRecordSerializer(app.sort_record).data if app.sort_record else None,
                'already_in_trial': False
            }
            
            # Проверить добавлен ли в указанное испытание
            if trial_id:
                app_data['already_in_trial'] = TrialParticipant.objects.filter(
                    trial_id=trial_id,
                    sort_record=app.sort_record,
                    is_deleted=False
                ).exists()
            
            result.append(app_data)
        
        return Response({
            'total': len(result),
            'region_id': region.id,
            'region_name': region.name,
            'culture_id': culture_id if culture_id else None,
            'applications': result
        })
    
    @action(detail=True, methods=['post'], url_path='make-decision')
    def make_decision(self, request, pk=None):
        """
        Принять решение по заявке за год
        
        POST /api/applications/{id}/make-decision/
        
        Body:
        {
            "oblast_id": 17,
            "year": 2024,
            "decision": "approved",
            "justification": "Превышает стандарт на 37%...",
            "average_yield": 128.2
        }
        """
        application = self.get_object()
        
        oblast_id = request.data.get('oblast_id')
        year = request.data.get('year')
        decision = request.data.get('decision')
        justification = request.data.get('justification', '')
        average_yield = request.data.get('average_yield')
        
        if not all([oblast_id, year, decision]):
            return Response({
                'success': False,
                'error': 'oblast_id, year and decision are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            oblast = Oblast.objects.get(id=oblast_id)
        except Oblast.DoesNotExist:
            return Response({
                'success': False,
                'error': f'Oblast {oblast_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Принять решение
        decision_history = application.make_decision(
            oblast=oblast,
            year=int(year),
            decision=decision,
            justification=justification,
            decided_by=request.user,
            average_yield=average_yield
        )
        
        return Response({
            'success': True,
            'message': 'Решение успешно принято',
            'decision': {
                'id': decision_history.id,
                'application_id': application.id,
                'oblast': oblast.name,
                'year': year,
                'decision': decision,
                'decision_date': str(decision_history.decision_date),
                'justification': justification,
                'average_yield': average_yield,
                'years_tested_total': decision_history.years_tested_total
            },
            'application_status': application.status
        })
    
    @action(detail=True, methods=['get'], url_path='decision-history')
    def decision_history_view(self, request, pk=None):
        """
        Получить историю решений по заявке
        
        GET /api/applications/{id}/decision-history/?oblast_id=17
        """
        application = self.get_object()
        oblast_id = request.query_params.get('oblast_id')
        
        oblast = None
        if oblast_id:
            try:
                oblast = Oblast.objects.get(id=oblast_id)
            except Oblast.DoesNotExist:
                pass
        
        history = application.get_decision_history(oblast=oblast)
        
        history_data = []
        for record in history:
            history_data.append({
                'id': record.id,
                'oblast': record.oblast.name,
                'year': record.year,
                'decision': record.decision,
                'decision_display': record.get_decision_display(),
                'decision_date': str(record.decision_date),
                'justification': record.decision_justification,
                'decided_by': record.decided_by.username if record.decided_by else None,
                'average_yield': record.average_yield,
                'years_tested_total': record.years_tested_total
            })
        
        return Response({
            'application_id': application.id,
            'application_number': application.application_number,
            'sort_name': application.sort_record.name,
            'history': history_data
        })




