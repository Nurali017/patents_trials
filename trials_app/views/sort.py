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
import logging

logger = logging.getLogger(__name__)


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
    ordering_fields = ['name', 'code', 'country', 'is_nanoc']
    ordering = ['name']
    pagination_class = None  # Отключаем пагинацию
    
    def get_permissions(self):
        """Чтение - всем, изменение - только авторизованным"""
        if self.action in ['list', 'retrieve', 'statistics', 'country_list']:
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
            'country': originator_data.get('country', ''),
            'is_nanoc': originator_data.get('is_nanoc', False),
        }
        
        # Включаем code только если он указан (не None)
        if 'code' in originator_data and originator_data.get('code') is not None:
            patents_data['code'] = originator_data.get('code')
        
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
            'country': originator_data.get('country', originator.country),
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
    
    @action(detail=False, methods=['get'], url_path='countries')
    def country_list(self, request):
        """
        Список стран для выбора при создании/редактировании оригинатора

        GET /api/patents/ariginators/countries/
        """
        from django_countries import countries
        data = [{'code': code, 'name': name} for code, name in countries]
        return Response(data)

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sort_id']

    def get_permissions(self):
        """Чтение - всем, изменение/синхронизация - только авторизованным"""
        if self.action in ['list', 'retrieve', 'by_culture']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """
        При создании сорта - создаем в Patents Service и сохраняем локально
        """
        from django.utils import timezone
        
        # Сначала создаем в Patents Service
        sort_data = serializer.validated_data.copy()
        
        logger.info(f"Создание сорта: {sort_data}")
        
        # Подготавливаем данные для Patents Service
        patents_data = {
            'name': sort_data.get('name'),
            'code': sort_data.get('public_code', ''),  # Используем public_code из сериализатора
            'culture': sort_data.get('culture').culture_id if sort_data.get('culture') else None,
            'originators': [],  # Оригинаторы будут обработаны после создания сорта
        }
        
        logger.info(f"Данные для Patents Service: {patents_data}")
        
        # Создаем в Patents Service
        patents_sort = patents_api.create_sort(patents_data)
        
        logger.info(f"Ответ от Patents Service: {patents_sort}")
        
        if patents_sort:
            # Если успешно создали в Patents Service, сохраняем локально
            sort = serializer.save(
                sort_id=patents_sort.get('id'),
                synced_at=timezone.now()
            )
            
            logger.info(f"Сорт создан локально с ID: {sort.id}, Patents ID: {sort.sort_id}")

            # Обрабатываем оригинаторов после создания сорта
            # originators не проходит через validated_data (SerializerMethodField = read-only),
            # поэтому берём из request.data
            originators_data = self.request.data.get('originators', [])
            self._handle_originators(sort, originators_data)

            return sort
        else:
            # Если не удалось создать в Patents Service, создаем только локально
            # с временным sort_id (будет обновлен при синхронизации)
            logger.warning("Не удалось создать сорт в Patents Service, создаем локально")
            import random
            temp_id = random.randint(100000, 999999)
            sort = serializer.save(
                sort_id=temp_id,
                synced_at=None
            )

            logger.info(f"Сорт создан локально с временным ID: {sort.id}, temp Patents ID: {sort.sort_id}")

            # Обрабатываем оригинаторов даже при локальном создании
            originators_data = self.request.data.get('originators', [])
            self._handle_originators(sort, originators_data)
            
            return sort
    
    def _handle_originators(self, sort_record, originators_data):
        """
        Обработать оригинаторов для созданного сорта

        Args:
            sort_record: созданный SortRecord
            originators_data: список оригинаторов из запроса
                [{"originator_id": 1, "percentage": 100}]
                originator_id может быть как локальный ID, так и Patents ID
        """
        from trials_app.models import SortOriginator, Originator

        if not originators_data:
            return

        # Удаляем старые связи (если есть)
        SortOriginator.objects.filter(sort_record=sort_record).delete()

        # Создаем новые связи
        for orig_data in originators_data:
            originator_id = orig_data.get('originator_id')
            percentage = orig_data.get('percentage', 100)

            if not originator_id:
                continue

            try:
                # Сначала ищем по локальному id, затем по Patents originator_id
                try:
                    originator = Originator.objects.get(id=originator_id, is_deleted=False)
                except Originator.DoesNotExist:
                    originator = Originator.objects.get(originator_id=originator_id, is_deleted=False)

                SortOriginator.objects.create(
                    sort_record=sort_record,
                    originator=originator,
                    percentage=percentage
                )

            except Originator.DoesNotExist:
                logger.warning(f"Оригинатор с ID {originator_id} не найден (ни local, ни Patents)")
                continue
    
    def perform_update(self, serializer):
        """
        При обновлении сорта - обновляем в Patents Service и локально
        """
        from django.utils import timezone

        sort = serializer.instance
        sort_data = serializer.validated_data.copy()

        # Serializer maps 'code' field → 'public_code' via source='public_code',
        # so validated_data uses 'public_code' as the key.
        culture = sort_data.get('culture', sort.culture)
        patents_data = {
            'name': sort_data.get('name', sort.name),
            'code': sort_data.get('public_code', sort.public_code),
            'culture': culture.culture_id if culture else None,
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

    @action(detail=False, methods=['get'], url_path='by-culture')
    def by_culture(self, request):
        """
        Получить сорта по культуре и области

        GET /api/sort-records/by-culture/?culture_id=71&oblast_id=17

        Параметры:
        - culture_id (int): Локальный ID культуры из таблицы Culture (обязательный)
        - oblast_id (int): ID области из таблицы Oblast (обязательный)

        Возвращает список сортов, которые принадлежат указанной культуре
        и связаны с указанной областью через таблицу SortOblast
        """
        from ..serializers import SortRecordByCultureSerializer
        from ..models import SortOblast

        culture_id = request.query_params.get('culture_id')
        oblast_id = request.query_params.get('oblast_id')

        if not culture_id:
            return Response({
                'error': 'Параметр culture_id обязателен'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not oblast_id:
            return Response({
                'error': 'Параметр oblast_id обязателен'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            culture_id = int(culture_id)
            oblast_id = int(oblast_id)
        except ValueError:
            return Response({
                'error': 'culture_id и oblast_id должны быть целыми числами'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Получаем ID сортов, связанных с указанной областью
        sort_ids_with_oblast = SortOblast.objects.filter(
            oblast_id=oblast_id
        ).values_list('sort_record_id', flat=True)

        # Фильтруем сорта по культуре (локальный ID) и области
        sorts = self.get_queryset().filter(
            culture_id=culture_id,  # culture_id - это локальный ID культуры
            id__in=sort_ids_with_oblast
        ).select_related('culture', 'culture__group_culture').prefetch_related(
            'sort_originators__originator',
            'sort_oblasts__oblast'
        )

        serializer = SortRecordByCultureSerializer(sorts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='originators')
    def manage_originators(self, request, pk=None):
        """
        Заменить список оригинаторов сорта (локально + Patents Service)

        PUT /api/sort-records/{id}/originators/
        Body: [{"originator": <local_id>, "percentage": 100}]

        Контракт: originator = локальный Originator.id (не Patents ID).
        """
        sort_record = self.get_object()
        originators_data = request.data

        if not isinstance(originators_data, list):
            return Response(
                {'error': 'Ожидается массив оригинаторов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from trials_app.models import SortOriginator
        from django.db import transaction

        # Validate all originators exist before modifying anything
        resolved = []
        for item in originators_data:
            originator_id = item.get('originator')
            percentage = item.get('percentage', 100)

            if not originator_id:
                continue

            if not isinstance(percentage, int) or percentage < 1 or percentage > 100:
                return Response(
                    {'error': f'Процент должен быть от 1 до 100 (получено {percentage})'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                originator = Originator.objects.get(id=originator_id, is_deleted=False)
            except Originator.DoesNotExist:
                return Response(
                    {'error': f'Оригинатор с ID {originator_id} не найден'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if any(r[0].id == originator.id for r in resolved):
                return Response(
                    {'error': f'Дубликат оригинатора: {originator.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            resolved.append((originator, percentage))

        # Validate total percentage = 100
        if resolved:
            total = sum(pct for _, pct in resolved)
            if total != 100:
                return Response(
                    {'error': f'Сумма процентов должна быть 100% (получено {total}%)'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        with transaction.atomic():
            SortOriginator.objects.filter(sort_record=sort_record).delete()
            for originator, percentage in resolved:
                SortOriginator.objects.create(
                    sort_record=sort_record,
                    originator=originator,
                    percentage=percentage
                )

        # Sync to Patents Service (best-effort, don't fail the request).
        # Send both flat IDs (originators) and structured ariginators with percentages
        # to match the Patents API contract used by sync_from_patents().
        if sort_record.sort_id:
            try:
                patents_api.update_sort(sort_record.sort_id, {
                    'originators': [orig.originator_id for orig, _ in resolved],
                    'ariginators': [
                        {'ariginator': orig.originator_id, 'percentage': pct}
                        for orig, pct in resolved
                    ],
                })
            except Exception as e:
                logger.warning(
                    f"Failed to sync originators to Patents for sort {sort_record.sort_id}: {e}"
                )

        return Response(SortRecordSerializer(sort_record).data)




