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
    
    def perform_create(self, serializer):
        """
        При создании группы культур - создаем в Patents Service и сохраняем локально
        """
        from django.utils import timezone
        
        # Сначала создаем в Patents Service
        group_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': group_data.get('name'),
            'description': group_data.get('description', ''),
        }
        
        # Создаем в Patents Service
        patents_group = patents_api.create_group_culture(patents_data)
        
        if patents_group:
            # Если успешно создали в Patents Service, сохраняем локально
            group = serializer.save(
                group_culture_id=patents_group.get('id'),
                synced_at=timezone.now()
            )
            return group
        else:
            # Если не удалось создать в Patents Service, создаем только локально
            # с временным group_culture_id (будет обновлен при синхронизации)
            import random
            temp_id = random.randint(100000, 999999)
            return serializer.save(
                group_culture_id=temp_id,
                synced_at=None
            )
    
    def perform_update(self, serializer):
        """
        При обновлении группы культур - обновляем в Patents Service и локально
        """
        from django.utils import timezone
        
        group = serializer.instance
        group_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': group_data.get('name', group.name),
            'description': group_data.get('description', group.description),
        }
        
        # Обновляем в Patents Service
        patents_group = patents_api.update_group_culture(
            group.group_culture_id,
            patents_data
        )
        
        if patents_group:
            # Если успешно обновили в Patents Service, сохраняем локально
            serializer.save(synced_at=timezone.now())
        else:
            # Если не удалось обновить в Patents Service, сохраняем только локально
            serializer.save(synced_at=None)
    
    def perform_destroy(self, instance):
        """
        При удалении группы культур - удаляем из Patents Service и локально
        """
        # Пробуем удалить из Patents Service
        patents_deleted = patents_api.delete_group_culture(instance.group_culture_id)
        
        if patents_deleted:
            # Если успешно удалили из Patents Service, удаляем локально
            instance.delete()
        else:
            # Если не удалось удалить из Patents Service, помечаем как удаленный локально
            instance.is_deleted = True
            instance.save()




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
    
    def perform_create(self, serializer):
        """
        При создании культуры - создаем в Patents Service и сохраняем локально
        """
        from django.utils import timezone
        
        # Сначала создаем в Patents Service
        culture_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': culture_data.get('name'),
            'description': culture_data.get('description', ''),
            'group_culture': culture_data.get('group_culture').group_culture_id if culture_data.get('group_culture') else None,
        }
        
        # Создаем в Patents Service
        patents_culture = patents_api.create_culture(patents_data)
        
        if patents_culture:
            # Если успешно создали в Patents Service, сохраняем локально
            culture = serializer.save(
                culture_id=patents_culture.get('id'),
                synced_at=timezone.now()
            )
            return culture
        else:
            # Если не удалось создать в Patents Service, создаем только локально
            # с временным culture_id (будет обновлен при синхронизации)
            import random
            temp_id = random.randint(100000, 999999)
            return serializer.save(
                culture_id=temp_id,
                synced_at=None
            )
    
    def perform_update(self, serializer):
        """
        При обновлении культуры - обновляем в Patents Service и локально
        """
        from django.utils import timezone
        
        culture = serializer.instance
        culture_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': culture_data.get('name', culture.name),
            'description': culture_data.get('description', culture.description),
            'group_culture': culture_data.get('group_culture', culture.group_culture).group_culture_id if culture_data.get('group_culture', culture.group_culture) else None,
        }
        
        # Обновляем в Patents Service
        patents_culture = patents_api.update_culture(
            culture.culture_id,
            patents_data
        )
        
        if patents_culture:
            # Если успешно обновили в Patents Service, сохраняем локально
            serializer.save(synced_at=timezone.now())
        else:
            # Если не удалось обновить в Patents Service, сохраняем только локально
            serializer.save(synced_at=None)
    
    def perform_destroy(self, instance):
        """
        При удалении культуры - удаляем из Patents Service и локально
        """
        # Пробуем удалить из Patents Service
        patents_deleted = patents_api.delete_culture(instance.culture_id)
        
        if patents_deleted:
            # Если успешно удалили из Patents Service, удаляем локально
            instance.delete()
        else:
            # Если не удалось удалить из Patents Service, помечаем как удаленный локально
            instance.is_deleted = True
            instance.save()
    
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




