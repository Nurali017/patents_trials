"""
Trial ViewSets
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


class TrialViewSet(viewsets.ModelViewSet):
    """
    Управление испытаниями сортов
    
    Сорта связываются через sort_id из Patents Service
    Культуры получаются через API (не хранятся локально)
    """
    queryset = Trial.objects.filter(is_deleted=False)
    serializer_class = TrialSerializer
    
    def get_permissions(self):
        """Чтение, список сортов - всем, остальное - только авторизованным"""
        if self.action in ['list', 'retrieve', 'available_sorts', 'form008', 'form008_statistics']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """При создании испытания устанавливаем created_by"""
        from django.core.exceptions import ObjectDoesNotExist
        from rest_framework.exceptions import ValidationError
        
        try:
            serializer.save(created_by=self.request.user)
        except ObjectDoesNotExist as e:
            # Понятное сообщение об отсутствующем объекте
            raise ValidationError({
                'error': f'Связанный объект не найден: {str(e)}'
            })
        except Exception as e:
            # Логируем ошибку для отладки
            import traceback
            error_msg = str(e)
            print(f"Error creating trial: {error_msg}")
            print(traceback.format_exc())
            
            # Более понятное сообщение для пользователя
            if 'foreign key constraint' in error_msg.lower() or 'does not exist' in error_msg.lower():
                raise ValidationError({
                    'error': 'Один или несколько указанных ID не существуют в базе данных',
                    'details': error_msg
                })
            raise
    
    @action(detail=False, methods=['get'], url_path='available-sorts')
    def available_sorts(self, request):
        """
        Получить список доступных сортов из Patents Service
        
        Проксирует запрос к Patents Service API для получения списка сортов.
        Используется фронтендом для выбора сорта при создании испытания.
        
        GET /api/v1/trials/available-sorts/
        """
        sorts = patents_api.get_all_sorts(params=request.query_params.dict())
        return Response(sorts)
    
    @action(detail=False, methods=['post'], url_path='validate-sort')
    def validate_sort(self, request):
        """
        Валидировать сорт перед созданием испытания
        
        Проверяет существование сорта в Patents Service и возвращает
        данные для денормализации.
        
        POST /api/v1/trials/validate-sort/
        Body: {"sort_id": 456}
        
        Returns:
            {
                "valid": true,
                "data": {
                    "sort_id": 456,
                    "sort_name": "Пшеница Акмола 3",
                    "culture_id": 1,
                    "culture_name": "Пшеница яровая"
                }
            }
        """
        sort_id = request.data.get('sort_id')
        if not sort_id:
            return Response({
                'valid': False,
                'error': 'sort_id required'
            }, status=400)
        
        sort_data = patents_api.validate_sort_for_trial(sort_id)
        if sort_data:
            return Response({
                'valid': True,
                'data': sort_data
            })
        else:
            return Response({
                'valid': False,
                'error': f'Sort with ID {sort_id} not found in Patents Service'
            }, status=404)
    
    @action(detail=True, methods=['post'], url_path='decision')
    def make_decision(self, request, pk=None):
        """
        Принять решение по испытанию
        
        После принятия решения автоматически обновляется статус заявки.
        
        POST /api/v1/trials/{id}/decision/
        Body: {
            "decision": "approved",  # approved | continue | rejected
            "justification": "Сорт показал отличные результаты...",
            "recommendations": "Рекомендовать к включению в реестр",
            "decision_date": "2025-10-01"
        }
        """
        trial = self.get_object()
        
        # Проверяем что испытание завершено
        if trial.status not in ['completed', 'lab_completed', 'completed_008']:
            return Response({
                'error': 'Trial must be completed before making decision'
            }, status=400)
        
        decision = request.data.get('decision')
        if decision not in ['approved', 'continue', 'rejected']:
            return Response({
                'error': 'Invalid decision. Must be: approved, continue, or rejected'
            }, status=400)
        
        # Сохраняем решение
        trial.decision = decision
        trial.decision_justification = request.data.get('justification', '')
        trial.decision_recommendations = request.data.get('recommendations', '')
        trial.decision_date = request.data.get('decision_date', timezone.now().date())
        trial.decided_by = request.user if request.user.is_authenticated else None
        
        # Обновляем статус испытания
        trial.status = decision  # approved, continue, или rejected
        trial.save()
        
        # АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ PlannedDistribution (многолетние испытания):
        # Ищем PlannedDistribution через участников
        from trials_app.models import TrialParticipant
        participants_with_app = TrialParticipant.objects.filter(
            trial=trial,
            application__isnull=False,
            is_deleted=False
        ).select_related('application')
        
        for participant in participants_with_app:
            planned_dist = PlannedDistribution.objects.filter(
                application=participant.application,
                region=trial.region,
                status='in_progress'
            ).first()
            
            if planned_dist:
                # Финальное решение: approved или rejected → завершаем PlannedDistribution
                if decision in ['approved', 'rejected']:
                    planned_dist.status = decision  # approved или rejected
                    planned_dist.year_completed = trial.year or (trial.start_date.year if trial.start_date else None)
                    planned_dist.save()
                # decision = 'continue' → оставляем in_progress (будет новый Trial в следующем году)
        
        return Response({
            'success': True,
            'message': f'Decision "{decision}" saved successfully',
            'trial': TrialSerializer(trial).data
        })
    
    @action(detail=True, methods=['post'], url_path='mark-sent-to-lab')
    def mark_sent_to_lab(self, request, pk=None):
        """
        Отметить что образец отправлен в лабораторию
        
        POST /api/v1/trials/{id}/mark-sent-to-lab/
        Body: {
            "laboratory_code": "LAB-2025-001-ALM",
            "sample_weight_kg": 2.0,
            "sent_date": "2025-10-15",
            "participant_id": 50,  # опционально - от какого участника образец
            "sample_source": "Образец из делянки №2"
        }
        """
        trial = self.get_object()
        
        # Проверка что испытание в статусе completed_008
        if trial.status != 'completed_008':
            return Response({
                'error': f'Trial must be in status completed_008 before sending to lab. Current status: {trial.status}'
            }, status=400)
        
        # Обновляем данные
        trial.laboratory_status = 'sent'
        trial.laboratory_code = request.data.get('laboratory_code')
        trial.laboratory_sent_date = request.data.get('sent_date', timezone.now().date())
        trial.laboratory_sample_weight = request.data.get('sample_weight_kg')
        trial.laboratory_sample_source = request.data.get('sample_source', '')
        trial.laboratory_notes = request.data.get('notes', '')
        trial.status = 'lab_sample_sent'
        trial.save()
        
        # АВТОМАТИЧЕСКИ СОЗДАТЬ КАЧЕСТВЕННЫЕ ПОКАЗАТЕЛИ ДЛЯ ЛАБОРАТОРИИ
        quality_results = create_quality_trial_results(trial, request.user)
        
        return Response({
            'success': True,
            'message': f'Sample {trial.laboratory_code} marked as sent to laboratory',
            'quality_indicators_created': len(quality_results),
            'trial': TrialSerializer(trial).data
        })
    
    @action(detail=True, methods=['post'], url_path='laboratory-results/bulk-entry')
    def laboratory_results_bulk_entry(self, request, pk=None):
        """
        Массовое внесение лабораторных результатов
        
        POST /api/v1/trials/{id}/laboratory-results/bulk-entry/
        Body: {
            "laboratory_code": "LAB-2025-001-ALM",
            "analysis_date": "2025-10-20",
            "participant_id": 50,  # опционально - для какого участника
            "results": [
                {
                    "indicator": 10,  # ID показателя (должен быть is_quality=True)
                    "value": 14.5
                },
                {
                    "indicator": 11,
                    "value": 28.0
                },
                {
                    "indicator": 12,
                    "value": 785
                }
            ]
        }
        """
        trial = self.get_object()
        
        # Проверка статуса
        if trial.laboratory_status != 'sent':
            return Response({
                'error': f'Trial must have laboratory_status=sent. Current: {trial.laboratory_status}'
            }, status=400)
        
        laboratory_code = request.data.get('laboratory_code')
        analysis_date = request.data.get('analysis_date', timezone.now().date())
        participant_id = request.data.get('participant_id')
        results_data = request.data.get('results', [])
        
        if not results_data:
            return Response({
                'error': 'No results provided'
            }, status=400)
        
        # Проверить participant если указан
        participant = None
        if participant_id:
            try:
                participant = TrialParticipant.objects.get(id=participant_id, trial=trial)
            except TrialParticipant.DoesNotExist:
                return Response({
                    'error': f'Participant {participant_id} not found in this trial'
                }, status=404)
        
        created_results = []
        updated_results = []
        
        for item in results_data:
            indicator_id = item.get('indicator')
            value = item.get('value')
            text_value = item.get('text_value')
            
            if not indicator_id:
                continue
            
            # Проверить что показатель существует и is_quality=True
            try:
                indicator = Indicator.objects.get(id=indicator_id)
                if not indicator.is_quality:
                    return Response({
                        'error': f'Indicator "{indicator.name}" is not a quality indicator (is_quality=False)'
                    }, status=400)
            except Indicator.DoesNotExist:
                return Response({
                    'error': f'Indicator {indicator_id} not found'
                }, status=404)
            
            # Создать или обновить результат
            result, created = TrialLaboratoryResult.objects.update_or_create(
                trial=trial,
                indicator=indicator,
                participant=participant,
                defaults={
                    'value': value,
                    'text_value': text_value,
                    'laboratory_code': laboratory_code,
                    'analysis_date': analysis_date,
                    'created_by': request.user
                }
            )
            
            if created:
                created_results.append(result)
            else:
                updated_results.append(result)
        
        return Response({
            'success': True,
            'created': len(created_results),
            'updated': len(updated_results),
            'total': len(results_data)
        })
    
    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """
        Завершить полевые работы
        
        POST /api/trials/{id}/complete/
        Body: {
            "completed_date": "2025-10-22"  # опционально
        }
        
        Переводит испытание в статус 'completed' (испытание полностью завершено).
        Это финальный статус после всех этапов.
        """
        trial = self.get_object()
        
        # Проверка текущего статуса - можно завершить из любого статуса
        if trial.status in ['approved', 'continue', 'rejected']:
            return Response({
                'error': f'Trial already has final decision. Current: {trial.status}'
            }, status=400)
        
        # Обновляем статус
        trial.status = 'completed'
        if 'completed_date' in request.data:
            # Если пользователь хочет установить кастомную дату
            from datetime.datetime import strptime
            completed_date = request.data['completed_date']
        else:
            completed_date = None
        
        trial.save()
        
        return Response({
            'success': True,
            'message': 'Trial completed successfully',
            'trial': TrialSerializer(trial).data
        })
    
    @action(detail=True, methods=['post'], url_path='laboratory-complete')
    def laboratory_complete(self, request, pk=None):
        """
        Завершить лабораторные анализы
        
        POST /api/v1/trials/{id}/laboratory-complete/
        Body: {
            "completed_date": "2025-10-22"  # опционально
        }
        """
        trial = self.get_object()
        
        # Проверка статуса
        if trial.laboratory_status != 'sent':
            return Response({
                'error': f'Trial must have laboratory_status=sent. Current: {trial.laboratory_status}'
            }, status=400)
        
        # Обновляем статусы
        trial.laboratory_status = 'completed'
        trial.laboratory_completed_date = request.data.get('completed_date', timezone.now().date())
        trial.status = 'lab_completed'
        trial.save()
        
        return Response({
            'success': True,
            'message': 'Laboratory analyses completed',
            'trial': TrialSerializer(trial).data
        })
    
    @action(detail=True, methods=['post'], url_path='lcomplete')
    def lcomplete(self, request, pk=None):
        """
        Завершить испытание (финальное завершение после лабораторных анализов)
        
        POST /api/trials/{id}/lcomplete/
        Body: {
            "completed_date": "2025-10-22"  # опционально
        }
        
        Переводит испытание из статуса 'lab_completed' в финальный статус 'completed'.
        После этого можно принимать решение комиссии.
        """
        trial = self.get_object()
        
        # Проверка текущего статуса
        if trial.status != 'lab_completed':
            return Response({
                'error': f'Trial must be in status lab_completed. Current: {trial.status}'
            }, status=400)
        
        # Обновляем статус на финальный completed
        trial.status = 'completed'
        trial.save()
        
        return Response({
            'success': True,
            'message': 'Trial completed successfully',
            'trial': TrialSerializer(trial).data
        })
    
    @action(detail=True, methods=['get'], url_path='laboratory-results')
    def get_laboratory_results(self, request, pk=None):
        """
        Получить лабораторные результаты испытания
        
        GET /api/v1/trials/{id}/laboratory-results/
        """
        trial = self.get_object()
        
        results = TrialLaboratoryResult.objects.filter(
            trial=trial,
            is_deleted=False
        )
        
        serializer = TrialLaboratoryResultSerializer(results, many=True)
        
        return Response({
            'trial_id': trial.id,
            'laboratory_status': trial.laboratory_status,
            'laboratory_code': trial.laboratory_code,
            'results_count': results.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'], url_path='form008')
    def form008(self, request, pk=None):
        """
        Получить форму 008 для заполнения результатов испытания
        
        GET /api/v1/trials/{id}/form008/
        
        Возвращает:
        - Организационную информацию (шапка формы)
        - Участников (СНАЧАЛА стандарт, потом испытываемые)
        - Показатели для данной культуры
        - Предупреждения (если не заполнены критические поля)
        """
        trial = self.get_object()
        
        # === КРИТИЧЕСКИЕ ПРОВЕРКИ ===
        warnings = []
        
        # Проверка 1: группа спелости
        if not trial.maturity_group_code and not trial.maturity_group_name:
            warnings.append({
                'level': 'error',
                'message': '⚠️ КРИТИЧНО: Группа спелости не указана! Форма 008 заполняется СТРОГО для одной группы спелости.'
            })
        
        # Проверка 2: НСР
        if not trial.lsd_095:
            warnings.append({
                'level': 'warning',
                'message': '⚠️ НСР₀.₉₅ не введен. "Группа по стат. обработке" не может быть рассчитана.'
            })
        
        # Проверка 3: точность опыта
        if trial.accuracy_percent and trial.accuracy_percent > 4.0 and trial.replication_count == 4:
            warnings.append({
                'level': 'warning',
                'message': f'⚠️ Точность опыта P={trial.accuracy_percent}% превышает допустимое значение 4% при 4-кратной повторности.'
            })
        
        # === ПОЛУЧИТЬ УЧАСТНИКОВ (СТАНДАРТ ПЕРВЫМ!) ===
        # Сначала стандарты (statistical_group=0)
        standards = trial.participants.filter(is_deleted=False, statistical_group=0).order_by('participant_number')
        # Потом испытываемые (statistical_group=1)
        tested = trial.participants.filter(is_deleted=False, statistical_group=1).order_by('participant_number')
        
        participants_data = []
        
        # Добавить стандарты первыми
        for participant in standards:
            participants_data.append(self._format_participant_for_form008(participant))
        
        # Добавить испытываемые
        for participant in tested:
            participants_data.append(self._format_participant_for_form008(participant))
        
        # === ПОЛУЧИТЬ ПОКАЗАТЕЛИ для данной культуры ===
        indicators_data = []
        if trial.culture:
            indicators = trial.indicators.filter(
                is_deleted=False,
                is_quality=False  # Только основные показатели (не лабораторные)
            ).order_by('sort_order', 'name')
            
            for indicator in indicators:
                indicators_data.append({
                    'id': indicator.id,
                    'code': indicator.code,
                    'name': indicator.name,
                    'unit': indicator.unit,
                    'is_numeric': indicator.is_numeric,
                    'is_required': indicator.is_required,
                    'is_auto_calculated': indicator.is_auto_calculated,
                    'validation_rules': indicator.validation_rules,
                    'category': indicator.category,
                    'sort_order': indicator.sort_order
                })
        
        # Рассчитать min/max по каждому показателю
        min_max = {}
        for indicator in indicators:
            values = TrialResult.objects.filter(
                participant__trial=trial,
                indicator=indicator,
                value__isnull=False,
                is_deleted=False
            ).values_list('value', flat=True)
            
            if values:
                min_max[indicator.code] = {
                    'min': float(min(values)),
                    'max': float(max(values))
                }
            else:
                min_max[indicator.code] = {
                    'min': None,
                    'max': None
                }
        
        # Получить статистику (готовые значения, введенные вручную)
        statistics = trial.calculate_trial_statistics()
        
        return Response({
            'trial': {
                # Основная информация
                'id': trial.id,
                'year': trial.year or (trial.start_date.year if trial.start_date else None),
                
                # ФОРМА 008: Организационная информация
                'maturity_group_code': trial.maturity_group_code,
                'maturity_group_name': trial.maturity_group_name,
                'trial_code': trial.trial_code,
                'culture_code': trial.culture_code,
                'predecessor_code': trial.predecessor_code,
                
                # ГСУ и область
                'region_name': trial.region.name,
                'oblast_name': trial.region.oblast.name,
                
                # Культура
                'culture_name': trial.culture.name if trial.culture else None,
                'culture_group': trial.culture.group_culture.name if trial.culture and trial.culture.group_culture else None,
                'culture_id': trial.culture.id if trial.culture else None,
                'patents_culture_id': trial.patents_culture_id,
                
                # Тип испытания
                'trial_type': trial.trial_type.name if trial.trial_type else 'КСИ',
                'trial_type_code': trial.trial_type.code if trial.trial_type else None,
                
                # Предшественник
                'predecessor': self._get_predecessor_display(trial),
                
                # Условия возделывания
                'agro_background': trial.get_agro_background_display() if trial.agro_background else None,
                'growing_conditions': trial.get_growing_conditions_display() if trial.growing_conditions else 'на богаре',
                'cultivation_technology': trial.get_cultivation_technology_display() if trial.cultivation_technology else 'обычная',
                'growing_method': trial.get_growing_method_display() if trial.growing_method else None,
                
                # Уборка
                'harvest_timing': trial.get_harvest_timing_display() if trial.harvest_timing else None,
                'harvest_date': trial.harvest_date,
                
                # Ответственный
                'responsible_person': trial.responsible_person,
                'responsible_person_title': trial.responsible_person_title,
                'approval_date': trial.approval_date,
                
                # Статус
                'status': trial.status,
                'status_display': trial.get_status_display()
            },
            'statistics': statistics or {
                'lsd_095': None,
                'error_mean': None,
                'accuracy_percent': None,
                'replication_count': 4,
                'has_data': False
            },
            'participants': participants_data,
            'indicators': indicators_data,
            'min_max': min_max,
            'warnings': warnings,
            'metadata': {
                'form_name': 'МСХ РК 008',
                'form_title': 'ОСНОВНЫЕ ПОКАЗАТЕЛИ ИСПЫТЫВАЕМЫХ СОРТОВ',
                'submission_deadline': '15 дней после уборки урожая',
                'note': 'Форма заполняется строго для одной группы спелости'
            }
        })
    
    def _format_participant_for_form008(self, participant):
        """
        Форматировать участника для формы 008
        
        Возвращает все данные участника включая результаты по делянкам
        """
        # Получить все результаты участника
        results = TrialResult.objects.filter(
            participant=participant,
            is_deleted=False
        ).select_related('indicator')
        
        current_results = {}
        for result in results:
            current_results[result.indicator.code] = {
                'value': result.value,
                'plot_1': result.plot_1,
                'plot_2': result.plot_2,
                'plot_3': result.plot_3,
                'plot_4': result.plot_4,
                'is_rejected': result.is_rejected,
                'rejection_reason': result.rejection_reason,
                'is_restored': result.is_restored,
                'text_value': result.text_value,
                'measurement_date': result.measurement_date
            }
        
        return {
            'id': participant.id,
            'participant_number': participant.participant_number,
            'sort_name': participant.sort_record.name if participant.sort_record else None,
            'sort_code': participant.sort_record.public_code if participant.sort_record else None,
            
            # ДВА РАЗНЫХ ПОЛЯ!
            'maturity_group_code': participant.maturity_group_code,  # Организационный
            'statistical_result': participant.statistical_result,    # Группа по стат. обработке (АВТОРАСЧЕТ)
            'statistical_result_display': participant.get_statistical_result_display(),
            
            'statistical_group': participant.statistical_group,
            'is_standard': participant.is_standard,
            'application_number': participant.application.application_number if participant.application else None,
            'current_results': current_results
        }
    
    def _get_predecessor_display(self, trial):
        """Получить отображение предшественника"""
        if trial.predecessor_culture:
            return trial.predecessor_culture.name
        return "пар"
    
    @action(detail=True, methods=['post'], url_path='form008/bulk-save')
    def form008_bulk_save(self, request, pk=None):
        """
        Массовое сохранение результатов формы 008
        
        POST /api/v1/trials/{id}/form008/bulk-save/
        {
            "is_final": false,
            "harvest_date": "2024-09-23",
            "measurement_date": "2024-09-23",
            
            // СТАТИСТИКА ОПЫТА (обязательно при is_final=true)
            "statistics": {
                "lsd_095": 5.2,
                "error_mean": 2.1,
                "accuracy_percent": 3.8,
                "replication_count": 4,
                "use_auto_calculation": false  // опционально - использовать авторасчет с делянок
            },
            
            "participants": [
                {
                    "participant_id": 50,
                    "results": {
                        "yield": {
                            // ВАРИАНТ 1: С делянками (опционально)
                            "plot_1": 84.5,
                            "plot_2": 86.1,
                            "plot_3": 85.0,
                            "plot_4": 85.6,
                            // value рассчитается автоматически
                            
                            // ВАРИАНТ 2: Сразу среднее
                            "value": 85.05
                        },
                        "seed_weight_1000": {
                            "value": 32.9
                        }
                    }
                }
            ]
        }
        """
        trial = self.get_object()
        
        # Проверка статуса
        if trial.status not in ['active', 'planned', 'completed_008']:
            return Response({
                'error': f'Cannot save results. Trial status is {trial.status}'
            }, status=400)
        
        is_final = request.data.get('is_final', False)
        harvest_date = request.data.get('harvest_date')
        measurement_date = request.data.get('measurement_date', harvest_date)
        
        # === ОБНОВИТЬ СТАТИСТИКУ ОПЫТА ===
        statistics = request.data.get('statistics', {})
        if statistics:
            # Если указан use_auto_calculation, получить авторасчет
            if statistics.get('use_auto_calculation', False):
                auto_stats = trial.calculate_auto_statistics_from_plots()
                if auto_stats:
                    trial.lsd_095 = statistics.get('lsd_095', auto_stats.get('auto_lsd_095'))
                    trial.error_mean = statistics.get('error_mean', auto_stats.get('auto_error_mean'))
                    trial.accuracy_percent = statistics.get('accuracy_percent', auto_stats.get('auto_accuracy_percent'))
                    trial.replication_count = statistics.get('replication_count', auto_stats.get('replication_count', 4))
                else:
                    return Response({
                        'error': 'Недостаточно данных с делянок для авторасчета. Введите значения вручную.'
                    }, status=400)
            else:
                # Обычный ручной ввод
                trial.lsd_095 = statistics.get('lsd_095')
                trial.error_mean = statistics.get('error_mean')
                trial.accuracy_percent = statistics.get('accuracy_percent')
                trial.replication_count = statistics.get('replication_count', 4)
        
        # Обновить harvest_date
        if harvest_date:
            trial.harvest_date = harvest_date
        
        trial.save()
        
        # Валидация: НСР обязателен при финальной отправке
        if is_final and not trial.lsd_095:
            return Response({
                'error': 'НСР₀.₉₅ обязателен для финальной отправки формы 008. Без НСР невозможно рассчитать "Группу по стат. обработке".'
            }, status=400)
        
        participants_data = request.data.get('participants', [])
        if not participants_data:
            return Response({
                'error': 'No participants data provided'
            }, status=400)
        
        results_created = 0
        results_updated = 0
        errors = []
        
        # === СОХРАНИТЬ РЕЗУЛЬТАТЫ ===
        for p_data in participants_data:
            participant_id = p_data.get('participant_id')
            results = p_data.get('results', {})
            
            if not participant_id:
                continue
            
            try:
                participant = TrialParticipant.objects.get(
                    id=participant_id,
                    trial=trial,
                    is_deleted=False
                )
            except TrialParticipant.DoesNotExist:
                errors.append(f'Participant {participant_id} not found')
                continue
            
            # Сохранить каждый показатель
            for indicator_code, result_data in results.items():
                try:
                    indicator = Indicator.objects.get(
                        code=indicator_code,
                        is_deleted=False
                    )
                except Indicator.DoesNotExist:
                    errors.append(f'Indicator {indicator_code} not found')
                    continue
                
                # Подготовить данные
                if isinstance(result_data, dict):
                    # Формат: {"value": 85.3, "plot_1": 84.5, ...}
                    value = result_data.get('value')
                    plot_1 = result_data.get('plot_1')
                    plot_2 = result_data.get('plot_2')
                    plot_3 = result_data.get('plot_3')
                    plot_4 = result_data.get('plot_4')
                    is_rejected = result_data.get('is_rejected', False)
                    rejection_reason = result_data.get('rejection_reason')
                    is_restored = result_data.get('is_restored', False)
                else:
                    # Формат: "yield": 85.3 (простое значение)
                    value = result_data
                    plot_1 = plot_2 = plot_3 = plot_4 = None
                    is_rejected = is_restored = False
                    rejection_reason = None
                
                # Валидация баллов (1-5, шаг 0.5)
                if indicator.unit == 'балл' and value is not None:
                    if value < 0 or value > 5:
                        errors.append(f'{indicator.name}: значение {value} вне допустимого диапазона (0-5 баллов)')
                        continue
                    # Проверка шага 0.5
                    if (value * 2) % 1 != 0:
                        errors.append(f'{indicator.name}: значение {value} должно иметь шаг 0.5 (например: 4.5)')
                        continue
                
                # Валидация по validation_rules
                if indicator.validation_rules and value is not None:
                    rules = indicator.validation_rules
                    
                    if 'min_value' in rules and value < rules['min_value']:
                        errors.append(f'{indicator.name}: значение {value} меньше минимального {rules["min_value"]}')
                        continue
                    
                    if 'max_value' in rules and value > rules['max_value']:
                        errors.append(f'{indicator.name}: значение {value} больше максимального {rules["max_value"]}')
                        continue
                
                # Создать или обновить результат
                result_obj, created = TrialResult.objects.update_or_create(
                    participant=participant,
                    indicator=indicator,
                    defaults={
                        'value': value,
                        'plot_1': plot_1,
                        'plot_2': plot_2,
                        'plot_3': plot_3,
                        'plot_4': plot_4,
                        'is_rejected': is_rejected,
                        'rejection_reason': rejection_reason,
                        'is_restored': is_restored,
                        'text_value': str(value) if not isinstance(value, (int, float)) and value is not None else None,
                        'measurement_date': measurement_date,
                        'trial': trial,
                        'sort_record': participant.sort_record,
                        'created_by': request.user
                    }
                )
                
                if created:
                    results_created += 1
                else:
                    results_updated += 1
        
        # === ПЕРЕСЧИТАТЬ "ГРУППУ ПО СТАТ. ОБРАБОТКЕ" для всех участников ===
        # (автоматически на основе урожайности и НСР)
        for participant in trial.participants.filter(is_deleted=False):
            participant.calculate_statistical_result()
        
        # Рассчитать min/max по каждому показателю
        min_max = {}
        for indicator in trial.indicators.filter(is_deleted=False, is_quality=False):
            values = TrialResult.objects.filter(
                participant__trial=trial,
                indicator=indicator,
                value__isnull=False,
                is_deleted=False
            ).values_list('value', flat=True)
            
            if values:
                min_max[indicator.code] = {
                    'min': float(min(values)),
                    'max': float(max(values))
                }
        
        # === ФИНАЛЬНАЯ ОТПРАВКА ===
        if is_final:
            trial.status = 'completed_008'
            trial.approval_date = timezone.now().date()
            trial.save()
            message = 'Форма 008 успешно отправлена. Полевые работы завершены.'
        else:
            message = 'Черновик формы 008 успешно сохранен'
        
        # === СОБРАТЬ КОДЫ ГРУПП всех участников ===
        standard_participant = trial.get_standard_participants().first()
        standard_yield = None
        
        if standard_participant:
            standard_yield_result = TrialResult.objects.filter(
                participant=standard_participant,
                indicator__code='yield',
                is_deleted=False
            ).first()
            if standard_yield_result:
                standard_yield = standard_yield_result.value
        
        participants_codes = []
        for participant in trial.participants.filter(is_deleted=False).order_by('participant_number'):
            # Получить урожайность
            yield_result = TrialResult.objects.filter(
                participant=participant,
                indicator__code='yield',
                is_deleted=False
            ).first()
            
            participant_yield = yield_result.value if yield_result else None
            
            # Рассчитать отклонения от стандарта
            deviation_abs = None
            deviation_pct = None
            
            if participant_yield is not None and standard_yield is not None and not participant.is_standard:
                deviation_abs = round(participant_yield - standard_yield, 2)
                deviation_pct = round((deviation_abs / standard_yield * 100), 1) if standard_yield != 0 else None
            
            participants_codes.append({
                'participant_id': participant.id,
                'participant_number': participant.participant_number,
                'sort_name': participant.sort_record.name if participant.sort_record else None,
                
                # ДВА РАЗНЫХ ПОЛЯ!
                'maturity_group_code': participant.maturity_group_code,  # Организационный код
                'statistical_result': participant.statistical_result,    # Группа по стат. обработке (АВТО)
                'statistical_result_display': participant.get_statistical_result_display(),
                
                'yield': participant_yield,
                'deviation_standard_abs': deviation_abs,
                'deviation_standard_pct': deviation_pct,
                'is_standard': participant.is_standard
            })
        
        # Получить обновленную статистику
        statistics_data = trial.calculate_trial_statistics()
        
        response_data = {
            'success': True,
            'message': message,
            'is_final': is_final,
            'results_created': results_created,
            'results_updated': results_updated,
            'trial_status': trial.status,
            'statistics': statistics_data or {
                'lsd_095': None,
                'error_mean': None,
                'accuracy_percent': None,
                'has_data': False
            },
            'min_max': min_max,
            'participants_codes': participants_codes
        }
        
        if errors:
            response_data['validation_errors'] = errors
        
        return Response(response_data)
    
    @action(detail=True, methods=['get'], url_path='form008/statistics')
    def form008_statistics(self, request, pk=None):
        """
        Получить статистику испытания (P%, НСР, E)
        
        Включает как введенную вручную статистику, так и авторасчет с делянок.
        
        GET /api/v1/trials/{id}/form008/statistics/
        """
        trial = self.get_object()
        
        # Получить введенную вручную статистику
        manual_statistics = trial.calculate_trial_statistics()
        
        # Получить авторасчет с делянок
        auto_statistics = trial.calculate_auto_statistics_from_plots()
        
        # Если нет никаких данных
        if not manual_statistics and not auto_statistics:
            return Response({
                'has_data': False,
                'message': 'No data available for statistics calculation'
            })
        
        # Найти стандарт
        standard = trial.get_standard_participants().first()
        standard_data = None
        
        if standard:
            yield_result = TrialResult.objects.filter(
                participant=standard,
                indicator__code='yield',
                is_deleted=False
            ).first()
            
            if yield_result:
                standard_data = {
                    'participant_id': standard.id,
                    'sort_name': standard.sort_record.name if standard.sort_record else None,
                    'yield': yield_result.value,
                    'plot_values': [
                        yield_result.plot_1,
                        yield_result.plot_2,
                        yield_result.plot_3,
                        yield_result.plot_4
                    ] if yield_result.plot_1 is not None else None
                }
        
        # Сравнение всех участников со стандартом
        comparison = []
        for participant in trial.get_tested_participants():
            yield_result = TrialResult.objects.filter(
                participant=participant,
                indicator__code='yield',
                is_deleted=False
            ).first()
            
            if yield_result and standard_data:
                deviation_abs = yield_result.value - standard_data['yield']
                deviation_pct = (deviation_abs / standard_data['yield'] * 100) if standard_data['yield'] != 0 else None
                
                comparison.append({
                    'participant_id': participant.id,
                    'participant_number': participant.participant_number,
                    'sort_name': participant.sort_record.name if participant.sort_record else None,
                    'yield': yield_result.value,
                    'deviation_standard_abs': round(deviation_abs, 2),
                    'deviation_standard_pct': round(deviation_pct, 1) if deviation_pct is not None else None,
                    'statistical_result': participant.statistical_result,
                    'statistical_result_display': participant.get_statistical_result_display() if participant.statistical_result is not None else None
                })
        
        response_data = {
            'trial_id': trial.id,
            'has_manual_data': manual_statistics is not None,
            'has_auto_data': auto_statistics is not None,
            'standard': standard_data,
            'comparison': comparison
        }
        
        # Добавить ручную статистику если есть
        if manual_statistics:
            response_data['manual_statistics'] = manual_statistics
        
        # Добавить авторасчет если есть
        if auto_statistics:
            response_data['auto_statistics'] = auto_statistics
        
        return Response(response_data)
    
    @action(detail=True, methods=['get'], url_path='form008/auto-statistics')
    def form008_auto_statistics(self, request, pk=None):
        """
        Получить только авторасчет статистики с делянок
        
        GET /api/v1/trials/{id}/form008/auto-statistics/
        
        Возвращает только авторасчитанные значения НСР₀.₉₅, E и P%
        на основе данных с делянок всех участников.
        """
        trial = self.get_object()
        
        # Получить авторасчет с делянок
        auto_statistics = trial.calculate_auto_statistics_from_plots()
        
        if not auto_statistics:
            return Response({
                'has_data': False,
                'message': 'Недостаточно данных с делянок для авторасчета статистики',
                'requirements': {
                    'min_participants': 2,
                    'min_plots_per_participant': 3,
                    'required_indicator': 'yield'
                }
            })
        
        return Response({
            'trial_id': trial.id,
            'has_data': True,
            'auto_statistics': auto_statistics,
            'note': 'Это авторасчет для справки. Проверьте корректность и введите окончательные значения вручную.'
        })
    
    @action(detail=True, methods=['patch'], url_path='form008/update-conditions')
    def form008_update_conditions(self, request, pk=None):
        """
        Обновить условия испытания для формы 008
        
        PATCH /api/v1/trials/{id}/form008/update-conditions/
        {
            "agro_background": "favorable",
            "growing_conditions": "irrigated", 
            "cultivation_technology": "traditional",
            "growing_method": "soil_traditional",
            "harvest_timing": "medium",
            "harvest_date": "2024-09-15",
            "additional_info": "Дополнительные примечания"
        }
        """
        trial = self.get_object()
        
        # Разрешенные поля для обновления
        allowed_fields = [
            'agro_background', 'growing_conditions', 'cultivation_technology', 
            'growing_method', 'harvest_timing', 'harvest_date', 'additional_info'
        ]
        
        # Валидация значений
        field_choices = {
            'agro_background': [choice[0] for choice in Trial.AGRO_BACKGROUND_CHOICES],
            'growing_conditions': [choice[0] for choice in Trial.GROWING_CONDITIONS_CHOICES],
            'cultivation_technology': [choice[0] for choice in Trial.CULTIVATION_TECHNOLOGY_CHOICES],
            'growing_method': [choice[0] for choice in Trial.GROWING_METHOD_CHOICES],
            'harvest_timing': [choice[0] for choice in Trial.HARVEST_TIMING_CHOICES],
        }
        
        errors = {}
        update_data = {}
        
        for field in allowed_fields:
            if field in request.data:
                value = request.data[field]
                
                # Проверка choices для enum полей
                if field in field_choices and value is not None:
                    if value not in field_choices[field]:
                        errors[field] = f"Invalid choice. Must be one of: {', '.join(field_choices[field])}"
                        continue
                
                # Проверка даты
                if field == 'harvest_date' and value is not None:
                    try:
                        from datetime import datetime
                        if isinstance(value, str):
                            datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        errors[field] = "Invalid date format. Use YYYY-MM-DD"
                        continue
                
                update_data[field] = value
        
        if errors:
            return Response({
                'error': 'Validation failed',
                'details': errors
            }, status=400)
        
        # Обновляем поля
        for field, value in update_data.items():
            setattr(trial, field, value)
        
        trial.save()
        
        return Response({
            'success': True,
            'message': 'Trial conditions updated successfully',
            'trial_id': trial.id,
            'updated_fields': list(update_data.keys()),
            'trial': TrialSerializer(trial).data
        })
    
    @action(detail=True, methods=['post'], url_path='add-indicators')
    def add_indicators(self, request, pk=None):
        """
        Добавить показатели к испытанию по культуре
        
        POST /api/v1/trials/{id}/add-indicators/
        {
            "indicator_ids": [1, 2, 3],  // опционально - конкретные показатели
            "by_culture": true,          // опционально - добавить все показатели культуры
            "include_recommended": true  // опционально - включить рекомендуемые показатели
        }
        
        Response:
        {
            "success": true,
            "added_indicators": 3,
            "total_indicators": 5,
            "indicators": [...]
        }
        """
        trial = self.get_object()
        
        indicator_ids = request.data.get('indicator_ids', [])
        by_culture = request.data.get('by_culture', False)
        include_recommended = request.data.get('include_recommended', True)
        
        added_indicators = []
        
        if indicator_ids:
            # Добавить конкретные показатели
            indicators_to_add = Indicator.objects.filter(
                id__in=indicator_ids,
                is_deleted=False
            )
            
            for indicator in indicators_to_add:
                if not trial.indicators.filter(id=indicator.id).exists():
                    trial.indicators.add(indicator)
                    added_indicators.append(indicator)
        
        elif by_culture and trial.culture:
            # Добавить показатели по культуре
            if trial.culture.group_culture:
                # Получить все показатели для группы культуры (кроме уже назначенных)
                existing_indicator_ids = trial.indicators.values_list('id', flat=True)
                
                culture_indicators = Indicator.objects.filter(
                    group_cultures=trial.culture.group_culture,
                    is_deleted=False
                ).exclude(id__in=existing_indicator_ids)
                
                # Если не включать рекомендуемые - только обязательные
                if not include_recommended:
                    culture_indicators = culture_indicators.filter(is_required=True)
                
                for indicator in culture_indicators:
                    trial.indicators.add(indicator)
                    added_indicators.append(indicator)
        
        # Получить обновленный список показателей
        all_indicators = trial.indicators.filter(is_deleted=False).order_by('sort_order', 'name')
        indicators_data = []
        
        for indicator in all_indicators:
            indicators_data.append({
                'id': indicator.id,
                'code': indicator.code,
                'name': indicator.name,
                'unit': indicator.unit,
                'is_numeric': indicator.is_numeric,
                'is_required': indicator.is_required,
                'is_recommended': indicator.is_recommended,
                'is_quality': indicator.is_quality,
                'category': indicator.category,
                'sort_order': indicator.sort_order
            })
        
        return Response({
            'success': True,
            'added_indicators': len(added_indicators),
            'total_indicators': len(indicators_data),
            'indicators': indicators_data,
            'message': f'Added {len(added_indicators)} indicators to trial'
        })
    
    @action(detail=True, methods=['delete'], url_path='remove-indicators')
    def remove_indicators(self, request, pk=None):
        """
        Удалить показатели из испытания
        
        DELETE /api/v1/trials/{id}/remove-indicators/
        {
            "indicator_ids": [1, 2, 3]  // обязательно - ID показателей для удаления
        }
        
        Response:
        {
            "success": true,
            "removed_indicators": 2,
            "total_indicators": 3
        }
        """
        trial = self.get_object()
        
        indicator_ids = request.data.get('indicator_ids', [])
        
        if not indicator_ids:
            return Response({
                'error': 'indicator_ids is required'
            }, status=400)
        
        # Удалить показатели (кроме обязательных)
        indicators_to_remove = Indicator.objects.filter(
            id__in=indicator_ids,
            is_deleted=False
        )
        
        removed_count = 0
        for indicator in indicators_to_remove:
            if indicator.is_required:
                return Response({
                    'error': f'Cannot remove required indicator: {indicator.name}'
                }, status=400)
            
            if trial.indicators.filter(id=indicator.id).exists():
                trial.indicators.remove(indicator)
                removed_count += 1
        
        total_indicators = trial.indicators.filter(is_deleted=False).count()
        
        return Response({
            'success': True,
            'removed_indicators': removed_count,
            'total_indicators': total_indicators,
            'message': f'Removed {removed_count} indicators from trial'
        })



