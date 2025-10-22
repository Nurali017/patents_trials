from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, auth_views

router = DefaultRouter()
# Роутер для оригинаторов в patents
patents_router = DefaultRouter()
patents_router.register(r'ariginators', views.OriginatorViewSet, basename='patent-originator')
# Справочники Trials
router.register(r'oblasts', views.OblastViewSet)
router.register(r'climate-zones', views.ClimateZoneViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'indicators', views.IndicatorViewSet)
router.register(r'trial-types', views.TrialTypeViewSet)

# Справочники из Patents - ИНТЕГРИРОВАНЫ с Patents Service
router.register(r'group-cultures', views.GroupCultureViewSet)
router.register(r'cultures', views.CultureViewSet)
router.register(r'originators', views.OriginatorViewSet)
router.register(r'sort-records', views.SortRecordViewSet)


# Основные сущности
router.register(r'trial-plans', views.TrialPlanViewSet)

# API для расчетов (удалено)
router.register(r'applications', views.ApplicationViewSet)  # Заявки на испытания
router.register(r'trials', views.TrialViewSet)  # Испытания по областям
router.register(r'trial-participants', views.TrialParticipantViewSet)  # Участники сортоопытов
router.register(r'trial-results', views.TrialResultViewSet)  # Результаты измерений
router.register(r'documents', views.DocumentViewSet)  # Документы

# Годовые отчеты и решения (новая логика)
router.register(r'annual-reports', views.AnnualReportViewSet, basename='annualreport')

urlpatterns = [
    path('', include(router.urls)),
    
    # === Авторизация ===
    path('auth/register/', auth_views.register, name='auth-register'),
    path('auth/login/', auth_views.login, name='auth-login'),
    path('auth/logout/', auth_views.logout, name='auth-logout'),
    path('auth/me/', auth_views.current_user, name='auth-current-user'),
    path('auth/change-password/', auth_views.change_password, name='auth-change-password'),
    path('auth/users/', auth_views.user_list, name='auth-user-list'),
    
    # === Интеграция с Patents Service ===
    
    # Диагностика
    path('patents/test-connection/', views.test_patents_connection, name='test-patents-connection'),
    
    # Группы культур (справочник)
    path('patents/group-cultures/', views.get_group_cultures, name='get-group-cultures'),
    path('patents/group-cultures/create/', views.create_group_culture, name='create-group-culture'),
    
    # Культуры (справочник)
    path('patents/cultures/', views.get_cultures, name='get-cultures'),
    path('patents/cultures/create/', views.create_culture, name='create-culture'),
    path('patents/cultures/<int:culture_id>/', views.get_culture_detail, name='get-culture-detail'),
    path('patents/cultures/<int:culture_id>/update/', views.update_culture, name='update-culture'),
    
    # Оригинаторы API (с новыми полями)
    path('patents/', include(patents_router.urls)),
    
    
    # Сорта (справочник)
    path('patents/sorts/', views.get_sorts, name='get-sorts'),
    path('patents/sorts/create/', views.create_sort, name='create-sort'),
    path('patents/sorts/<int:sort_id>/', views.get_sort_detail, name='get-sort-detail'),
    
    
    # Сорта с маппингом культур (для Trials)
    path('sort-records/by-culture/', views.get_sorts_for_trial_culture, name='get-sorts-for-trial-culture'),
]
