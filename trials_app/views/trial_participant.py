"""
Trial Participant ViewSets
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


class TrialParticipantViewSet(viewsets.ModelViewSet):
    """Участники сортоопытов"""
    queryset = TrialParticipant.objects.filter(is_deleted=False)
    serializer_class = TrialParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]  # Требуется авторизация
    
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """
        Массовое создание участников для испытания
        
        POST /api/v1/trial-participants/bulk-create/
        {
            "trial": 10,
            "participants": [
                {
                    "sort_record": 100,
                    "statistical_group": 0,
                    "participant_number": 1
                },
                {
                    "sort_record": 50,
                    "statistical_group": 1,
                    "participant_number": 2,
                    "application": 5
                }
            ]
        }
        """
        trial_id = request.data.get('trial')
        participants_data = request.data.get('participants', [])
        
        if not trial_id:
            return Response({'error': 'trial is required'}, status=400)
        
        try:
            trial = Trial.objects.get(id=trial_id)
        except Trial.DoesNotExist:
            return Response({'error': 'Trial not found'}, status=404)
        
        created_participants = []
        for p_data in participants_data:
            participant = TrialParticipant.objects.create(
                trial=trial,
                sort_record_id=p_data['sort_record'],
                statistical_group=p_data.get('statistical_group', 1),
                participant_number=p_data['participant_number'],
                application_id=p_data.get('application'),
            )
            created_participants.append(participant)
            
            # АВТОМАТИЧЕСКИ СОЗДАТЬ ОСНОВНЫЕ ПОКАЗАТЕЛИ ДЛЯ СОРТОПЫТА
            create_basic_trial_results(participant, request.user)
        
        # АВТОМАТИЧЕСКИЙ СТАТУС TRIAL:
        # Если Trial был planned и добавили участников → переводим в active
        if trial.status == 'planned' and created_participants:
            trial.status = 'active'
            trial.save()
        
        # АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ СТАТУСА ЗАЯВКИ И PlannedDistribution:
        application_ids = set()
        for participant in created_participants:
            if participant.application_id:
                application_ids.add(participant.application_id)
        
        if application_ids:
            # Обновляем общий статус заявки
            Application.objects.filter(
                id__in=application_ids,
                status='distributed'
            ).update(status='in_progress')
            
            # Обновляем PlannedDistribution (многолетние испытания)
            for app_id in application_ids:
                planned_dist = PlannedDistribution.objects.filter(
                    application_id=app_id,
                    region=trial.region
                ).first()
                
                if planned_dist:
                    # Если первый Trial для этого PlannedDistribution
                    if planned_dist.status == 'planned':
                        planned_dist.status = 'in_progress'
                        planned_dist.year_started = trial.year or (trial.start_date.year if trial.start_date else None)
                        planned_dist.save()
        
        serializer = TrialParticipantSerializer(created_participants, many=True)
        return Response({
            'success': True,
            'count': len(created_participants),
            'participants': serializer.data,
            'trial_status': trial.status,
            'updated_applications': list(application_ids)
        })




