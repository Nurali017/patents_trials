"""
Document ViewSets
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
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


class DocumentViewSet(viewsets.ModelViewSet):
    """Документы испытаний и заявок"""
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Требуется авторизация
    
    def get_queryset(self):
        """Фильтрация по application или trial"""
        queryset = super().get_queryset()
        
        application_id = self.request.query_params.get('application')
        trial_id = self.request.query_params.get('trial')
        
        if application_id:
            queryset = queryset.filter(application_id=application_id)
        
        if trial_id:
            queryset = queryset.filter(trial_id=trial_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """При создании документа устанавливаем uploaded_by автоматически"""
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        """
        Скачать файл документа
        
        GET /api/v1/documents/{id}/download/
        
        Возвращает файл для скачивания
        """
        from django.http import FileResponse, Http404
        import os
        
        document = self.get_object()
        
        if not document.file:
            return Response({
                'error': 'Document has no file attached'
            }, status=404)
        
        try:
            file_path = document.file.path
            if not os.path.exists(file_path):
                return Response({
                    'error': 'File not found on server'
                }, status=404)
            
            # Открываем файл и возвращаем как attachment
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )
            return response
        except Exception as e:
            return Response({
                'error': f'Error downloading file: {str(e)}'
            }, status=500)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_cultures(request):
    """
    Получить список всех культур из Patents Service
    
    Проксирует запрос к Patents Service для получения справочника культур.
    Используется при создании/редактировании сортов.
    
    GET /api/v1/patents/cultures/
    
    Query params:
        - group: фильтр по группе культур (ID группы)
        - group_culture_id: алиас для параметра group (для обратной совместимости)
        - culture_group: алиас для параметра group (для обратной совместимости)
        - search: поиск по названию культуры
    
    Примеры:
        GET /api/v1/patents/cultures/?group=1  # Зерновые культуры
        GET /api/v1/patents/cultures/?search=пшеница  # Поиск по названию
        GET /api/v1/patents/cultures/?group=1&search=пшеница  # Комбинированная фильтрация
    """
    cultures = patents_api.get_all_cultures(params=request.query_params.dict())
    return Response(cultures)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_group_cultures(request):
    """
    Получить список всех групп культур из Patents Service
    
    Проксирует запрос к Patents Service для получения справочника групп культур.
    Используется при создании/редактировании культур и сортов.
    
    GET /api/v1/patents/group-cultures/
    
    Query params:
        - search: поиск по названию
    """
    group_cultures = patents_api.get_all_group_cultures(params=request.query_params.dict())
    return Response(group_cultures)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_culture_detail(request, culture_id):
    """
    Получить детальную информацию о культуре
    
    GET /api/v1/patents/cultures/{id}/
    """
    culture = patents_api.get_culture(culture_id)
    if culture:
        return Response(culture)
    else:
        return Response({
            'error': f'Culture {culture_id} not found'
        }, status=404)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_culture(request):
    """
    Создать новую культуру в Patents Service
    
    Проксирует запрос к Patents Service.
    Trials Service НЕ хранит культуры локально!
    
    POST /api/v1/patents/cultures/create/
    Body: {
        "name": "Новая культура",
        "group_culture": 1,
        "description": "Описание"
    }
    """
    culture = patents_api.create_culture(request.data)
    if culture:
        return Response(culture, status=201)
    else:
        return Response({
            'error': 'Failed to create culture in Patents Service'
        }, status=500)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.AllowAny])
def update_culture(request, culture_id):
    """
    Обновить культуру в Patents Service
    
    PUT/PATCH /api/v1/patents/cultures/{id}/update/
    """
    culture = patents_api.update_culture(culture_id, request.data)
    if culture:
        return Response(culture)
    else:
        return Response({
            'error': f'Failed to update culture {culture_id}'
        }, status=500)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_group_culture(request):
    """
    Создать новую группу культур в Patents Service
    
    POST /api/v1/patents/group-cultures/create/
    Body: {
        "name": "Новая группа",
        "description": "Описание"
    }
    """
    group = patents_api.create_group_culture(request.data)
    if group:
        return Response(group, status=201)
    else:
        return Response({
            'error': 'Failed to create group culture in Patents Service'
        }, status=500)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_originators(request):
    """
    Получить список всех оригинаторов из Patents Service
    
    Проксирует запрос к Patents Service.
    Используется при создании/редактировании сортов.
    
    GET /api/v1/patents/originators/
    
    Query params:
        - search: поиск по названию
    """
    originators = patents_api.get_all_originators(params=request.query_params.dict())
    return Response(originators)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_originator_detail(request, originator_id):
    """
    Получить информацию об оригинаторе
    
    GET /api/v1/patents/originators/{id}/
    """
    originator = patents_api.get_originator(originator_id)
    if originator:
        return Response(originator)
    else:
        return Response({
            'error': f'Originator {originator_id} not found'
        }, status=404)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_originator(request):
    """
    Создать нового оригинатора в Patents Service
    
    POST /api/v1/patents/originators/create/
    Body: {
        "name": "Название оригинатора"
    }
    """
    originator = patents_api.create_originator(request.data)
    if originator:
        return Response(originator, status=201)
    else:
        return Response({
            'error': 'Failed to create originator in Patents Service'
        }, status=500)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_sorts(request):
    """
    Получить список всех сортов из Patents Service
    
    Проксирует запрос к Patents Service для получения справочника сортов.
    
    GET /api/v1/patents/sorts/
    
    Query params:
        - culture: фильтр по культуре (Patents culture ID)
        - search: поиск по названию
        - code: поиск по коду
    """
    sorts = patents_api.get_all_sorts(params=request.query_params.dict())
    return Response(sorts)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_sorts_for_trial_culture(request):
    """
    Получить сорта для культуры из Trials Service
    
    Принимает локальный Trials culture ID и делает правильный маппинг к Patents API.
    
    GET /api/v1/trials/sorts-by-culture/
    
    Query params:
        - culture_id: локальный ID культуры в Trials (обязательно)
        - region_id: ID региона (опционально) - если передан, возвращается первые 4 сорта
        - search: поиск по названию
        - code: поиск по коду
    
    Response:
        {
            "trials_culture_id": 6,           # Локальный ID в Trials
            "trials_culture_name": "Айва",
            "patents_culture_id": 535,        # ID в Patents Service
            "sorts": [                        # Список сортов из Patents (первые 4 если передан region_id)
                {
                    "id": 2096,
                    "name": "Аксинья",
                    "maturity_group": "D01"   # Только если передан region_id
                },
                {
                    "id": 2097,
                    "name": "Другой сорт",
                    "maturity_group": "D01"   # Только если передан region_id
                }
            ],
            "count": 4 или 10                 # Количество сортов (4 если передан region_id)
        }
    """
    trials_culture_id = request.query_params.get('culture_id')
    
    if not trials_culture_id:
        return Response({
            'error': 'culture_id parameter is required'
        }, status=400)
    
    # Найти культуру в Trials Service
    try:
        culture = Culture.objects.get(id=trials_culture_id, is_deleted=False)
    except Culture.DoesNotExist:
        return Response({
            'error': f'Culture with ID {trials_culture_id} not found in Trials Service'
        }, status=404)
    
    # Получить Patents culture ID
    patents_culture_id = culture.culture_id
    
    if not patents_culture_id:
        return Response({
            'error': f'Culture "{culture.name}" does not have Patents culture_id mapping'
        }, status=400)
    
    # Подготовить параметры для Patents API
    patents_params = {
        'culture': patents_culture_id,  # Используем правильный Patents ID!
    }
    
    # Добавить дополнительные параметры фильтрации
    if 'search' in request.query_params:
        patents_params['search'] = request.query_params['search']
    if 'code' in request.query_params:
        patents_params['code'] = request.query_params['code']
    
    # Запросить сорта из Patents API
    sorts = patents_api.get_all_sorts(params=patents_params)
    
    if sorts is None:
        return Response({
            'error': 'Failed to fetch sorts from Patents Service'
        }, status=500)
    
    # Если передан region_id, возвращаем только первый сорт и добавляем maturity_group к каждому сорту
    region_id = request.query_params.get('region_id')
    response_data = {
        'trials_culture_id': culture.id,
        'trials_culture_name': culture.name,
        'patents_culture_id': patents_culture_id,
        'sorts': sorts,
        'count': len(sorts) if isinstance(sorts, list) else 0
    }
    
    if region_id and isinstance(sorts, list) and len(sorts) > 0:
        # Берем первые 4 сорта и добавляем к каждому maturity_group
        first_4_sorts = sorts[:4]  # Берем первые 4 сорта
        for sort in first_4_sorts:
            if isinstance(sort, dict):
                sort['maturity_group'] = "D01"
        response_data['sorts'] = first_4_sorts
        response_data['count'] = len(first_4_sorts)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_sort_detail(request, sort_id):
    """
    Получить детальную информацию о сорте
    
    GET /api/v1/patents/sorts/{id}/
    """
    sort = patents_api.get_sort(sort_id)
    if sort:
        return Response(sort)
    else:
        return Response({
            'error': f'Sort {sort_id} not found'
        }, status=404)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_sort(request):
    """
    Создать новый сорт в Patents Service
    
    POST /api/v1/patents/sorts/create/
    Body: {
        "name": "Название сорта",
        "code": "371/06",
        "culture": 1,
        "originators": [1, 2]
    }
    """
    sort = patents_api.create_sort(request.data)
    if sort:
        return Response(sort, status=201)
    else:
        return Response({
            'error': 'Failed to create sort in Patents Service'
        }, status=500)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_patents_connection(request):
    """
    Тестовый endpoint для проверки подключения к Patents Service
    
    Проверяет:
    - Доступность Patents Service
    - Аутентификацию через токен
    - Получение данных
    
    GET /api/v1/patents/test-connection/
    
    Returns:
        {
            "status": "success",
            "patents_service_url": "http://localhost:8000",
            "authentication": "configured",
            "token_obtained": true,
            "test_request": "success",
            "message": "Successfully connected to Patents Service"
        }
    """
    from .patents_integration import patents_api
    
    result = {
        "status": "success",
        "patents_service_url": patents_api.base_url,
        "authentication": "not configured",
        "token_obtained": False,
        "test_request": "not tested",
        "message": ""
    }
    
    # Проверяем настроены ли credentials
    if patents_api.service_username and patents_api.service_password:
        result["authentication"] = "configured"
        
        # Пробуем получить токен
        token = patents_api.get_auth_token()
        if token:
            result["token_obtained"] = True
            result["token_preview"] = f"{token[:10]}...{token[-10:]}" if len(token) > 20 else token
        else:
            result["status"] = "warning"
            result["message"] = "Failed to obtain authentication token"
    else:
        result["status"] = "warning"
        result["message"] = "Patents Service credentials not configured"
    
    # Пробуем сделать тестовый запрос
    try:
        sorts = patents_api.get_all_sorts()
        if sorts is not None:
            result["test_request"] = "success"
            result["sorts_count"] = len(sorts) if isinstance(sorts, list) else 0
            if result["status"] == "success":
                result["message"] = f"Successfully connected to Patents Service. Found {result['sorts_count']} sorts."
        else:
            result["test_request"] = "failed"
            result["status"] = "error"
            result["message"] = "Failed to fetch data from Patents Service"
    except Exception as e:
        result["test_request"] = "error"
        result["status"] = "error"
        result["error"] = str(e)
        result["message"] = f"Exception while testing connection: {str(e)}"
    
    status_code = 200 if result["status"] == "success" else (500 if result["status"] == "error" else 200)
    return Response(result, status=status_code)




