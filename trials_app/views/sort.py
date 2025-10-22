"""
Sort ViewSets
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db import models as django_models
from django.db.models import Q

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
    OriginatorSerializer, OriginatorRetrieveSerializer, SortRecordSerializer, ApplicationSerializer,
    TrialTypeSerializer, TrialSerializer, TrialParticipantSerializer,
    TrialResultSerializer, TrialLaboratoryResultSerializer,
    DocumentSerializer, TrialPlanSerializer, TrialPlanWriteSerializer,
    TrialPlanAddParticipantsSerializer, TrialPlanCultureSerializer,
    TrialPlanAddCultureSerializer, create_basic_trial_results,
    create_quality_trial_results
)
from ..patents_integration import patents_api
from ..filters import OriginatorFilter


class OriginatorViewSet(viewsets.ModelViewSet):
    """
    Оригинаторы (создатели сортов)
    
    Работа с локальной БД (синхронизированной с Patents Service) с новыми полями:
    - code: код оригинатора
    - is_foreign: иностранный оригинатор
    - is_nanoc: НАНОЦ оригинатор
    """
    queryset = Originator.objects.filter(is_deleted=False)
    serializer_class = OriginatorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OriginatorFilter
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_foreign', 'is_nanoc']
    ordering = ['name']
    pagination_class = None  # Отключаем пагинацию
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve', 'statistics']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        """Использовать разные сериализаторы для разных действий"""
        if self.action == 'retrieve':
            return OriginatorRetrieveSerializer
        return OriginatorSerializer
    
    def perform_create(self, serializer):
        """
        При создании оригинатора - создаем в Patents Service и сохраняем локально
        """
        from django.utils import timezone
        
        # Сначала создаем в Patents Service
        originator_data = serializer.validated_data.copy()
        
        # Убираем поля, которые не нужны для Patents Service
        patents_data = {
            'name': originator_data.get('name'),
            'code': originator_data.get('code'),
            'is_foreign': originator_data.get('is_foreign', False),
            'is_nanoc': originator_data.get('is_nanoc', False),
        }
        
        # Создаем в Patents Service
        patents_originator = patents_api.create_originator(patents_data)
        
        if patents_originator:
            # Если успешно создали в Patents Service, сохраняем локально
            originator = serializer.save(
                originator_id=patents_originator.get('id'),
                synced_at=timezone.now()
            )
            return originator
        else:
            # Если не удалось создать в Patents Service, создаем только локально
            # с временным originator_id (будет обновлен при синхронизации)
            import random
            temp_id = random.randint(100000, 999999)
            return serializer.save(
                originator_id=temp_id,
                synced_at=None
            )
    
    def perform_update(self, serializer):
        """
        При обновлении оригинатора - обновляем в Patents Service и локально
        """
        from django.utils import timezone
        
        originator = serializer.instance
        originator_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': originator_data.get('name', originator.name),
            'code': originator_data.get('code', originator.code),
            'is_foreign': originator_data.get('is_foreign', originator.is_foreign),
            'is_nanoc': originator_data.get('is_nanoc', originator.is_nanoc),
        }
        
        # Обновляем в Patents Service
        patents_originator = patents_api.update_originator(
            originator.originator_id, 
            patents_data
        )
        
        if patents_originator:
            # Если успешно обновили в Patents Service, сохраняем локально
            serializer.save(synced_at=timezone.now())
        else:
            # Если не удалось обновить в Patents Service, сохраняем только локально
            serializer.save(synced_at=None)
    
    def perform_destroy(self, instance):
        """
        При удалении оригинатора - удаляем из Patents Service и локально
        """
        # Пробуем удалить из Patents Service
        patents_deleted = patents_api.delete_originator(instance.originator_id)
        
        if patents_deleted:
            # Если успешно удалили из Patents Service, удаляем локально
            instance.delete()
        else:
            # Если не удалось удалить из Patents Service, помечаем как удаленный локально
            instance.is_deleted = True
            instance.save()
    
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """
        Получить статистику по оригинаторам из локальной БД
        
        GET /api/patents/ariginators/statistics/
        """
        queryset = self.get_queryset()
        
        stats = {
            'total_count': queryset.count(),
            'foreign_count': queryset.filter(is_foreign=True).count(),
            'domestic_count': queryset.filter(is_foreign=False).count(),
            'nanoc_count': queryset.filter(is_nanoc=True).count(),
            'with_code_count': queryset.exclude(code__isnull=True).count(),
            'without_code_count': queryset.filter(code__isnull=True).count(),
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'], url_path='sync')
    def sync(self, request, pk=None):
        """
        Синхронизировать оригинатора с Patents Service
        
        POST /api/patents/ariginators/{id}/sync/
        """
        originator = self.get_object()
        if originator.sync_from_patents():
            return Response({
                'success': True,
                'message': f'Оригинатор {originator.name} успешно синхронизирован',
                'data': OriginatorRetrieveSerializer(originator).data
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
    
    def perform_create(self, serializer):
        """
        При создании сорта - создаем в Patents Service и сохраняем локально
        """
        from django.utils import timezone
        
        # Сначала создаем в Patents Service
        sort_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': sort_data.get('name'),
            'code': sort_data.get('code', ''),
            'culture': sort_data.get('culture').culture_id if sort_data.get('culture') else None,
            'originators': [sort_data.get('originators')] if sort_data.get('originators') else [],
        }
        
        # Создаем в Patents Service
        patents_sort = patents_api.create_sort(patents_data)
        
        if patents_sort:
            # Если успешно создали в Patents Service, сохраняем локально
            sort = serializer.save(
                sort_id=patents_sort.get('id'),
                synced_at=timezone.now()
            )
            return sort
        else:
            # Если не удалось создать в Patents Service, создаем только локально
            # с временным sort_id (будет обновлен при синхронизации)
            import random
            temp_id = random.randint(100000, 999999)
            return serializer.save(
                sort_id=temp_id,
                synced_at=None
            )
    
    def perform_update(self, serializer):
        """
        При обновлении сорта - обновляем в Patents Service и локально
        """
        from django.utils import timezone
        
        sort = serializer.instance
        sort_data = serializer.validated_data.copy()
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': sort_data.get('name', sort.name),
            'code': sort_data.get('code', sort.code),
            'culture': sort_data.get('culture', sort.culture).culture_id if sort_data.get('culture', sort.culture) else None,
            'originators': [sort_data.get('originators')] if sort_data.get('originators') else [],
        }
        
        # Обновляем в Patents Service
        patents_sort = patents_api.update_sort(
            sort.sort_id,
            patents_data
        )
        
        if patents_sort:
            # Если успешно обновили в Patents Service, сохраняем локально
            serializer.save(synced_at=timezone.now())
        else:
            # Если не удалось обновить в Patents Service, сохраняем только локально
            serializer.save(synced_at=None)
    
    def perform_destroy(self, instance):
        """
        При удалении сорта - удаляем из Patents Service и локально
        """
        # Пробуем удалить из Patents Service
        patents_deleted = patents_api.delete_sort(instance.sort_id)
        
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




