"""
Фильтры для API endpoints
"""
import django_filters
from django.db.models import Q, Count, Subquery, OuterRef, Exists
from rest_framework.filters import SearchFilter
from .models import Originator, Application, Trial, TrialPlan, Culture, GroupCulture, Document, APPLICATION_MANDATORY_DOCUMENT_TYPES


class OriginatorFilter(django_filters.FilterSet):
    """
    Фильтр для оригинаторов
    """
    is_foreign = django_filters.BooleanFilter(
        field_name='is_foreign',
        help_text='Фильтр по иностранным/отечественным оригинаторам'
    )
    is_nanoc = django_filters.BooleanFilter(
        field_name='is_nanoc',
        help_text='Фильтр по НАНОЦ оригинаторам'
    )
    country = django_filters.CharFilter(
        field_name='country',
        help_text='Фильтр по ISO коду страны (например, KZ, RU, DE)'
    )
    has_code = django_filters.BooleanFilter(
        method='filter_has_code',
        help_text='Фильтр по наличию кода'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        help_text='Поиск по названию или коду'
    )

    class Meta:
        model = Originator
        fields = ['is_foreign', 'is_nanoc', 'country', 'has_code', 'search']

    def filter_has_code(self, queryset, name, value):
        """Фильтр по наличию кода"""
        if value is True:
            return queryset.exclude(code__isnull=True)
        elif value is False:
            return queryset.filter(code__isnull=True)
        return queryset

    def filter_search(self, queryset, name, value):
        """Поиск по названию или коду"""
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(code__icontains=value)
            )
        return queryset


class ApplicationFilter(django_filters.FilterSet):
    """
    Фильтр для заявок на сортоиспытания
    
    Поддерживает фильтрацию по:
    - Группе культур (culture_group) - локальный ID группы культур
    - Группе культур по названию (culture_group_name) - поиск по названию группы
    - Конкретной культуре (culture) - локальный ID культуры
    - Культуре из Patents Service (patents_culture_id) - ID культуры в Patents Service
    - Группе культур из Patents Service (patents_group_id) - ID группы культур в Patents Service
    - Статусу заявки (status)
    - Области (oblast) - ID области
    - Году подачи заявки (year)
    - Поиск по номеру заявки или названию сорта (search)
    - Поиск по группе культур (group_search) - поиск по названию группы культур
    """
    culture_group = django_filters.NumberFilter(
        field_name='sort_record__culture__group_culture',
        help_text='ID группы культур (локальный ID)'
    )
    culture_group_name = django_filters.CharFilter(
        method='filter_culture_group_name',
        help_text='Поиск по названию группы культур'
    )
    culture = django_filters.NumberFilter(
        field_name='sort_record__culture',
        help_text='ID культуры (локальный ID)'
    )
    patents_culture_id = django_filters.NumberFilter(
        field_name='sort_record__culture__culture_id',
        help_text='ID культуры в Patents Service'
    )
    patents_group_id = django_filters.NumberFilter(
        field_name='sort_record__culture__group_culture__group_culture_id',
        help_text='ID группы культур в Patents Service'
    )
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Application.STATUS_CHOICES,
        help_text='Статус заявки'
    )
    oblast = django_filters.NumberFilter(
        field_name='target_oblasts',
        help_text='ID области'
    )
    year = django_filters.NumberFilter(
        field_name='submission_date__year',
        help_text='Год подачи заявки'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        help_text='Поиск по номеру заявки или названию сорта'
    )
    group_search = django_filters.CharFilter(
        method='filter_group_search',
        help_text='Поиск по названию группы культур'
    )
    has_documents = django_filters.BooleanFilter(
        method='filter_has_documents',
        help_text='true — все обязательные документы загружены, false — есть недостающие'
    )

    class Meta:
        model = Application
        fields = ['culture_group', 'culture_group_name', 'culture', 'patents_culture_id', 'patents_group_id', 'status', 'oblast', 'year', 'search', 'group_search', 'has_documents']

    def filter_culture_group_name(self, queryset, name, value):
        """Фильтр по названию группы культур"""
        if value:
            return queryset.filter(
                sort_record__culture__group_culture__name__icontains=value
            )
        return queryset

    def filter_group_search(self, queryset, name, value):
        """Поиск по названию группы культур"""
        if value:
            return queryset.filter(
                Q(sort_record__culture__group_culture__name__icontains=value) |
                Q(sort_record__culture__group_culture__code__icontains=value)
            )
        return queryset

    def filter_has_documents(self, queryset, name, value):
        """Фильтр по наличию всех обязательных документов"""
        mandatory_count = len(APPLICATION_MANDATORY_DOCUMENT_TYPES)
        if mandatory_count == 0:
            return queryset

        # Подсчитываем количество обязательных типов документов у каждой заявки
        qs = queryset.annotate(
            mandatory_docs_count=Count(
                'documents',
                filter=Q(
                    documents__is_deleted=False,
                    documents__document_type__in=APPLICATION_MANDATORY_DOCUMENT_TYPES,
                ),
                distinct=True,
            )
        )
        if value:
            return qs.filter(mandatory_docs_count__gte=mandatory_count)
        else:
            return qs.filter(mandatory_docs_count__lt=mandatory_count)

    def filter_search(self, queryset, name, value):
        """Поиск по номеру заявки или названию сорта"""
        if value:
            return queryset.filter(
                Q(application_number__icontains=value) |
                Q(sort_record__name__icontains=value)
            )
        return queryset


class TrialFilter(django_filters.FilterSet):
    """
    Фильтр для испытаний сортов

    Поддерживает фильтрацию по:
    - status — статус испытания (planned, active, completed_008, ...)
    - oblast — ID области (через region__oblast)
    - region — ID ГСУ/региона
    - trial_type — ID типа испытания
    - culture — ID культуры (локальный)
    - year — год проведения испытания
    - search — поиск по названию сорта, номеру заявки, названию ГСУ
    """
    status = django_filters.CharFilter(
        method='filter_status',
        help_text='Статус испытания (planned, active, ...) или решение (approved, continue, rejected)'
    )
    oblast = django_filters.NumberFilter(
        field_name='region__oblast',
        help_text='ID области'
    )
    region = django_filters.NumberFilter(
        field_name='region',
        help_text='ID ГСУ/региона'
    )
    trial_type = django_filters.NumberFilter(
        field_name='trial_type',
        help_text='ID типа испытания'
    )
    trial_type_code = django_filters.CharFilter(
        field_name='trial_type__code',
        help_text='Код типа испытания'
    )
    culture = django_filters.NumberFilter(
        field_name='culture',
        help_text='ID культуры (локальный)'
    )
    year = django_filters.NumberFilter(
        field_name='year',
        help_text='Год проведения испытания'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        help_text='Поиск по названию сорта, номеру заявки или ГСУ'
    )

    class Meta:
        model = Trial
        fields = [
            'status', 'oblast', 'region', 'trial_type',
            'trial_type_code', 'culture', 'year', 'search',
        ]

    # Значения decision, которые фронтенд передаёт как status
    DECISION_VALUES = {v for v, _ in Trial.DECISION_CHOICES}

    def filter_status(self, queryset, name, value):
        """
        Фильтр по статусу или решению.

        STATUS_CHOICES: planned, active, completed_008, lab_sample_sent, lab_completed, completed
        DECISION_CHOICES: approved, continue, rejected — хранятся в поле decision
        """
        if not value:
            return queryset
        if value in self.DECISION_VALUES:
            return queryset.filter(decision=value)
        return queryset.filter(status=value)

    def filter_search(self, queryset, name, value):
        """Поиск по названию сорта, номеру заявки или ГСУ"""
        if value:
            return queryset.filter(
                Q(region__name__icontains=value) |
                Q(culture__name__icontains=value) |
                Q(participants__sort_record__name__icontains=value) |
                Q(participants__application__application_number__icontains=value)
            ).distinct()
        return queryset
