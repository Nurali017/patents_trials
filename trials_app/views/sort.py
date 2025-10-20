"""
Sort ViewSets
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


class OriginatorViewSet(viewsets.ModelViewSet):
    """
    Оригинаторы (создатели сортов)
    
    Локальная копия данных из Patents Service
    """
    queryset = Originator.objects.filter(is_deleted=False)
    serializer_class = OriginatorSerializer
    
    def get_permissions(self):
        """Чтение - всем, изменение/синхронизация - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'], url_path='sync')
    def sync(self, request, pk=None):
        """
        Синхронизировать оригинатора с Patents Service
        
        POST /api/v1/originators/{id}/sync/
        """
        originator = self.get_object()
        if originator.sync_from_patents():
            return Response({
                'success': True,
                'message': f'Оригинатор {originator.name} успешно синхронизирован'
            })
        else:
            return Response({
                'success': False,
                'error': 'Failed to sync with Patents Service'
            }, status=500)



class SortRecordViewSet(viewsets.ModelViewSet):
    """
    Записи о сортах для испытаний
    
    Хранит ВСЕ данные сорта локально для автономной работы
    Синхронизируется с Patents Service
    """
    queryset = SortRecord.objects.filter(is_deleted=False)
    serializer_class = SortRecordSerializer
    
    def get_permissions(self):
        """Чтение - всем, изменение/синхронизация - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'], url_path='sync')
    def sync(self, request, pk=None):
        """
        Синхронизировать сорт с Patents Service
        
        Обновляет все данные включая оригинаторов
        
        POST /api/v1/sort-records/{id}/sync/
        """
        sort_record = self.get_object()
        if sort_record.sync_from_patents():
            return Response({
                'success': True,
                'message': f'Сорт {sort_record.name} успешно синхронизирован',
                'data': SortRecordSerializer(sort_record).data
            })
        else:
            return Response({
                'success': False,
                'error': 'Failed to sync with Patents Service'
            }, status=500)
    
    @action(detail=False, methods=['post'], url_path='sync-all')
    def sync_all(self, request):
        """
        Синхронизировать все сорта с Patents Service
        
        POST /api/v1/sort-records/sync-all/
        """
        count = 0
        errors = []
        
        for sort_record in self.get_queryset():
            if sort_record.sync_from_patents():
                count += 1
            else:
                errors.append(sort_record.sort_id)
        
        return Response({
            'synced': count,
            'failed': len(errors),
            'failed_ids': errors
        })




