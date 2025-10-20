"""
Geography ViewSets
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


class OblastViewSet(viewsets.ModelViewSet):
    """Области для испытаний"""
    queryset = Oblast.objects.filter(is_deleted=False)
    serializer_class = OblastSerializer
    pagination_class = None  # Отключаем пагинацию - возвращаем все области
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]



class ClimateZoneViewSet(viewsets.ModelViewSet):
    """Природно-климатические зоны"""
    queryset = ClimateZone.objects.filter(is_deleted=False)
    serializer_class = ClimateZoneSerializer
    pagination_class = None  # Отключаем пагинацию - возвращаем все зоны
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]



class RegionViewSet(viewsets.ModelViewSet):
    """Сортоиспытательные участки (ГСУ)"""
    queryset = Region.objects.filter(is_deleted=False).select_related('oblast', 'climate_zone')
    serializer_class = RegionSerializer
    pagination_class = None  # Отключаем пагинацию - возвращаем все регионы
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """Фильтрация по области"""
        queryset = super().get_queryset()
        
        # Фильтр по области
        oblast_id = self.request.query_params.get('oblast')
        if oblast_id:
            queryset = queryset.filter(oblast_id=oblast_id)
        
        return queryset



