"""
Application ViewSets
"""
import json
import logging

from rest_framework import viewsets, permissions, status, parsers, serializers as drf_serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models as django_models, transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from ..pagination import StandardPagination

from ..models import (
    Oblast, Region, ClimateZone, Indicator, GroupCulture, Culture,
    Originator, SortRecord, Application, ApplicationDecisionHistory,
    ApplicationOblastState,
    PlannedDistribution, TrialType, Trial, TrialParticipant, TrialResult,
    TrialLaboratoryResult, Document, TrialPlan, TrialPlanParticipant,
    APPLICATION_MANDATORY_DOCUMENT_TYPES,
    TrialPlanTrial, TrialPlanCulture, TrialPlanCultureTrialType
)
from ..serializers import (
    OblastSerializer, RegionSerializer, ClimateZoneSerializer,
    IndicatorSerializer, GroupCultureSerializer, CultureSerializer,
    OriginatorSerializer, SortRecordSerializer, ApplicationSerializer,
    TrialTypeSerializer, TrialSerializer, TrialParticipantSerializer,
    TrialResultSerializer, TrialLaboratoryResultSerializer,
    DocumentSerializer, TrialPlanSerializer, TrialPlanWriteSerializer,
    ApplicationSubmissionDocumentMetaSerializer,
    TrialPlanAddParticipantsSerializer, TrialPlanCultureSerializer,
    TrialPlanAddCultureSerializer, create_basic_trial_results,
    create_quality_trial_results
)
from ..filters import ApplicationFilter
from ..patents_integration import patents_api
from ..services import WorkflowService
from ..storage import is_storage_error

logger = logging.getLogger(__name__)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Управление заявками на сортоиспытания
    
    Заявка → Распределение по областям → Испытания → Решения → Реестр
    
    Поддерживает расширенную фильтрацию, сортировку и пагинацию:
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
    - Сортировка (ordering) - по полям: application_number, submission_date, id, created_at, updated_at
      Используйте префикс "-" для сортировки по убыванию, например: ?ordering=-application_number
    - Пагинация с настраиваемым размером страницы
    
    Примеры использования:
    - GET /api/applications/?patents_culture_id=720&page=1&page_size=20
    - GET /api/applications/?patents_group_id=1&search=пшеница
    - GET /api/applications/?status=submitted&patents_culture_id=749
    - GET /api/applications/?culture_group_name=зерновые
    - GET /api/applications/?group_search=пшеница&year=2025
    - GET /api/applications/?oblast=1&culture_group=2
    - GET /api/applications/?patents_group_id=1&patents_culture_id=720
    - GET /api/applications/?ordering=application_number
    - GET /api/applications/?ordering=-application_number
    - GET /api/applications/?ordering=submission_date
    """
    queryset = Application.objects.filter(is_deleted=False).select_related(
        'sort_record__culture__group_culture'
    ).prefetch_related('target_oblasts')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Требуется авторизация
    
    # Фильтрация и сортировка
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ApplicationFilter
    ordering_fields = ['application_number', 'submission_date', 'id', 'created_at', 'updated_at']
    ordering = ['-id']  # Сортировка по умолчанию (последние сначала)
    
    # Пагинация
    pagination_class = StandardPagination
    
    def perform_create(self, serializer):
        """При создании заявки устанавливаем created_by"""
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

    @staticmethod
    def _cleanup_saved_files(saved_files):
        for storage, file_name in reversed(saved_files):
            if not file_name:
                continue
            try:
                if storage.exists(file_name):
                    storage.delete(file_name)
            except Exception:
                logger.warning('Failed to cleanup uploaded file %s after rollback', file_name, exc_info=True)

    @action(
        detail=False,
        methods=['post'],
        url_path='submit',
        parser_classes=[parsers.MultiPartParser, parsers.FormParser],
    )
    def submit(self, request):
        """
        Атомарная подача заявки с документами в одном multipart-запросе.
        """
        payload_raw = request.data.get('payload')
        document_meta_raw = request.data.get('document_meta')
        uploaded_files = request.FILES.getlist('documents')

        if not payload_raw:
            return Response({'payload': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        if not document_meta_raw:
            return Response({'document_meta': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        if not uploaded_files:
            return Response({'documents': ['At least one file is required.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = json.loads(payload_raw)
        except (TypeError, ValueError):
            return Response(
                {'payload': ['Expected a valid JSON object string.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            document_meta = json.loads(document_meta_raw)
        except (TypeError, ValueError):
            return Response(
                {'document_meta': ['Expected a valid JSON array string.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(payload, dict):
            return Response(
                {'payload': ['Expected a JSON object.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not isinstance(document_meta, list):
            return Response(
                {'document_meta': ['Expected a JSON array.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(uploaded_files) != len(document_meta):
            return Response(
                {'documents': ['Document files count must match document_meta count.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application_serializer = self.get_serializer(data=payload)
        application_serializer.is_valid(raise_exception=True)

        document_meta_serializer = ApplicationSubmissionDocumentMetaSerializer(data=document_meta, many=True)
        if not document_meta_serializer.is_valid():
            return Response(
                {'document_meta': document_meta_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submitted_document_types = {
            item['document_type']
            for item in document_meta_serializer.validated_data
        }
        missing_document_types = [
            doc_type
            for doc_type in APPLICATION_MANDATORY_DOCUMENT_TYPES
            if doc_type not in submitted_document_types
        ]
        if missing_document_types:
            return Response(
                {
                    'document_meta': ['Missing mandatory documents in submission.'],
                    'missing_mandatory_documents': missing_document_types,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        saved_files = []
        created_document_ids = []
        application = None

        try:
            with transaction.atomic():
                application = application_serializer.save(created_by=request.user)

                for meta, uploaded_file in zip(document_meta_serializer.validated_data, uploaded_files):
                    document_serializer = DocumentSerializer(data={
                        'title': meta['title'],
                        'document_type': meta['document_type'],
                        'is_mandatory': meta['is_mandatory'],
                        'application': application.id,
                        'file': uploaded_file,
                    })
                    document_serializer.is_valid(raise_exception=True)
                    document = document_serializer.save(uploaded_by=request.user)
                    created_document_ids.append(document.id)
                    if document.file and document.file.name:
                        saved_files.append((document.file.storage, document.file.name))
        except drf_serializers.ValidationError as exc:
            self._cleanup_saved_files(saved_files)
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            self._cleanup_saved_files(saved_files)
            if is_storage_error(exc):
                logger.exception(
                    'Atomic application submission storage failure application_number=%s sort_id=%s document_types=%s',
                    payload.get('application_number'),
                    payload.get('sort_id'),
                    [item.get('document_type') for item in document_meta],
                )
                return Response(
                    {
                        'error': 'Document storage is unavailable. Please try again later.',
                        'code': 'storage_unavailable',
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            logger.exception(
                'Atomic application submission failed application_number=%s sort_id=%s',
                payload.get('application_number'),
                payload.get('sort_id'),
            )
            return Response(
                {
                    'error': 'Failed to submit application with documents.',
                    'code': 'submit_failed',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                'application': self.get_serializer(application).data,
                'document_ids': created_document_ids,
                'documents_count': len(created_document_ids),
            },
            status=status.HTTP_201_CREATED,
        )
    
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
        
        WorkflowService.distribute_application(application, validated_distributions, request.user)
        
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
        total = applications.count()

        # Подсчет заявок с полными документами
        from trials_app.models import APPLICATION_MANDATORY_DOCUMENT_TYPES
        mandatory_count = len(APPLICATION_MANDATORY_DOCUMENT_TYPES)
        docs_complete = 0
        docs_incomplete = 0
        if mandatory_count > 0:
            for app in applications.prefetch_related('documents').iterator(chunk_size=500):
                uploaded = set(
                    app.documents.filter(is_deleted=False).values_list('document_type', flat=True)
                )
                if all(dt in uploaded for dt in APPLICATION_MANDATORY_DOCUMENT_TYPES):
                    docs_complete += 1
                else:
                    docs_incomplete += 1
        else:
            docs_complete = total

        # Распределение по годам подачи
        from django.db.models import Count
        by_year_qs = (
            applications
            .exclude(submission_date__isnull=True)
            .values('submission_date__year')
            .annotate(count=Count('id'))
            .order_by('submission_date__year')
        )
        by_year = {str(row['submission_date__year']): row['count'] for row in by_year_qs}

        registered = applications.filter(status='registered').count()
        rejected = applications.filter(status='rejected').count()
        decided = registered + rejected
        success_rate = round((registered / decided) * 100, 1) if decided > 0 else 0

        return Response({
            'total': total,
            'by_status': {
                'draft': applications.filter(status='draft').count(),
                'submitted': applications.filter(status='submitted').count(),
                'distributed': applications.filter(status='distributed').count(),
                'in_progress': applications.filter(status='in_progress').count(),
                'completed': applications.filter(status='completed').count(),
                'registered': registered,
                'rejected': rejected,
            },
            'by_year': by_year,
            'success_rate': success_rate,
            'current_year': applications.filter(
                submission_date__year=timezone.now().year
            ).count(),
            'documents': {
                'complete': docs_complete,
                'incomplete': docs_incomplete,
            },
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
    
    @action(detail=False, methods=['get'], url_path='top-cultures')
    def top_cultures(self, request):
        """
        Топ-12 культур по количеству заявок с разбивкой по документам.

        GET /api/v1/applications/top-cultures/
        """
        from django.db.models import Count, Q as DQ
        from trials_app.models import APPLICATION_MANDATORY_DOCUMENT_TYPES

        queryset = self.get_queryset()
        mandatory_count = len(APPLICATION_MANDATORY_DOCUMENT_TYPES)

        stats = (
            queryset
            .values(
                'sort_record__culture__id',
                'sort_record__culture__name',
            )
            .annotate(
                total=Count('id'),
            )
            .order_by('-total')[:20]
        )

        # Для каждой культуры подсчитаем docs_complete
        results = []
        for row in stats:
            culture_id = row['sort_record__culture__id']
            total = row['total']
            culture_qs = queryset.filter(sort_record__culture_id=culture_id)

            if mandatory_count > 0:
                docs_complete = 0
                for app in culture_qs.prefetch_related('documents').iterator(chunk_size=200):
                    uploaded = set(
                        app.documents.filter(is_deleted=False)
                        .values_list('document_type', flat=True)
                    )
                    if all(dt in uploaded for dt in APPLICATION_MANDATORY_DOCUMENT_TYPES):
                        docs_complete += 1
            else:
                docs_complete = total

            results.append({
                'culture_id': culture_id,
                'culture_name': row['sort_record__culture__name'] or 'Не указана',
                'total': total,
                'docs_complete': docs_complete,
                'docs_incomplete': total - docs_complete,
            })

        total_applications = queryset.count()
        return Response({
            'total_applications': total_applications,
            'cultures': results,
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
    
    @action(detail=True, methods=['post'], url_path='update-oblast-statuses')
    def update_oblast_statuses(self, request, pk=None):
        """
        Ручное обновление статусов по областям.

        - Для финальных статусов (approved/continue/rejected) также создаёт
          ApplicationDecisionHistory и пишет decision metadata в OblastState.
        - Для возврата в ранние статусы (planned..decision_made) очищает
          decision metadata, чтобы не оставлять стейл от предыдущего решения.
        - trial и trial_plan никогда не затрагиваются.

        POST /api/applications/{id}/update-oblast-statuses/
        Body: { "statuses": [{ "oblast_id": 1, "status": "approved" }, ...] }
        """
        DECISION_STATUSES = {'approved', 'continue', 'rejected', 'removed', 'withdrawn'}
        PRE_DECISION_STATUSES = {
            'planned', 'trial_plan_created', 'trial_created',
            'trial_in_progress', 'trial_completed',
            'decision_pending', 'decision_made',
        }

        application = self.get_object()
        statuses = request.data.get('statuses', [])

        if not isinstance(statuses, list) or not statuses:
            return Response(
                {'success': False, 'error': 'statuses list is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = dict(ApplicationOblastState.STATUS_CHOICES)
        target_ids = set(application.target_oblasts.values_list('id', flat=True))

        # Fail-fast: validate all items before applying any changes
        errors = []
        for idx, item in enumerate(statuses):
            oblast_id = item.get('oblast_id')
            new_status = item.get('status')
            if oblast_id not in target_ids:
                errors.append(f'[{idx}] Oblast {oblast_id} not in target oblasts')
            if new_status not in valid_statuses:
                errors.append(f'[{idx}] Invalid status: {new_status}')

        if errors:
            return Response(
                {'success': False, 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = timezone.now()
        updated_count = 0

        with transaction.atomic():
            for item in statuses:
                oblast_id = item['oblast_id']
                new_status = item['status']
                custom_year = item.get('decision_year')
                if custom_year is not None:
                    try:
                        custom_year = int(custom_year)
                    except (ValueError, TypeError):
                        custom_year = None
                effective_year = custom_year or now.year

                qs = ApplicationOblastState.objects.filter(
                    application=application,
                    oblast_id=oblast_id,
                    is_deleted=False,
                )

                if new_status in DECISION_STATUSES:
                    from datetime import date as date_type
                    effective_date = date_type(effective_year, 1, 1)
                    # Decision status: update status + decision metadata + create history
                    rows = qs.update(
                        status=new_status,
                        decision_date=effective_date,
                        decision_justification='Ручное изменение статуса',
                        decided_by=request.user,
                        decision_year=effective_year,
                        updated_at=now,
                    )
                    years_tested = ApplicationDecisionHistory.objects.filter(
                        application=application,
                        oblast_id=oblast_id,
                        year__lte=effective_year,
                    ).exclude(year=effective_year).count() + 1
                    ApplicationDecisionHistory.objects.update_or_create(
                        application=application,
                        oblast_id=oblast_id,
                        year=effective_year,
                        defaults={
                            'decision': new_status,
                            'decision_date': effective_date,
                            'decision_justification': 'Ручное изменение статуса',
                            'decided_by': request.user,
                            'years_tested_total': years_tested,
                        },
                    )
                elif new_status in PRE_DECISION_STATUSES:
                    # Pre-decision: clear stale decision metadata
                    rows = qs.update(
                        status=new_status,
                        decision_date=None,
                        decision_justification=None,
                        decided_by=None,
                        decision_year=None,
                        updated_at=now,
                    )

                updated_count += rows

            application._update_overall_status()

        application.refresh_from_db()
        serializer = self.get_serializer(application)
        return Response({
            'success': True,
            'updated_count': updated_count,
            'application': serializer.data,
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
        raw_decision_date = request.data.get('decision_date')

        if not all([oblast_id, year, decision]):
            return Response({
                'success': False,
                'error': 'oblast_id, year and decision are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        parsed_decision_date = None
        if raw_decision_date and isinstance(raw_decision_date, str):
            from datetime import date as date_type
            try:
                parsed_decision_date = date_type.fromisoformat(raw_decision_date)
            except ValueError:
                pass

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
            average_yield=average_yield,
            decision_date=parsed_decision_date,
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
                'oblast_id': record.oblast_id,
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

    @action(detail=True, methods=['patch'], url_path=r'edit-decision/(?P<history_id>\d+)')
    def edit_decision(self, request, pk=None, history_id=None):
        """
        Редактировать решение в истории.

        PATCH /api/applications/{id}/edit-decision/{history_id}/

        Проходит через make_decision() для атомарного обновления
        ApplicationDecisionHistory + ApplicationOblastState + Application.status.
        """
        application = self.get_object()

        try:
            record = ApplicationDecisionHistory.objects.get(
                id=history_id, application=application,
            )
        except ApplicationDecisionHistory.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Decision history record not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        year = request.data.get('year', record.year)
        decision = request.data.get('decision', record.decision)
        justification = request.data.get('justification', record.decision_justification)
        average_yield = request.data.get('average_yield', record.average_yield)
        oblast_id = request.data.get('oblast_id', record.oblast_id)
        raw_decision_date = request.data.get('decision_date')

        parsed_decision_date = None
        if raw_decision_date and isinstance(raw_decision_date, str):
            from datetime import date as date_type
            try:
                parsed_decision_date = date_type.fromisoformat(raw_decision_date)
            except ValueError:
                pass

        try:
            oblast = Oblast.objects.get(id=oblast_id)
        except Oblast.DoesNotExist:
            return Response(
                {'success': False, 'error': f'Oblast {oblast_id} not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Если год или область изменились — удалить старую запись
        if int(year) != record.year or int(oblast_id) != record.oblast_id:
            record.delete()

        decision_history = application.make_decision(
            oblast=oblast,
            year=int(year),
            decision=decision,
            justification=justification,
            decided_by=request.user,
            average_yield=average_yield,
            decision_date=parsed_decision_date,
        )

        return Response({
            'success': True,
            'decision': {
                'id': decision_history.id,
                'oblast_id': oblast.id,
                'oblast': oblast.name,
                'year': decision_history.year,
                'decision': decision_history.decision,
                'decision_display': decision_history.get_decision_display(),
                'decision_date': str(decision_history.decision_date),
                'justification': decision_history.decision_justification,
                'average_yield': decision_history.average_yield,
                'years_tested_total': decision_history.years_tested_total,
            },
        })

    @action(detail=True, methods=['delete'], url_path=r'delete-decision/(?P<history_id>\d+)')
    def delete_decision(self, request, pk=None, history_id=None):
        """
        Удалить решение из истории.

        DELETE /api/applications/{id}/delete-decision/{history_id}/

        После удаления откатывает ApplicationOblastState на предыдущее решение.
        Если истории не осталось — сбрасывает на 'planned'.
        """
        application = self.get_object()

        try:
            record = ApplicationDecisionHistory.objects.get(
                id=history_id, application=application,
            )
        except ApplicationDecisionHistory.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Decision history record not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        oblast = record.oblast
        record.delete()

        # Откатить OblastState на предыдущее решение
        previous = ApplicationDecisionHistory.objects.filter(
            application=application, oblast=oblast,
        ).order_by('-year').first()

        if previous:
            application.update_oblast_status(
                oblast=oblast,
                new_status=previous.decision,
                decision_date=previous.decision_date,
                decision_justification=previous.decision_justification,
                decided_by=previous.decided_by,
                decision_year=previous.year,
            )
        else:
            # Нет истории — сбросить на planned, очистить decision metadata
            ApplicationOblastState.objects.filter(
                application=application, oblast=oblast, is_deleted=False,
            ).update(
                status='planned',
                decision_date=None,
                decision_justification=None,
                decided_by=None,
                decision_year=None,
                updated_at=timezone.now(),
            )

        application._update_overall_status()

        return Response({'success': True})

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        """
        Excel-экспорт заявок с фильтрами.

        GET /api/applications/export/?search=пшеница&year=2025
        Возвращает .xlsx файл. Принимает те же фильтры что и список заявок.
        Если передан ?oblast=N, экспортируются только состояния для этой области.
        """
        from datetime import date as date_type
        from django.http import HttpResponse
        from ..services.exporters import build_applications_export_workbook

        queryset = self.filter_queryset(self.get_queryset())

        # Pass oblast filter to exporter for strict oblast filtering
        filter_oblast_id = None
        oblast_param = request.query_params.get('oblast')
        if oblast_param:
            try:
                filter_oblast_id = int(oblast_param)
            except (ValueError, TypeError):
                pass

        content = build_applications_export_workbook(queryset, filter_oblast_id=filter_oblast_id)

        filename = f'applications_export_{date_type.today().isoformat()}.xlsx'
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=['get'], url_path='report')
    def report(self, request):
        """
        Сводный отчёт по годам (как в Gosreestr).

        GET /api/applications/report/
        Возвращает JSON с rows (по годам) и totals.
        """
        from ..services.reports import build_applications_report_rows, build_applications_report_totals

        queryset = self.filter_queryset(self.get_queryset())
        rows = build_applications_report_rows(queryset)
        totals = build_applications_report_totals(rows)

        return Response({'rows': rows, 'totals': totals})

    @action(detail=False, methods=['get'], url_path='report/export')
    def report_export(self, request):
        """
        Excel-экспорт сводного отчёта.

        GET /api/applications/report/export/
        """
        from datetime import date as date_type
        from django.http import HttpResponse
        from ..services.reports import (
            build_applications_report_rows,
            build_applications_report_totals,
            build_applications_report_workbook,
        )

        queryset = self.filter_queryset(self.get_queryset())
        rows = build_applications_report_rows(queryset)
        totals = build_applications_report_totals(rows)
        content = build_applications_report_workbook(rows, totals)

        filename = f'report_{date_type.today().isoformat()}.xlsx'
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

