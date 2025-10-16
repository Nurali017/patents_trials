"""
Сериализаторы для годовых таблиц решений (Annual Decision Tables)
"""
from rest_framework import serializers
from .models import AnnualDecisionTable, AnnualDecisionItem
from .serializers import SortRecordSerializer


class AnnualDecisionTableSerializer(serializers.ModelSerializer):
    """Сериализатор для годовой таблицы решений"""
    oblast_name = serializers.CharField(source='oblast.name', read_only=True)
    culture_name = serializers.CharField(source='culture.name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnualDecisionTable
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'title']
    
    def get_items_count(self, obj):
        """Количество элементов в таблице"""
        return obj.items.filter(is_deleted=False).count()


class AnnualDecisionItemSerializer(serializers.ModelSerializer):
    """Сериализатор элемента годовой таблицы"""
    sort_record_data = SortRecordSerializer(source='sort_record', read_only=True)
    decision_display = serializers.CharField(source='get_decision_display', read_only=True)
    decided_by_name = serializers.CharField(source='decided_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = AnnualDecisionItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AnnualDecisionTableDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор таблицы с элементами"""
    oblast_name = serializers.CharField(source='oblast.name', read_only=True)
    culture_name = serializers.CharField(source='culture.name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    items = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnualDecisionTable
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'title']
    
    def get_items(self, obj):
        """Элементы таблицы"""
        items = obj.items.filter(is_deleted=False).order_by('row_number')
        return AnnualDecisionItemSerializer(items, many=True).data
    
    def get_statistics(self, obj):
        """Статистика таблицы"""
        items = obj.items.filter(is_deleted=False)
        return {
            'total': items.count(),
            'approved': items.filter(decision='approved').count(),
            'removed': items.filter(decision='removed').count(),
            'continue': items.filter(decision='continue').count(),
            'pending': items.filter(decision='pending').count(),
        }


class AnnualDecisionTableCreateSerializer(serializers.Serializer):
    """Сериализатор для создания таблицы"""
    year = serializers.IntegerField()
    oblast = serializers.IntegerField()
    culture = serializers.IntegerField(required=False, allow_null=True)
    auto_populate = serializers.BooleanField(default=True)
    include_year_3 = serializers.BooleanField(default=True)
    include_year_2 = serializers.BooleanField(default=True)
    include_year_1 = serializers.BooleanField(default=False)


class AnnualDecisionItemDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор элемента с дополнительными данными"""
    sort_record_data = SortRecordSerializer(source='sort_record', read_only=True)
    decision_display = serializers.CharField(source='get_decision_display', read_only=True)
    decided_by_name = serializers.CharField(source='decided_by.username', read_only=True, allow_null=True)
    trials_data = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnualDecisionItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_trials_data(self, obj):
        """Данные испытаний сорта"""
        # Получить испытания через TrialPlanParticipant
        from .models import TrialPlanParticipant
        participants = TrialPlanParticipant.objects.filter(
            patents_sort_id=obj.sort_record.sort_id,
            is_deleted=False
        ).select_related('trial_plan')
        
        trials = []
        for participant in participants:
            trials.append({
                'id': participant.trial_plan.id,
                'year': participant.trial_plan.year,
                'status': participant.trial_plan.status,
                'status_display': participant.trial_plan.get_status_display(),
            })
        
        return trials


class AnnualDecisionItemUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления решения"""
    decision = serializers.ChoiceField(
        choices=['pending', 'approved', 'continue', 'removed']
    )
    decision_justification = serializers.CharField(required=False, allow_blank=True)
    decision_recommendations = serializers.CharField(required=False, allow_blank=True)
    recommended_zones = serializers.JSONField(required=False)
    continue_reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    continue_until_year = serializers.IntegerField(required=False, allow_null=True)
    removal_reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)

