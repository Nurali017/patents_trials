"""
Фильтры для API endpoints
"""
import django_filters
from django.db.models import Q
from .models import Originator


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
