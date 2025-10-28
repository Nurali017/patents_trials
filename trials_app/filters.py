"""
Фильтры для API endpoints
"""
import django_filters
from django.db.models import Q
from .models import Originator, Application, Trial, TrialPlan, Culture, GroupCulture


class OriginatorFilter(django_filters.FilterSet):
    """
    Фильтр для оригинаторов с новыми полями
    """
    is_foreign = django_filters.BooleanFilter(
        field_name='is_foreign',
        help_text='Фильтр по иностранным/отечественным оригинаторам'
    )
    is_nanoc = django_filters.BooleanFilter(
        field_name='is_nanoc',
        help_text='Фильтр по НАНОЦ оригинаторам'
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
        fields = ['is_foreign', 'is_nanoc', 'has_code', 'search']

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
        field_name='created_at__year',
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

    class Meta:
        model = Application
        fields = ['culture_group', 'culture_group_name', 'culture', 'patents_culture_id', 'patents_group_id', 'status', 'oblast', 'year', 'search', 'group_search']

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

    def filter_search(self, queryset, name, value):
        """Поиск по номеру заявки или названию сорта"""
        if value:
            return queryset.filter(
                Q(application_number__icontains=value) |
                Q(sort_record__name__icontains=value)
            )
        return queryset
