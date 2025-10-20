"""
Trial Plan ViewSets
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models as django_models

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
from ..patents_integration import patents_api


class TrialPlanViewSet(viewsets.ModelViewSet):
    """
    Управление планами испытаний
    
    Планы сортоиспытаний на год с участниками (заявки + сорта из реестра).
    Автоматическое предложение заявок по областям и культурам.
    """
    queryset = TrialPlan.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated]  # Требуется авторизация
    
    def get_serializer_class(self):
        """Используем разные сериализаторы для чтения и записи"""
        if self.action in ['create', 'update', 'partial_update']:
            return TrialPlanWriteSerializer
        return TrialPlanSerializer
    
    def perform_create(self, serializer):
        """При создании плана устанавливаем created_by"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='suggest-applications')
    def suggest_applications(self, request):
        """
        Предложить заявки для плана по областям и культурам
        
        GET /api/v1/trial-plans/suggest-applications/?oblast_id=1&culture_id=5&trial_type_id=1&season=spring
        
        Возвращает заявки со статусом 'submitted' для указанной области и культуры.
        """
        oblast_id = request.query_params.get('oblast_id')
        culture_id = request.query_params.get('culture_id')
        trial_type_id = request.query_params.get('trial_type_id')
        season = request.query_params.get('season', 'spring')  # По умолчанию весна
        
        if not oblast_id or not culture_id:
            return Response({
                'error': 'oblast_id and culture_id are required'
            }, status=400)
        
        try:
            oblast = Oblast.objects.get(id=oblast_id, is_deleted=False)
            culture = Culture.objects.get(id=culture_id, is_deleted=False)
        except (Oblast.DoesNotExist, Culture.DoesNotExist):
            return Response({'error': 'Oblast or Culture not found'}, status=404)
        
        # Найти заявки для этой области и культуры
        applications = Application.objects.filter(
            target_oblasts=oblast,
            sort_record__culture=culture,
            status='submitted',
            is_deleted=False
        ).select_related('sort_record__culture').distinct()
        
        # Дополнительная фильтрация по типу испытания если указан
        if trial_type_id:
            # Здесь можно добавить логику фильтрации по типу испытания
            pass
        
        result = []
        for app in applications:
            app_data = {
                'id': app.id,
                'application_number': app.application_number,
                'sort_record': {
                    'id': app.sort_record.id,
                    'name': app.sort_record.name,
                    'patents_sort_id': app.sort_record.sort_id
                },
                'submission_date': app.submission_date,
                'applicant': app.applicant,
                'maturity_group': app.maturity_group,
            }
            result.append(app_data)
        
        return Response({
            'total': len(result),
            'oblast_id': oblast.id,
            'oblast_name': oblast.name,
            'culture_id': culture.id,
            'culture_name': culture.name,
            'season': season,
            'applications': result
        })
    
    @action(detail=True, methods=['post'], url_path='cultures/(?P<culture_id>[^/.]+)/trial-types/(?P<trial_type_id>[^/.]+)/add-participants')
    def add_participants(self, request, pk=None, culture_id=None, trial_type_id=None):
        """
        Добавить участников к типу испытания культуры в плане
        
        POST /api/trial-plans/{id}/cultures/{culture_id}/trial-types/{trial_type_id}/add-participants/
        {
            "participants": [
                {
                    "patents_sort_id": 1774,
                    "statistical_group": 0,
                    "seeds_provision": "provided",
                    "maturity_group": "D03",
                    "application": 22,
                    "trials": [
                        {
                            "region_id": 1,
                            "predecessor": "fallow",  // или culture_id (например: 5)
                            "seeding_rate": 4.5,
                            "season": "spring"  // опционально, подставляется из культуры
                        }
                    ]
                }
            ]
        }
        """
        trial_plan = self.get_object()
        
        # Проверяем что культура существует в плане
        try:
            trial_plan_culture = TrialPlanCulture.objects.get(
                trial_plan=trial_plan,
                culture_id=culture_id,
                is_deleted=False
            )
        except TrialPlanCulture.DoesNotExist:
            return Response(
                {'error': 'Культура не найдена в плане'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Проверяем что тип испытания существует для этой культуры
        try:
            culture_trial_type = TrialPlanCultureTrialType.objects.get(
                trial_plan_culture=trial_plan_culture,
                trial_type_id=trial_type_id,
                is_deleted=False
            )
        except TrialPlanCultureTrialType.DoesNotExist:
            return Response(
                {'error': 'Тип испытания не найден для данной культуры в плане'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TrialPlanAddParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            participants_data = serializer.validated_data['participants']
            
            # ✅ ГРУППИРОВКА: Объединяем участников с одинаковым сортом
            # Ключ: patents_sort_id, значение: объединенные данные участника
            grouped_participants = {}
            
            for p_data in participants_data:
                sort_id = p_data['patents_sort_id']
                trials_data = p_data.pop('trials', [])
                
                if sort_id not in grouped_participants:
                    # Первый участник с этим сортом - сохраняем его данные
                    grouped_participants[sort_id] = p_data.copy()
                    grouped_participants[sort_id]['trials'] = trials_data
                else:
                    # Сорт уже есть - добавляем trials к существующему
                    grouped_participants[sort_id]['trials'].extend(trials_data)
            
            created_participants = []
            created_trials = []
            
            # Создать участников и их trials
            for sort_id, p_data in grouped_participants.items():
                # Получить trials data
                trials_data = p_data.pop('trials', [])
                
                # Получить application если указан
                application_id = p_data.get('application')
                application_obj = None
                if application_id:
                    try:
                        from .models import Application
                        application_obj = Application.objects.get(id=application_id)
                    except Application.DoesNotExist:
                        return Response({
                            'error': f'Application with ID {application_id} not found'
                        }, status=400)
                
                # ✅ ПРОВЕРКА: Если участник с таким сортом уже существует, используем его
                existing_participant = TrialPlanParticipant.objects.filter(
                    culture_trial_type=culture_trial_type,
                    patents_sort_id=sort_id,
                    is_deleted=False
                ).first()
                
                if existing_participant:
                    # Используем существующего участника
                    participant = existing_participant
                else:
                    # Создаем нового участника
                    # Автоматически генерируем participant_number (следующий доступный номер)
                    max_number = TrialPlanParticipant.objects.filter(
                        culture_trial_type=culture_trial_type,
                        is_deleted=False
                    ).aggregate(max_num=django_models.Max('participant_number'))['max_num'] or 0
                    participant_number = max_number + 1
                    
                    try:
                        participant = TrialPlanParticipant.objects.create(
                            culture_trial_type=culture_trial_type,
                            patents_sort_id=p_data['patents_sort_id'],
                            statistical_group=p_data.get('statistical_group', 1),
                            seeds_provision=p_data.get('seeds_provision', 'not_provided'),
                            participant_number=participant_number,
                            maturity_group=p_data.get('maturity_group', ''),
                            application=application_obj,
                            created_by=request.user
                        )
                        created_participants.append(participant)
                    except Exception as e:
                        return Response({
                            'error': f'Failed to create participant: {str(e)}'
                        }, status=400)
                
                # Создать trials для этого участника
                for trial_data in trials_data:
                    # Валидация обязательных полей
                    region_id = trial_data.get('region_id')
                    if not region_id:
                        return Response({
                            'error': 'region_id is required for each trial'
                        }, status=400)
                    
                    predecessor = trial_data.get('predecessor')
                    if not predecessor:
                        return Response({
                            'error': 'predecessor is required for each trial'
                        }, status=400)
                    
                    seeding_rate = trial_data.get('seeding_rate')
                    if seeding_rate is None:
                        return Response({
                            'error': 'seeding_rate is required for each trial'
                        }, status=400)
                    
                    # Подставляем дефолты с плана если не переданы
                    trial_season = trial_data.get('season', culture_trial_type.season)
                    
                    try:
                        trial = TrialPlanTrial.objects.create(
                            participant=participant,
                            region_id=region_id,
                            predecessor=predecessor,
                            seeding_rate=seeding_rate,
                            season=trial_season,
                            created_by=request.user
                        )
                    except Exception as e:
                        return Response({
                            'error': f'Failed to create trial: {str(e)}'
                        }, status=400)
                    created_trials.append(trial)
            
            # Обновить статус плана
            trial_plan.status = 'structured'
            trial_plan.update_statistics()
            
            return Response({
                'success': True,
                'message': f'Added {len(created_participants)} participants with {len(created_trials)} trials',
                'participants_created': len(created_participants),
                'trials_created': len(created_trials),
                'plan': TrialPlanSerializer(trial_plan).data
            })
        else:
            return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['post'], url_path='distribute')
    def distribute(self, request, pk=None):
        """
        Распределить план - создать PlannedDistribution для каждой заявки
        
        Использует trial-level season и trial_type из TrialPlanTrial.
        
        POST /api/v1/trial-plans/{id}/distribute/
        """
        trial_plan = self.get_object()
        
        if trial_plan.status not in ['structured']:
            return Response({
                'error': 'Plan must be structured before distribution'
            }, status=400)
        
        # Работаем с моделями, а не с JSON
        participants = TrialPlanParticipant.objects.filter(
            trial_plan=trial_plan,
            is_deleted=False
        ).prefetch_related('trials')
        
        created_distributions = []
        
        # Найти участников с заявками
        for participant in participants:
            if not participant.application:
                continue
            
            # Получить trials для участника
            trials = participant.trials.filter(is_deleted=False)
            
            # Создать PlannedDistribution для каждого trial
            for trial in trials:
                try:
                    # Создать или обновить PlannedDistribution
                    # Используем trial-level значения (не с плана!)
                    planned_dist, created = PlannedDistribution.objects.update_or_create(
                        application=participant.application,
                        region=trial.region,
                        defaults={
                            'trial_type': trial.trial_type,  # Из trial, не из плана
                            'planting_season': trial.season,  # Из trial, не из плана
                            'created_by': request.user,
                            'notes': f'Created from plan {trial_plan.id}'
                        }
                    )
                    
                    if created:
                        created_distributions.append({
                            'application_id': participant.application.id,
                            'application_number': participant.application.application_number,
                            'region_id': trial.region.id,
                            'region_name': trial.region.name,
                            'planned_distribution_id': planned_dist.id,
                            'trial_type': trial.trial_type.name if trial.trial_type else None,
                            'season': trial.season
                        })
                
                except Exception as e:
                    # Логируем ошибку и продолжаем
                    print(f"Error creating PlannedDistribution: {str(e)}")
                    continue
        
        # Обновить статус плана
        trial_plan.status = 'distributed'
        trial_plan.save()
        
        return Response({
            'success': True,
            'message': f'Plan distributed with {len(created_distributions)} new distributions',
            'created_distributions': created_distributions,
            'plan': TrialPlanSerializer(trial_plan).data
        })
    
    @action(detail=True, methods=['get'], url_path='statistics')
    def statistics(self, request, pk=None):
        """
        Получить статистику плана
        
        Считает по модели с учетом trial-level значений.
        
        GET /api/v1/trial-plans/{id}/statistics/
        """
        trial_plan = self.get_object()
        
        # Получить участников из модели (не JSON)
        participants = TrialPlanParticipant.objects.filter(
            trial_plan=trial_plan,
            is_deleted=False
        )
        
        # Статистика по группам спелости
        maturity_groups = {}
        for participant in participants:
            group = participant.maturity_group or 'unknown'
            if group not in maturity_groups:
                maturity_groups[group] = 0
            maturity_groups[group] += 1
        
        # Статистика по обеспеченности семенами
        seeds_provision = {}
        for participant in participants:
            provision = participant.seeds_provision or 'unknown'
            if provision not in seeds_provision:
                seeds_provision[provision] = 0
            seeds_provision[provision] += 1
        
        # Статистика по источникам (заявки vs реестр)
        from_applications = participants.filter(application__isnull=False).count()
        from_registry = participants.filter(application__isnull=True).count()
        
        # Статистика по типам испытания (из TrialPlanTrial)
        trial_types_stats = {}
        trials = TrialPlanTrial.objects.filter(
            participant__trial_plan=trial_plan,
            is_deleted=False
        ).select_related('trial_type')
        
        for trial in trials:
            trial_type_name = trial.trial_type.name if trial.trial_type else 'Не указан'
            if trial_type_name not in trial_types_stats:
                trial_types_stats[trial_type_name] = 0
            trial_types_stats[trial_type_name] += 1
        
        # Статистика по сезонам (из TrialPlanTrial)
        seasons_stats = {}
        for trial in trials:
            season = trial.season or 'unknown'
            if season not in seasons_stats:
                seasons_stats[season] = 0
            seasons_stats[season] += 1
        
        return Response({
            'plan_id': trial_plan.id,
            'total_participants': participants.count(),
            'from_applications': from_applications,
            'from_registry': from_registry,
            'maturity_groups': maturity_groups,
            'seeds_provision': seeds_provision,
            'total_trials': trial_plan.get_trials_count(),
            'trial_types': trial_types_stats,
            'seasons': seasons_stats,
            'status': trial_plan.status
        })
    
    @action(detail=False, methods=['get'], url_path='by-year')
    def by_year(self, request):
        """
        Получить планы по году
        
        GET /api/v1/trial-plans/by-year/?year=2025
        """
        year = request.query_params.get('year')
        if not year:
            return Response({'error': 'year parameter is required'}, status=400)
        
        try:
            year = int(year)
        except ValueError:
            return Response({'error': 'year must be a number'}, status=400)
        
        plans = self.get_queryset().filter(year=year)
        serializer = self.get_serializer(plans, many=True)
        
        return Response({
            'year': year,
            'total_plans': plans.count(),
            'plans': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='predecessor-options')
    def predecessor_options(self, request):
        """
        Получить список доступных опций для предшественника
        
        GET /api/v1/trial-plans/predecessor-options/
        
        Returns:
        {
            "fallow": "Fallow (Пар)",
            "cultures": [
                {"id": 1, "name": "Wheat", "patents_id": 100},
                {"id": 2, "name": "Barley", "patents_id": 101}
            ]
        }
        """
        # Получаем список культур из локальной базы
        from trials_app.models import Culture
        cultures = Culture.objects.filter(is_deleted=False).order_by('name')
        
        culture_options = []
        for culture in cultures:
            culture_options.append({
                'id': culture.id,
                'name': culture.name,
                'patents_id': culture.culture_id
            })
        
        return Response({
            'fallow': 'Fallow (Пар)',
            'cultures': culture_options
        })
    
    @action(detail=True, methods=['get'], url_path='cultures')
    def get_cultures(self, request, pk=None):
        """
        Получить список культур в плане
        
        GET /api/v1/trial-plans/{id}/cultures/
        
        Returns:
        [
            {
                "id": 1,
                "culture": 5,
                "culture_name": "Пшеница",
                "culture_group": "Зерновые",
                "created_by": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        ]
        """
        trial_plan = self.get_object()
        cultures = TrialPlanCulture.objects.filter(
            trial_plan=trial_plan, 
            is_deleted=False
        ).order_by('culture__name')
        
        serializer = TrialPlanCultureSerializer(cultures, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='add-culture')
    def add_culture(self, request, pk=None):
        """
        Добавить культуру в план
        
        POST /api/v1/trial-plans/{id}/add-culture/
        
        Body:
        {
            "culture_id": 5
        }
        
        Returns:
        {
            "id": 1,
            "culture": 5,
            "culture_name": "Пшеница",
            "culture_group": "Зерновые",
            "created_by": 1,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        """
        trial_plan = self.get_object()
        serializer = TrialPlanAddCultureSerializer(data=request.data)
        
        if serializer.is_valid():
            culture_id = serializer.validated_data['culture_id']
            
            # Проверяем, не добавлена ли уже эта культура
            existing = TrialPlanCulture.objects.filter(
                trial_plan=trial_plan,
                culture_id=culture_id,
                is_deleted=False
            ).exists()
            
            if existing:
                return Response(
                    {'error': 'Культура уже добавлена в план'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создаем связь
            trial_plan_culture = TrialPlanCulture.objects.create(
                trial_plan=trial_plan,
                culture_id=culture_id,
                created_by=request.user
            )
            
            response_serializer = TrialPlanCultureSerializer(trial_plan_culture)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='remove-culture/(?P<culture_id>[^/.]+)')
    def remove_culture(self, request, pk=None, culture_id=None):
        """
        Удалить культуру из плана
        
        DELETE /api/v1/trial-plans/{id}/remove-culture/{culture_id}/
        
        Returns:
        {
            "message": "Культура удалена из плана"
        }
        """
        trial_plan = self.get_object()
        
        try:
            trial_plan_culture = TrialPlanCulture.objects.get(
                trial_plan=trial_plan,
                culture_id=culture_id,
                is_deleted=False
            )
            trial_plan_culture.delete()  # Soft delete
            return Response({'message': 'Культура удалена из плана'})
        
        except TrialPlanCulture.DoesNotExist:
            return Response(
                {'error': 'Культура не найдена в плане'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], url_path='cultures/(?P<culture_id>[^/.]+)/add-trial-type')
    def add_trial_type_to_culture(self, request, pk=None, culture_id=None):
        """
        Добавить тип испытания к культуре в плане
        
        POST /api/trial-plans/{id}/cultures/{culture_id}/add-trial-type/
        
        Body:
        {
            "trial_type_id": 1,
            "season": "spring"
        }
        
        Returns:
        {
            "id": 1,
            "trial_type_id": 1,
            "trial_type_name": "КСИ",
            "season": "spring",
            "participants": [],
            "created_by": 1,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        """
        trial_plan = self.get_object()
        
        # Проверяем что культура существует в плане
        try:
            trial_plan_culture = TrialPlanCulture.objects.get(
                trial_plan=trial_plan,
                culture_id=culture_id,
                is_deleted=False
            )
        except TrialPlanCulture.DoesNotExist:
            return Response(
                {'error': 'Культура не найдена в плане'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        trial_type_id = request.data.get('trial_type_id')
        season = request.data.get('season', 'spring')
        
        if not trial_type_id:
            return Response(
                {'error': 'trial_type_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем, не добавлен ли уже этот тип испытания
        existing = TrialPlanCultureTrialType.objects.filter(
            trial_plan_culture=trial_plan_culture,
            trial_type_id=trial_type_id,
            is_deleted=False
        ).exists()
        
        if existing:
            return Response(
                {'error': 'Этот тип испытания уже добавлен к культуре'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем что trial_type существует
        try:
            trial_type = TrialType.objects.get(id=trial_type_id, is_deleted=False)
        except TrialType.DoesNotExist:
            return Response(
                {'error': 'Тип испытания не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Создаем связь
        culture_trial_type = TrialPlanCultureTrialType.objects.create(
            trial_plan_culture=trial_plan_culture,
            trial_type=trial_type,
            season=season,
            created_by=request.user
        )
        
        # Формируем ответ
        response_data = {
            'id': culture_trial_type.id,
            'trial_type_id': trial_type.id,
            'trial_type_name': trial_type.name,
            'season': culture_trial_type.season,
            'participants': [],
            'created_by': request.user.id,
            'created_at': culture_trial_type.created_at,
            'updated_at': culture_trial_type.updated_at
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='cultures/(?P<culture_id>[^/.]+)/trial-types/(?P<trial_type_id>[^/.]+)/add-participant')
    def add_participant_to_trial_type(self, request, pk=None, culture_id=None, trial_type_id=None):
        """
        Добавить участника к типу испытания культуры в плане
        
        POST /api/trial-plans/{id}/cultures/{culture_id}/trial-types/{trial_type_id}/add-participant/
        
        Body:
        {
            "patents_sort_id": 1774,
            "statistical_group": 0,
            "seeds_provision": "provided",
            "maturity_group": "D03",
            "application_id": 22
        }
        
        Returns:
        {
            "id": 1,
            "patents_sort_id": 1774,
            "statistical_group": 0,
            "seeds_provision": "provided",
            "maturity_group": "D03",
            "participant_number": 1,
            "application_id": 22,
            "created_by": 1,
            "created_at": "2024-01-01T00:00:00Z"
        }
        """
        trial_plan = self.get_object()
        
        # Проверяем что культура существует в плане
        try:
            trial_plan_culture = TrialPlanCulture.objects.get(
                trial_plan=trial_plan,
                culture_id=culture_id,
                is_deleted=False
            )
        except TrialPlanCulture.DoesNotExist:
            return Response(
                {'error': 'Культура не найдена в плане'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Проверяем что тип испытания существует для этой культуры
        try:
            culture_trial_type = TrialPlanCultureTrialType.objects.get(
                trial_plan_culture=trial_plan_culture,
                trial_type_id=trial_type_id,
                is_deleted=False
            )
        except TrialPlanCultureTrialType.DoesNotExist:
            return Response(
                {'error': 'Тип испытания не найден для данной культуры в плане'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Валидируем данные участника
        required_fields = ['patents_sort_id']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Поле {field} обязательно'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        patents_sort_id = request.data['patents_sort_id']
        
        # Проверяем, не добавлен ли уже этот сорт как участник
        existing_participant = TrialPlanParticipant.objects.filter(
            culture_trial_type=culture_trial_type,
            patents_sort_id=patents_sort_id,
            is_deleted=False
        ).first()
        
        if existing_participant:
            return Response(
                {'error': 'Этот сорт уже добавлен как участник'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Автоматически генерируем participant_number
        max_number = TrialPlanParticipant.objects.filter(
            culture_trial_type=culture_trial_type,
            is_deleted=False
        ).aggregate(max_num=django_models.Max('participant_number'))['max_num'] or 0
        participant_number = max_number + 1
        
        # Получаем application если указан
        application_id = request.data.get('application_id')
        application_obj = None
        if application_id:
            try:
                from .models import Application
                application_obj = Application.objects.get(id=application_id)
            except Application.DoesNotExist:
                return Response(
                    {'error': f'Application with ID {application_id} not found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Создаем участника
        try:
            participant = TrialPlanParticipant.objects.create(
                culture_trial_type=culture_trial_type,
                patents_sort_id=patents_sort_id,
                statistical_group=request.data.get('statistical_group', 1),
                seeds_provision=request.data.get('seeds_provision', 'not_provided'),
                participant_number=participant_number,
                maturity_group=request.data.get('maturity_group', ''),
                application=application_obj,
                created_by=request.user
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to create participant: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Формируем ответ
        response_data = {
            'id': participant.id,
            'patents_sort_id': participant.patents_sort_id,
            'statistical_group': participant.statistical_group,
            'seeds_provision': participant.seeds_provision,
            'maturity_group': participant.maturity_group,
            'participant_number': participant.participant_number,
            'application_id': participant.application.id if participant.application else None,
            'created_by': request.user.id,
            'created_at': participant.created_at,
            'updated_at': participant.updated_at
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='create-trial')
    def create_trial(self, request, pk=None):
        """
        Создать Trial из плана для конкретного ГСУ и культуры
        
        ВАЖНО: Создает ОТДЕЛЬНОЕ ИСПЫТАНИЕ для каждой группы спелости!
        Согласно методике формы 008: "Форма заполняется строго для одной группы спелости"
        
        POST /api/v1/trial-plans/{id}/create-trial/
        {
            "region_id": 1,
            "culture_id": 5,
            "area_ha": 0.5,
            "responsible_person": "Иванов И.И.",
            "start_date": "2025-03-15",  // опционально - дата начала испытания (по умолчанию текущая дата)
            "exclude_participants": [123, 456],  // опционально - ID участников для исключения
            "maturity_groups": [  // опционально - если не указано, создаст для всех найденных групп
                {
                    "code": "D03",
                    "name": "Средний (среднеспелый)"
                },
                {
                    "code": "D07", 
                    "name": "Среднеранний"
                }
            ]
        }
        
        Response:
        {
            "success": true,
            "trials_created": 2,
            "trials": [
                {
                    "trial_id": 20,
                    "maturity_group_code": "D03",
                    "maturity_group_name": "Средний (среднеспелый)",
                    "total_participants": 5,
                    "status": "active"
                },
                {
                    "trial_id": 21,
                    "maturity_group_code": "D07", 
                    "maturity_group_name": "Среднеранний",
                    "total_participants": 6,
                    "status": "active"
                }
            ],
            "message": "Created 2 trials for different maturity groups"
        }
        """
        trial_plan = self.get_object()
        
        region_id = request.data.get('region_id')
        culture_id = request.data.get('culture_id')
        area_ha = request.data.get('area_ha')
        responsible_person = request.data.get('responsible_person')
        exclude_participants = request.data.get('exclude_participants', [])
        start_date = request.data.get('start_date')
        maturity_groups = request.data.get('maturity_groups', [])
        
        if not region_id or not culture_id:
            return Response({
                'error': 'region_id and culture_id are required'
            }, status=400)
        
        # Проверить регион и культуру
        try:
            region = Region.objects.get(id=region_id, is_deleted=False)
            culture = Culture.objects.get(id=culture_id, is_deleted=False)
        except (Region.DoesNotExist, Culture.DoesNotExist):
            return Response({'error': 'Region or Culture not found'}, status=404)
        
        # Проверить что культура есть в плане
        culture_in_plan = TrialPlanCulture.objects.filter(
            trial_plan=trial_plan,
            culture=culture,
            is_deleted=False
        ).exists()
        
        if not culture_in_plan:
            return Response({
                'error': f'Culture {culture.name} not found in this plan'
            }, status=400)
        
        # Найти участников плана для этого ГСУ и культуры
        trial_plan_trials = TrialPlanTrial.objects.filter(
            participant__culture_trial_type__trial_plan_culture__trial_plan=trial_plan,
            region=region,
            is_deleted=False
        ).select_related('participant').prefetch_related('participant__trials')
        
        if not trial_plan_trials.exists():
            return Response({
                'error': f'No participants found in plan for region {region.name} and culture {culture.name}'
            }, status=400)
        
        # === СГРУППИРОВАТЬ УЧАСТНИКОВ ПО ГРУППАМ СПЕЛОСТИ ===
        participants_by_maturity_group = {}
        
        for plan_trial in trial_plan_trials:
            participant = plan_trial.participant
            
            # Исключить участников из списка exclude_participants
            if participant.patents_sort_id in exclude_participants:
                continue
            
            # Получить сорт и проверить культуру
            sort_record, _ = SortRecord.objects.get_or_create(
                sort_id=participant.patents_sort_id,
                defaults={'name': f'Сорт {participant.patents_sort_id}'}
            )
            
            # Синхронизировать если нужно
            if not sort_record.culture:
                sort_record.sync_from_patents()
            
            # Проверить что культура совпадает
            if sort_record.culture and sort_record.culture.id != culture.id:
                continue
            
            # Получить группу спелости из заявки или сорта
            maturity_group_code = self._get_maturity_group_code(participant, sort_record)
            
            # Группировать по коду группы спелости
            if maturity_group_code not in participants_by_maturity_group:
                participants_by_maturity_group[maturity_group_code] = []
            
            # Избегаем дубликатов внутри группы
            existing_sort_ids = {p['participant'].patents_sort_id for p in participants_by_maturity_group[maturity_group_code]}
            if participant.patents_sort_id not in existing_sort_ids:
                participants_by_maturity_group[maturity_group_code].append({
                    'participant': participant,
                    'sort_record': sort_record,
                    'plan_trial': plan_trial,
                    'maturity_group_code': maturity_group_code
                })
        
        if not participants_by_maturity_group:
            return Response({
                'error': f'No matching participants found for culture {culture.name}'
            }, status=400)
        
        # === СОЗДАТЬ ОТДЕЛЬНОЕ ИСПЫТАНИЕ ДЛЯ КАЖДОЙ ГРУППЫ СПЕЛОСТИ ===
        created_trials = []
        
        # Если указаны конкретные группы спелости - использовать их
        if maturity_groups:
            groups_to_create = maturity_groups
        else:
            # Создать для всех найденных групп
            groups_to_create = []
            for group_code, participants in participants_by_maturity_group.items():
                groups_to_create.append({
                    'code': group_code,
                    'name': self._get_maturity_group_name(group_code)
                })
        
        for group_info in groups_to_create:
            group_code = group_info['code']
            group_name = group_info['name']
            
            # Получить участников для этой группы спелости
            group_participants = participants_by_maturity_group.get(group_code, [])
            
            if not group_participants:
                continue  # Пропускаем пустые группы
            
            # Взять параметры из первого участника группы
            first_plan_trial = group_participants[0]['plan_trial']
            trial_start_date = start_date or timezone.now().date()
            
            # Создать Trial для этой группы спелости
            trial = Trial.objects.create(
                region=region,
                culture=culture,
                trial_type=first_plan_trial.trial_type or trial_plan.trial_type,
                area_ha=area_ha,
                year=trial_plan.year,
                planting_season=first_plan_trial.season,
                predecessor_culture=self._get_predecessor_culture(first_plan_trial.predecessor),
                growing_conditions='rainfed',
                cultivation_technology='traditional',
                responsible_person=responsible_person,
                trial_plan=trial_plan,
                status='active',
                start_date=trial_start_date,
                created_by=request.user,
                
                # ФОРМА 008: Группа спелости (КРИТИЧНО!)
                maturity_group_code=group_code,
                maturity_group_name=group_name,
                
                # Коды для отчетности
                trial_code=f"{region.name[:3].upper()}-{trial_plan.year}-{group_code}",
                culture_code=culture.name[:3].upper(),
                predecessor_code=first_plan_trial.predecessor or "ПАР"
            )
            
            # Автоматически назначить только ОБЯЗАТЕЛЬНЫЕ показатели по культуре
            if culture.group_culture:
                required_indicators = Indicator.objects.filter(
                    group_cultures=culture.group_culture,
                    is_required=True,  # Только обязательные показатели
                    is_deleted=False
                ).distinct()
                trial.indicators.set(required_indicators)
            
            # Создать участников для этой группы спелости
            created_participants = []
            for idx, p_info in enumerate(group_participants, start=1):
                participant = p_info['participant']
                sort_record = p_info['sort_record']
                
                trial_participant = TrialParticipant.objects.create(
                    trial=trial,
                    sort_record=sort_record,
                    statistical_group=participant.statistical_group,
                    participant_number=idx,
                    application_id=participant.application.id if participant.application else None,
                    
                    # ФОРМА 008: Код группы спелости участника
                    maturity_group_code=group_code
                )
                created_participants.append(trial_participant)
                
                # Автоматически создать пустые результаты для основных показателей
                create_basic_trial_results(trial_participant, request.user)
            
            # Обновить статус заявок
            application_ids = set()
            for tp in created_participants:
                if tp.application_id:
                    application_ids.add(tp.application_id)
            
            if application_ids:
                Application.objects.filter(
                    id__in=application_ids,
                    status='distributed'
                ).update(status='in_progress')
            
            created_trials.append({
                'trial_id': trial.id,
                'maturity_group_code': group_code,
                'maturity_group_name': group_name,
                'total_participants': len(created_participants),
                'status': trial.status,
                'trial': TrialSerializer(trial).data
            })
        
        if not created_trials:
            return Response({
                'error': 'No trials were created. Check maturity groups configuration.'
            }, status=400)
        
        return Response({
            'success': True,
            'trials_created': len(created_trials),
            'trials': created_trials,
            'message': f'Created {len(created_trials)} trial(s) for different maturity groups'
        })
    
    def _get_maturity_group_code(self, participant, sort_record):
        """
        Определить код группы спелости для участника
        
        Приоритет:
        1. Из заявки (application.maturity_group)
        2. Из сорта (sort_record.maturity_group)
        3. По умолчанию "D01"
        
        Args:
            participant: TrialPlanParticipant
            sort_record: SortRecord
            
        Returns:
            str: код группы спелости (D01, D03, D07...)
        """
        # 1. Попробовать из заявки
        if participant.application and hasattr(participant.application, 'maturity_group'):
            maturity_group = participant.application.maturity_group
            if maturity_group:
                # Извлечь код из строки типа "D07 - Среднеспелая группа"
                if isinstance(maturity_group, str) and '-' in maturity_group:
                    code = maturity_group.split('-')[0].strip()
                    if code.startswith('D') and code[1:].isdigit():
                        return code
                elif isinstance(maturity_group, str) and maturity_group.startswith('D'):
                    return maturity_group
        
        # 2. Попробовать из сорта
        if sort_record and hasattr(sort_record, 'maturity_group'):
            maturity_group = sort_record.maturity_group
            if maturity_group:
                if isinstance(maturity_group, str) and '-' in maturity_group:
                    code = maturity_group.split('-')[0].strip()
                    if code.startswith('D') and code[1:].isdigit():
                        return code
                elif isinstance(maturity_group, str) and maturity_group.startswith('D'):
                    return maturity_group
        
        # 3. По умолчанию
        return "D01"
    
    def _get_maturity_group_name(self, group_code):
        """
        Получить название группы спелости по коду
        
        Args:
            group_code: str - код группы (D01, D02, D03...)
            
        Returns:
            str: название группы спелости
        """
        group_names = {
            "D01": "Очень ранний (ультраранний)",
            "D02": "Ранний (раннеспелый)",
            "D03": "Средний (среднеспелый)",
            "D04": "Поздний (позднеспелый)",
            "D05": "Очень поздний",
            "D06": "От очень раннего до раннего",
            "D07": "Среднеранний",
            "D08": "Среднепоздний",
            "D09": "От позднего до очень позднего",
            "D10": "Ремонтантный"
        }
        
        return group_names.get(group_code, f"Группа спелости {group_code}")
    
    def _get_predecessor_culture(self, predecessor_value):
        """
        Получить Culture объект предшественника
        
        Args:
            predecessor_value: 'fallow' или ID культуры
        
        Returns:
            Culture object или None
        """
        if predecessor_value == 'fallow':
            return None
        
        if isinstance(predecessor_value, int):
            try:
                return Culture.objects.get(id=predecessor_value, is_deleted=False)
            except Culture.DoesNotExist:
                return None
        
        return None
    
    @action(detail=False, methods=['get'], url_path='my-tasks')
    def my_tasks(self, request):
        """
        Получить задачи для агронома/филиала
        
        GET /api/v1/trial-plans/my-tasks/?region_id=1&year=2025
        
        Показывает какие Trial нужно создать из плана для конкретного ГСУ
        """
        region_id = request.query_params.get('region_id')
        year = request.query_params.get('year')
        
        if not region_id:
            return Response({
                'error': 'region_id is required'
            }, status=400)
        
        try:
            region = Region.objects.get(id=region_id, is_deleted=False)
        except Region.DoesNotExist:
            return Response({'error': 'Region not found'}, status=404)
        
        # Найти планы для области региона
        plans_query = TrialPlan.objects.filter(
            oblast=region.oblast,
            is_deleted=False
        )
        
        if year:
            plans_query = plans_query.filter(year=year)
        
        tasks = []
        
        for plan in plans_query:
            try:
                # Найти культуры в плане
                plan_cultures = TrialPlanCulture.objects.filter(
                    trial_plan=plan,
                    is_deleted=False
                ).select_related('culture')
                
                for plan_culture in plan_cultures:
                    culture = plan_culture.culture
                    
                    try:
                        # Упрощенный подсчет участников - просто считаем всех участников плана для культуры
                        participants_count = TrialPlanParticipant.objects.filter(
                            culture_trial_type__trial_plan_culture__trial_plan=plan,
                            culture_trial_type__trial_plan_culture__culture=culture,
                            is_deleted=False
                        ).count()
                        
                        if participants_count == 0:
                            continue
                        
                        # Проверить создан ли уже Trial
                        existing_trial = Trial.objects.filter(
                            trial_plan=plan,
                            region=region,
                            culture=culture,
                            is_deleted=False
                        ).first()
                        
                        task_data = {
                            'plan_id': plan.id,
                            'plan_year': plan.year,
                            'culture_id': culture.id,
                            'culture_name': culture.name,
                            'culture_group': culture.group_culture.name if culture.group_culture else None,
                            'participants_count': participants_count,
                            'trial_created': existing_trial is not None,
                            'trial_id': existing_trial.id if existing_trial else None,
                            'trial_status': existing_trial.status if existing_trial else None,
                            'can_start': existing_trial is None  # Можно начать если еще не создан
                        }
                        
                        tasks.append(task_data)
                    except Exception as e:
                        # Пропускаем проблемные культуры
                        continue
            except Exception as e:
                # Пропускаем проблемные планы
                continue
        
        return Response({
            'region_id': region.id,
            'region_name': region.name,
            'oblast_id': region.oblast.id,
            'oblast_name': region.oblast.name,
            'year': year,
            'total_tasks': len(tasks),
            'tasks': tasks
        })


# ============================================================================
# ГОДОВЫЕ ОТЧЕТЫ И РЕШЕНИЯ (НОВАЯ ЛОГИКА)
# ============================================================================




