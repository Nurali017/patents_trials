"""
Culture ViewSets
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


class IndicatorViewSet(viewsets.ModelViewSet):
    """
    Показатели измерений
    
    Фильтрация:
        ?culture_id=<id> - показатели для конкретной культуры (через группу культуры)
        ?group_culture_id=<id> - показатели для группы культур
        ?culture_group=<id> - алиас для group_culture_id
        ?is_universal=true - универсальные показатели
        ?category=common|quality|specific - по категории
        ?is_quality=true|false - лабораторные (true) или основные (false) показатели
        ?search=<text> - поиск по названию или коду
    """
    queryset = Indicator.objects.filter(is_deleted=False).prefetch_related('group_cultures')
    serializer_class = IndicatorSerializer
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """Фильтрация по культуре или группе культур (новая логика через group_cultures)"""
        queryset = super().get_queryset()
        
        # Фильтр по культуре - получаем показатели группы этой культуры
        culture_id = self.request.query_params.get('culture_id')
        if culture_id:
            try:
                culture = Culture.objects.get(id=culture_id, is_deleted=False)
                if culture.group_culture:
                    # Показатели группы этой культуры (НОВАЯ ЛОГИКА)
                    queryset = queryset.filter(
                        group_cultures=culture.group_culture
                    ).distinct()
                else:
                    # Если у культуры нет группы - вернуть пустой набор
                    queryset = queryset.none()
            except Culture.DoesNotExist:
                queryset = queryset.none()
        
        # Фильтр по группе культур напрямую (два варианта: group_culture_id и culture_group)
        group_culture_id = self.request.query_params.get('group_culture_id') or self.request.query_params.get('culture_group')
        if group_culture_id:
            queryset = queryset.filter(
                group_cultures__id=group_culture_id
            ).distinct()
        
        # Фильтр по категории
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Фильтр по is_quality (лабораторные/основные показатели)
        is_quality = self.request.query_params.get('is_quality')
        if is_quality is not None:
            if is_quality.lower() == 'true':
                queryset = queryset.filter(is_quality=True)
            elif is_quality.lower() == 'false':
                queryset = queryset.filter(is_quality=False)
        
        # Фильтр только универсальные
        is_universal = self.request.query_params.get('is_universal')
        if is_universal == 'true':
            queryset = queryset.filter(is_universal=True)
        
        # Поиск по названию или коду
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                django_models.Q(name__icontains=search) |
                django_models.Q(code__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='by-culture/(?P<culture_id>[^/.]+)')
    def by_culture(self, request, culture_id=None):
        """
        Получить показатели для конкретной культуры с группировкой
        
        GET /api/v1/indicators/by-culture/{culture_id}/
        
        Response:
        {
            "culture": {...},
            "required_indicators": [...],
            "recommended_indicators": [...],
            "quality_indicators": [...],
            "total_indicators": 15
        }
        """
        try:
            culture = Culture.objects.get(id=culture_id, is_deleted=False)
        except Culture.DoesNotExist:
            return Response({'error': 'Culture not found'}, status=404)
        
        if not culture.group_culture:
            return Response({
                'culture': {
                    'id': culture.id,
                    'name': culture.name,
                    'group_culture': None
                },
                'required_indicators': [],
                'recommended_indicators': [],
                'quality_indicators': [],
                'total_indicators': 0,
                'message': 'Culture has no group assigned'
            })
        
        # Получить все показатели для группы культуры
        all_indicators = Indicator.objects.filter(
            group_cultures=culture.group_culture,
            is_deleted=False
        ).order_by('sort_order', 'name')
        
        # Разделить по типам
        required_indicators = []
        recommended_indicators = []
        quality_indicators = []
        
        for indicator in all_indicators:
            indicator_data = {
                'id': indicator.id,
                'code': indicator.code,
                'name': indicator.name,
                'unit': indicator.unit,
                'is_numeric': indicator.is_numeric,
                'is_required': indicator.is_required,
                'is_recommended': indicator.is_recommended,
                'is_quality': indicator.is_quality,
                'is_auto_calculated': indicator.is_auto_calculated,
                'calculation_formula': indicator.calculation_formula,
                'category': indicator.category,
                'sort_order': indicator.sort_order,
                'description': indicator.description
            }
            
            if indicator.is_quality:
                quality_indicators.append(indicator_data)
            elif indicator.is_required:
                required_indicators.append(indicator_data)
            elif indicator.is_recommended:
                recommended_indicators.append(indicator_data)
        
        return Response({
            'culture': {
                'id': culture.id,
                'name': culture.name,
                'group_culture': {
                    'id': culture.group_culture.id,
                    'name': culture.group_culture.name
                }
            },
            'required_indicators': required_indicators,
            'recommended_indicators': recommended_indicators,
            'quality_indicators': quality_indicators,
            'total_indicators': len(all_indicators),
            'summary': {
                'required_count': len(required_indicators),
                'recommended_count': len(recommended_indicators),
                'quality_count': len(quality_indicators)
            }
        })



class TrialTypeViewSet(viewsets.ModelViewSet):
    """Типы испытаний (КСИ, ООС, ДЮС-ТЕСТ и т.д.)"""
    queryset = TrialType.objects.filter(is_deleted=False)
    serializer_class = TrialTypeSerializer
    pagination_class = None  # Отключаем пагинацию - возвращаем все типы испытаний
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]




class GroupCultureViewSet(viewsets.ModelViewSet):
    """
    Группы культур (Зерновые, Овощные и т.д.)
    
    Локальная копия из Patents Service для автономной работы
    """
    queryset = GroupCulture.objects.filter(is_deleted=False)
    serializer_class = GroupCultureSerializer
    
    def get_permissions(self):
        """Чтение - всем, изменение/синхронизация - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]




class CultureViewSet(viewsets.ModelViewSet):
    """
    Культуры растений (Пшеница яровая, Ячмень и т.д.)
    
    Локальная копия из Patents Service для автономной работы
    """
    queryset = Culture.objects.filter(is_deleted=False)
    serializer_class = CultureSerializer
    
    def get_permissions(self):
        """Чтение - всем, изменение/синхронизация - только авторизованным"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'], url_path='sync')
    def sync(self, request, pk=None):
        """
        Синхронизировать культуру с Patents Service
        
        POST /api/v1/cultures/{id}/sync/
        """
        culture = self.get_object()
        if culture.sync_from_patents():
            return Response({
                'success': True,
                'message': f'Культура {culture.name} успешно синхронизирована'
            })
        else:
            return Response({
                'success': False,
                'error': 'Failed to sync with Patents Service'
            }, status=500)




