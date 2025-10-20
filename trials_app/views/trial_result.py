"""
Trial Result ViewSets
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


class TrialResultViewSet(viewsets.ModelViewSet):
    """Результаты испытаний"""
    queryset = TrialResult.objects.filter(is_deleted=False)
    serializer_class = TrialResultSerializer
    permission_classes = [permissions.IsAuthenticated]  # Требуется авторизация
    
    @action(detail=False, methods=['post'], url_path='bulk-entry')
    def bulk_entry(self, request):
        """
        Массовое внесение результатов (для сортопыта)
        
        POST /api/v1/trial-results/bulk-entry/
        {
            "trial": 10,
            "participant": 5,
            "measurement_date": "2024-09-23",
            "data": [
                {
                    "indicator": 1,  // урожайность
                    "value": 45.6
                },
                {
                    "indicator": 2,  // белок
                    "value": 14.5
                },
                {
                    "indicator": 3,  // устойчивость к полеганию
                    "value": 5
                }
            ]
        }
        """
        participant_id = request.data.get('participant')
        measurement_date = request.data.get('measurement_date')
        data = request.data.get('data', [])
        
        if not participant_id:
            return Response({'error': 'participant is required'}, status=400)
        
        try:
            participant = TrialParticipant.objects.get(id=participant_id)
        except TrialParticipant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=404)
        
        created_results = []
        updated_results = []
        
        for item in data:
            indicator_id = item['indicator']
            
            # Проверить, существует ли результат (обычно уже создан автоматически)
            result, created = TrialResult.objects.get_or_create(
                participant=participant,
                indicator_id=indicator_id,
                defaults={
                    'trial': participant.trial,
                    'sort_record': participant.sort_record,
                    'measurement_date': measurement_date,
                    'created_by': request.user
                }
            )
            
            # Обновить данные (работает как для существующих, так и для новых записей)
            if 'plots' in item and len(item['plots']) == 4:
                result.plot_1 = item['plots'][0]
                result.plot_2 = item['plots'][1]
                result.plot_3 = item['plots'][2]
                result.plot_4 = item['plots'][3]
                # Можно сбросить value если заполняются делянки
                # (среднее рассчитается автоматически в модели)
            elif 'value' in item:
                result.value = item['value']
                # Если передается итоговое значение, очищаем делянки
                result.plot_1 = None
                result.plot_2 = None
                result.plot_3 = None
                result.plot_4 = None
            
            if 'text_value' in item:
                result.text_value = item['text_value']
            
            if measurement_date:
                result.measurement_date = measurement_date
            
            result.save()
            
            if created:
                created_results.append(result)
            else:
                updated_results.append(result)
        
        return Response({
            'success': True,
            'created': len(created_results),
            'updated': len(updated_results),
            'total': len(data)
        })



