from django.db.models import Count, Q

from ..models import Culture, GroupCulture


class PatentsCatalogService:
    """Read-model adapter for locally synced patents catalogs."""

    @staticmethod
    def serialize_group_culture(group_culture):
        return {
            'id': group_culture.group_culture_id,
            'local_id': group_culture.id,
            'group_culture_id': group_culture.group_culture_id,
            'name': group_culture.name,
            'description': group_culture.description,
            'code': group_culture.code,
            'cultures_count': getattr(group_culture, 'cultures_count', 0),
            'created_at': group_culture.created_at,
            'updated_at': group_culture.updated_at,
            'synced_at': group_culture.synced_at,
        }

    @classmethod
    def list_group_cultures(cls, *, search=None):
        queryset = GroupCulture.objects.filter(is_deleted=False).annotate(
            cultures_count=Count('cultures', filter=Q(cultures__is_deleted=False), distinct=True)
        )

        if search:
            queryset = queryset.filter(name__icontains=search)

        return [cls.serialize_group_culture(group_culture) for group_culture in queryset]

    @classmethod
    def get_group_culture(cls, group_culture_id):
        group_culture = GroupCulture.objects.filter(
            group_culture_id=group_culture_id,
            is_deleted=False,
        ).annotate(
            cultures_count=Count('cultures', filter=Q(cultures__is_deleted=False), distinct=True)
        ).first()

        if not group_culture:
            return None

        return cls.serialize_group_culture(group_culture)

    @staticmethod
    def serialize_culture(culture):
        external_group_id = culture.group_culture.group_culture_id if culture.group_culture else None
        group_name = culture.group_culture.name if culture.group_culture else None

        return {
            'id': culture.culture_id,
            'local_id': culture.id,
            'patents_culture_id': culture.culture_id,
            'name': culture.name,
            'code': culture.code,
            'culture_group': external_group_id,
            'culture_group_name': group_name,
            'group_culture': external_group_id,
            'group_culture_id': external_group_id,
            'group_culture_name': group_name,
            'created_at': culture.created_at,
            'updated_at': culture.updated_at,
            'synced_at': culture.synced_at,
        }

    @classmethod
    def list_cultures(cls, *, group=None, search=None):
        queryset = Culture.objects.select_related('group_culture').filter(is_deleted=False)

        if group:
            queryset = queryset.filter(group_culture__group_culture_id=group)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return [cls.serialize_culture(culture) for culture in queryset]

    @classmethod
    def get_culture(cls, culture_id):
        culture = Culture.objects.select_related('group_culture').filter(
            culture_id=culture_id,
            is_deleted=False,
        ).first()

        if not culture:
            return None

        return cls.serialize_culture(culture)
