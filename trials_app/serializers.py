from rest_framework import serializers
from .models import (
    Oblast, Region, ClimateZone, Indicator, GroupCulture, Culture, Originator, SortOriginator, SortRecord, 
    Application, PlannedDistribution, TrialType, Trial, TrialParticipant, TrialResult, 
    TrialLaboratoryResult, Document, TrialPlan, TrialPlanParticipant, TrialPlanTrial, TrialPlanCulture,
    AnnualDecisionTable, AnnualDecisionItem
)


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def validate_and_normalize_predecessor(predecessor):
    """
    Валидация и нормализация значения предшественника
    
    Args:
        predecessor: значение предшественника (может быть строкой, числом)
        
    Returns:
        Нормализованное значение: 'fallow' или int (culture_id)
        
    Raises:
        ValidationError: если значение невалидно
    """
    from rest_framework import serializers
    
    if not predecessor and predecessor != 0:
        raise serializers.ValidationError("predecessor is required")
    
    # Если это 'fallow'
    if predecessor == 'fallow':
        return 'fallow'
    
    # Если это целое число
    if isinstance(predecessor, int) and predecessor > 0:
        return predecessor
    
    # Если это строка
    if isinstance(predecessor, str):
        # Проверяем на 'fallow'
        if predecessor.lower() == 'fallow':
            return 'fallow'
        
        # Пробуем преобразовать в число
        try:
            culture_id = int(predecessor)
            if culture_id <= 0:
                raise serializers.ValidationError("culture_id must be positive")
            return culture_id
        except ValueError:
            raise serializers.ValidationError(
                "predecessor must be either 'fallow' or a positive culture_id (integer)"
            )
    
    raise serializers.ValidationError(
        "predecessor must be either 'fallow' or a positive culture_id (integer)"
    )


def create_basic_trial_results(participant, created_by):
    """
    Автоматически создать пустые TrialResult для ОСНОВНЫХ показателей
    
    Вызывается при создании TrialParticipant.
    Создает пустые записи для всех основных показателей (is_quality=False),
    чтобы сортопыт мог их заполнить.
    
    Args:
        participant: TrialParticipant instance
        created_by: User who creates the results
    
    Returns:
        list: Созданные TrialResult объекты
    """
    results_created = []
    
    # Получить только ОСНОВНЫЕ показатели (не качественные)
    basic_indicators = participant.trial.indicators.filter(
        is_quality=False,
        is_deleted=False
    )
    
    for indicator in basic_indicators:
        result, created = TrialResult.objects.get_or_create(
            participant=participant,
            indicator=indicator,
            defaults={
                'trial': participant.trial,
                'sort_record': participant.sort_record,
                'created_by': created_by,
                'value': None,  # Пустое значение - заполнит сортопыт
            }
        )
        if created:
            results_created.append(result)
    
    return results_created


def create_quality_trial_results(trial, created_by):
    """
    Автоматически создать пустые TrialResult для КАЧЕСТВЕННЫХ показателей
    
    Вызывается при отправке образца в лабораторию (mark_sent_to_lab).
    Создает пустые записи для всех качественных показателей (is_quality=True)
    для ВСЕХ участников испытания.
    
    Args:
        trial: Trial instance
        created_by: User who creates the results
    
    Returns:
        list: Созданные TrialResult объекты
    """
    results_created = []
    
    # Получить только КАЧЕСТВЕННЫЕ показатели
    quality_indicators = trial.indicators.filter(
        is_quality=True,
        is_deleted=False
    )
    
    # Для каждого участника создать качественные показатели
    for participant in trial.participants.filter(is_deleted=False):
        for indicator in quality_indicators:
            result, created = TrialResult.objects.get_or_create(
                participant=participant,
                indicator=indicator,
                defaults={
                    'trial': trial,
                    'sort_record': participant.sort_record,
                    'created_by': created_by,
                    'value': None,  # Пустое значение - заполнит лаборатория
                }
            )
            if created:
                results_created.append(result)
    
    return results_created


# ============================================================================
# СЕРИАЛИЗАТОРЫ
# ============================================================================

class OblastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oblast
        fields = '__all__'

class ClimateZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateZone
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    oblast_name = serializers.CharField(source='oblast.name', read_only=True)
    climate_zone_name = serializers.CharField(source='climate_zone.name', read_only=True)
    
    class Meta:
        model = Region
        fields = '__all__'

class GroupCultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCulture
        fields = '__all__'

class CultureSerializer(serializers.ModelSerializer):
    group_culture_name = serializers.CharField(source='group_culture.name', read_only=True)
    
    class Meta:
        model = Culture
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    # Показываем группы культур
    group_cultures_data = GroupCultureSerializer(source='group_cultures', many=True, read_only=True)
    
    # Дополнительно: количество культур, на которые распространяется показатель
    applicable_cultures_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Indicator
        fields = '__all__'
    
    def get_applicable_cultures_count(self, obj):
        """Подсчитать количество культур через группы"""
        if obj.is_universal:
            from trials_app.models import Culture
            return Culture.objects.filter(is_deleted=False).count()
        return obj.get_applicable_cultures().count()

class TrialTypeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = TrialType
        fields = '__all__'

class OriginatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Originator
        fields = '__all__'

class SortOriginatorSerializer(serializers.ModelSerializer):
    """Сериализатор для связи сорта с оригинатором"""
    originator_name = serializers.CharField(source='originator.name', read_only=True)
    originator_patents_id = serializers.IntegerField(source='originator.originator_id', read_only=True)
    
    class Meta:
        model = SortOriginator
        fields = ['id', 'originator', 'originator_name', 'originator_patents_id', 'percentage']


class SortRecordSerializer(serializers.ModelSerializer):
    patents_sort_data = serializers.ReadOnlyField()
    culture_name = serializers.CharField(source='culture.name', read_only=True)
    group_culture_name = serializers.CharField(source='culture.group_culture.name', read_only=True, allow_null=True)
    patents_status_display = serializers.CharField(source='get_patents_status_display', read_only=True)
    
    # Оригинаторы (список с процентами)
    originators = serializers.SerializerMethodField()
    
    class Meta:
        model = SortRecord
        fields = '__all__'
    
    def get_originators(self, obj):
        """Получить список оригинаторов сорта"""
        from trials_app.models import SortOriginator
        sort_originators = SortOriginator.objects.filter(
            sort_record=obj
        ).select_related('originator')
        return SortOriginatorSerializer(sort_originators, many=True).data


class ApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок на испытания"""
    sort_record_data = SortRecordSerializer(source='sort_record', read_only=True)
    target_oblasts_data = OblastSerializer(source='target_oblasts', many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    # Принимаем sort_id из Patents Service
    sort_id = serializers.IntegerField(write_only=True, required=False)
    
    # Статистика по испытаниям (через TrialParticipant)
    regional_trials_count = serializers.SerializerMethodField()
    decisions_summary = serializers.SerializerMethodField()
    
    # Информация о документах
    missing_mandatory_documents = serializers.SerializerMethodField()
    is_ready_for_submission = serializers.SerializerMethodField()
    
    # Распределения из таблицы (для обратной совместимости с фронтом)
    planned_distributions = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'sort_record': {'required': False},
            'created_by': {'read_only': True}  # Устанавливается автоматически
        }
    
    def get_regional_trials_count(self, obj):
        """Количество испытаний по областям (через TrialParticipant)"""
        from trials_app.models import TrialParticipant, Trial
        trial_ids = TrialParticipant.objects.filter(
            application=obj,
            is_deleted=False
        ).values_list('trial_id', flat=True).distinct()
        
        return Trial.objects.filter(
            id__in=trial_ids,
            is_deleted=False
        ).count()
    
    def get_decisions_summary(self, obj):
        """Сводка по решениям (через TrialParticipant)"""
        from trials_app.models import TrialParticipant, Trial
        trial_ids = TrialParticipant.objects.filter(
            application=obj,
            is_deleted=False
        ).values_list('trial_id', flat=True).distinct()
        
        trials = Trial.objects.filter(
            id__in=trial_ids,
            is_deleted=False
        )
        decisions = trials.exclude(decision__isnull=True).exclude(decision='')
        
        return {
            'total': trials.count(),
            'with_decision': decisions.count(),
            'approved': decisions.filter(decision='approved').count(),
            'continue': decisions.filter(decision='continue').count(),
            'rejected': decisions.filter(decision='rejected').count(),
        }
    
    def get_missing_mandatory_documents(self, obj):
        """Список отсутствующих обязательных документов"""
        return obj.get_missing_mandatory_documents()
    
    def get_is_ready_for_submission(self, obj):
        """Готовность заявки к подаче"""
        return obj.is_ready_for_submission()
    
    def get_planned_distributions(self, obj):
        """
        Получить распределения из таблицы PlannedDistribution
        Возвращает в том же JSON формате, что ожидает фронтенд
        """
        distributions = PlannedDistribution.objects.filter(
            application=obj,
            is_deleted=False
        )
        
        result = []
        for dist in distributions:
            dist_data = {
                'region': dist.region.id,
            }
            if dist.trial_type:
                dist_data['trial_type'] = dist.trial_type.code
            if dist.planting_season:
                dist_data['planting_season'] = dist.planting_season
            result.append(dist_data)
        
        return result
    
    def validate_applicant_inn_bin(self, value):
        """Валидация ИНН/БИН (должен состоять из 12 цифр)"""
        if value and not value.isdigit():
            raise serializers.ValidationError("ИНН/БИН должен содержать только цифры")
        if value and len(value) != 12:
            raise serializers.ValidationError("ИНН/БИН должен содержать ровно 12 цифр")
        return value
    
    def validate(self, data):
        """Проверка что указан либо sort_id, либо sort_record"""
        if not data.get('sort_id') and not data.get('sort_record'):
            raise serializers.ValidationError({
                'sort_id': 'Необходимо указать sort_id (ID из Patents Service) или sort_record'
            })
        return data
    
    def create(self, validated_data):
        """Автоматически создать SortRecord если передан sort_id"""
        from django.utils import timezone
        from datetime import timedelta
        
        sort_id = validated_data.pop('sort_id', None)
        
        if sort_id:
            # Найти или создать SortRecord по sort_id
            sort_record, created = SortRecord.objects.get_or_create(
                sort_id=sort_id,
                defaults={'name': f'Сорт {sort_id}'}
            )
            
            # Синхронизировать если:
            # - Новый объект (created=True)
            # - Данные старше 1 дня
            # - Никогда не синхронизировался (synced_at=None)
            should_sync = (
                created or 
                not sort_record.synced_at or
                (timezone.now() - sort_record.synced_at) > timedelta(days=1)
            )
            
            if should_sync:
                sort_record.sync_from_patents()
            
            validated_data['sort_record'] = sort_record
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Автоматически обновить SortRecord если передан sort_id"""
        from django.utils import timezone
        from datetime import timedelta
        
        sort_id = validated_data.pop('sort_id', None)
        
        if sort_id:
            # Найти или создать SortRecord по sort_id
            sort_record, created = SortRecord.objects.get_or_create(
                sort_id=sort_id,
                defaults={'name': f'Сорт {sort_id}'}
            )
            
            # Синхронизировать если:
            # - Новый объект (created=True)
            # - Данные старше 1 дня
            # - Никогда не синхронизировался (synced_at=None)
            should_sync = (
                created or 
                not sort_record.synced_at or
                (timezone.now() - sort_record.synced_at) > timedelta(days=1)
            )
            
            if should_sync:
                sort_record.sync_from_patents()
            
            validated_data['sort_record'] = sort_record
        
        return super().update(instance, validated_data)


class TrialParticipantSerializer(serializers.ModelSerializer):
    """Сериализатор участника сортоопыта"""
    sort_record_data = SortRecordSerializer(source='sort_record', read_only=True)
    application_number = serializers.CharField(source='application.application_number', read_only=True, allow_null=True)
    statistical_group_display = serializers.CharField(source='get_statistical_group_display', read_only=True)
    statistical_result_display = serializers.CharField(source='get_statistical_result_display', read_only=True)
    
    class Meta:
        model = TrialParticipant
        fields = '__all__'
        read_only_fields = ['statistical_result', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Валидация участника перед добавлением в испытание
        """
        trial = data.get('trial')
        sort_record = data.get('sort_record')
        
        # ПРАВИЛО: Культура сорта должна совпадать с культурой испытания
        if trial and trial.culture and sort_record:
            # Если у сорта нет культуры
            if not sort_record.culture:
                raise serializers.ValidationError({
                    'sort_record': f'У сорта "{sort_record.name}" не указана культура. '
                                  f'Для участия в испытании культуры "{trial.culture.name}" '
                                  f'необходимо указать культуру сорта.'
                })
            
            # Если культуры не совпадают
            if trial.culture.id != sort_record.culture.id:
                raise serializers.ValidationError({
                    'sort_record': f'Сорт "{sort_record.name}" относится к культуре "{sort_record.culture.name}", '
                                  f'но испытание проводится для культуры "{trial.culture.name}". '
                                  f'Можно добавить только сорта культуры "{trial.culture.name}".'
                })
        
        return data


class TrialSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(source='application.application_number', read_only=True)
    sort_record_data = serializers.SerializerMethodField()
    region_name = serializers.CharField(source='region.name', read_only=True)
    oblast_name = serializers.CharField(source='region.oblast.name', read_only=True)
    climate_zone_name = serializers.CharField(source='region.climate_zone.name', read_only=True)
    culture_name = serializers.CharField(source='culture.name', read_only=True, allow_null=True)
    predecessor_culture_name = serializers.CharField(source='predecessor_culture.name', read_only=True, allow_null=True)
    decided_by_name = serializers.CharField(source='decided_by.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    sort_records_data = SortRecordSerializer(source='sort_records', many=True, read_only=True)
    indicators_data = IndicatorSerializer(source='indicators', many=True, read_only=True)
    trial_type_data = TrialTypeSerializer(source='trial_type', read_only=True)
    results_count = serializers.SerializerMethodField()
    
    # Новые поля для работы с участниками
    participants_data = TrialParticipantSerializer(source='participants', many=True, read_only=True)
    completion_status = serializers.SerializerMethodField()
    trial_statistics = serializers.SerializerMethodField()
    
    # Для создания с участниками
    participants = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        help_text="Список участников для создания"
    )
    
    class Meta:
        model = Trial
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},  # Устанавливается автоматически
            'indicators': {'required': False}   # Назначаются автоматически по культуре
        }
    
    def get_sort_record_data(self, obj):
        """Получить данные сорта (из заявки или напрямую)"""
        sort_record = obj.get_sort_record()
        if sort_record:
            return SortRecordSerializer(sort_record).data
        return None
    
    def get_results_count(self, obj):
        """Количество результатов измерений"""
        return obj.results.filter(is_deleted=False).count()
    
    def get_completion_status(self, obj):
        """Статус заполненности данных"""
        return obj.get_completion_status()
    
    def get_trial_statistics(self, obj):
        """Статистика опыта (Sx, P%, НСР, E)"""
        return obj.calculate_trial_statistics()
    
    def validate(self, data):
        """Валидация данных перед созданием"""
        from rest_framework import serializers
        
        # Проверить что region существует
        if 'region' in data:
            from trials_app.models import Region
            if not Region.objects.filter(id=data['region'].id, is_deleted=False).exists():
                raise serializers.ValidationError({
                    'region': f'Region с ID {data["region"].id} не найден'
                })
        
        # Проверить что culture существует (если указана)
        if 'culture' in data and data['culture']:
            from trials_app.models import Culture
            if not Culture.objects.filter(id=data['culture'].id, is_deleted=False).exists():
                raise serializers.ValidationError({
                    'culture': f'Culture с ID {data["culture"].id} не найдена'
                })
        
        # Проверить что trial_type существует (если указан)
        if 'trial_type' in data and data['trial_type']:
            from trials_app.models import TrialType
            if not TrialType.objects.filter(id=data['trial_type'].id, is_deleted=False).exists():
                raise serializers.ValidationError({
                    'trial_type': f'TrialType с ID {data["trial_type"].id} не найден'
                })
        
        return data
    
    def create(self, validated_data):
        """Создать испытание с участниками"""
        from rest_framework import serializers
        
        participants_data = validated_data.pop('participants', [])
        
        # Убедимся что indicators это список ID, а не QuerySet
        if 'indicators' in validated_data:
            indicators = validated_data.pop('indicators', [])
        else:
            indicators = []
        
        # Проверить что все indicators существуют
        if indicators:
            from trials_app.models import Indicator
            indicator_ids = [ind.id if hasattr(ind, 'id') else ind for ind in indicators]
            existing_indicators = Indicator.objects.filter(
                id__in=indicator_ids, 
                is_deleted=False
            ).values_list('id', flat=True)
            missing = set(indicator_ids) - set(existing_indicators)
            if missing:
                raise serializers.ValidationError({
                    'indicators': f'Indicators с ID {list(missing)} не найдены'
                })
        
        # Обработать participants: создать SortRecord из Patents ID если нужно
        if participants_data:
            from trials_app.models import SortRecord
            from django.utils import timezone
            from datetime import timedelta
            
            for p_data in participants_data:
                # Если передан patents_sort_id, создать/получить SortRecord
                if 'patents_sort_id' in p_data:
                    patents_sort_id = p_data.pop('patents_sort_id')
                    
                    # Найти или создать SortRecord
                    sort_record, created = SortRecord.objects.get_or_create(
                        sort_id=patents_sort_id,
                        defaults={'name': f'Сорт {patents_sort_id}'}
                    )
                    
                    # Синхронизировать если нужно
                    should_sync = (
                        created or 
                        not sort_record.synced_at or
                        (timezone.now() - sort_record.synced_at) > timedelta(days=1)
                    )
                    
                    if should_sync:
                        sort_record.sync_from_patents()
                    
                    # Заменить patents_sort_id на sort_record
                    p_data['sort_record'] = sort_record.id
                
                # Проверить что sort_record указан
                if 'sort_record' not in p_data:
                    raise serializers.ValidationError({
                        'participants': 'Необходимо указать sort_record или patents_sort_id'
                    })
            
            # Проверить что все sort_records существуют
            sort_record_ids = [p['sort_record'] for p in participants_data]
            existing_sorts = SortRecord.objects.filter(
                id__in=sort_record_ids,
                is_deleted=False
            ).values_list('id', flat=True)
            missing = set(sort_record_ids) - set(existing_sorts)
            if missing:
                raise serializers.ValidationError({
                    'participants': f'SortRecord с ID {list(missing)} не найдены'
                })
        
        trial = super().create(validated_data)
        
        # АВТОМАТИЧЕСКОЕ НАЗНАЧЕНИЕ ПОКАЗАТЕЛЕЙ ПО КУЛЬТУРЕ
        # Если indicators не указаны, берем все показатели группы культуры
        if not indicators and trial.culture:
            from trials_app.models import Indicator
            
            if trial.culture.group_culture:
                # Получить все показатели для ГРУППЫ этой культуры (НОВАЯ ЛОГИКА)
                auto_indicators = Indicator.objects.filter(
                    group_cultures=trial.culture.group_culture,
                    is_deleted=False
                ).distinct()
                
                trial.indicators.set(auto_indicators)
            else:
                # Если у культуры нет группы - не назначаем показатели автоматически
                pass
        elif indicators:
            # Если indicators указаны явно - используем их
            trial.indicators.set(indicators)
        
        # АВТОМАТИЧЕСКИЙ СТАТУС: испытание всегда создается с участниками → active
        trial.status = 'active'
        trial.save()
        
        # Создать участников
        from django.core.exceptions import ValidationError as DjangoValidationError
        
        created_participants = []
        for p_data in participants_data:
            try:
                participant = TrialParticipant.objects.create(
                    trial=trial,
                    sort_record_id=p_data['sort_record'],
                    statistical_group=p_data.get('statistical_group', 1),
                    participant_number=p_data['participant_number'],
                    application_id=p_data.get('application'),
                )
                created_participants.append(participant)
                
                # АВТОМАТИЧЕСКИ СОЗДАТЬ ОСНОВНЫЕ ПОКАЗАТЕЛИ ДЛЯ СОРТОПЫТА
                create_basic_trial_results(participant, self.context['request'].user)
                
            except DjangoValidationError as e:
                # Преобразовать Django ValidationError в DRF ValidationError
                trial.delete()  # Откатить создание испытания
                error_messages = []
                if hasattr(e, 'message_dict'):
                    for field, messages in e.message_dict.items():
                        error_messages.extend(messages)
                else:
                    error_messages = [str(e)]
                raise serializers.ValidationError({
                    'participants': error_messages
                })
        
        # АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ СТАТУСА ЗАЯВКИ И PlannedDistribution:
        application_ids = set()
        for p_data in participants_data:
            if p_data.get('application'):
                application_ids.add(p_data['application'])
        
        if application_ids:
            from trials_app.models import Application, PlannedDistribution
            
            # Обновляем общий статус заявки
            Application.objects.filter(
                id__in=application_ids,
                status='distributed'  # Только если была distributed
            ).update(status='in_progress')
            
            # Обновляем PlannedDistribution (многолетние испытания)
            for app_id in application_ids:
                planned_dist = PlannedDistribution.objects.filter(
                    application_id=app_id,
                    region=trial.region
                ).first()
                
                if planned_dist:
                    # Если первый Trial для этого PlannedDistribution
                    if planned_dist.status == 'planned':
                        planned_dist.status = 'in_progress'
                        planned_dist.year_started = trial.year or (trial.start_date.year if trial.start_date else None)
                        planned_dist.save()
        
        return trial

class TrialResultSerializer(serializers.ModelSerializer):
    sort_name = serializers.CharField(source='sort_record.name', read_only=True, allow_null=True)
    indicator_name = serializers.CharField(source='indicator.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    participant_data = TrialParticipantSerializer(source='participant', read_only=True)
    
    # Для bulk ввода данных по делянкам
    plots = serializers.ListField(
        child=serializers.FloatField(allow_null=True),
        write_only=True,
        required=False,
        help_text="Массив значений по делянкам [plot_1, plot_2, plot_3, plot_4]"
    )
    
    class Meta:
        model = TrialResult
        fields = '__all__'
        read_only_fields = ['value', 'trial', 'sort_record', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Создать результат с возможностью передачи делянок массивом"""
        plots = validated_data.pop('plots', None)
        
        if plots and len(plots) == 4:
            validated_data['plot_1'] = plots[0]
            validated_data['plot_2'] = plots[1]
            validated_data['plot_3'] = plots[2]
            validated_data['plot_4'] = plots[3]
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Обновить результат с возможностью передачи делянок массивом"""
        plots = validated_data.pop('plots', None)
        
        if plots and len(plots) == 4:
            validated_data['plot_1'] = plots[0]
            validated_data['plot_2'] = plots[1]
            validated_data['plot_3'] = plots[2]
            validated_data['plot_4'] = plots[3]
        
        return super().update(instance, validated_data)

class TrialLaboratoryResultSerializer(serializers.ModelSerializer):
    """
    Сериализатор для лабораторных результатов испытания
    
    Используется для внесения качественных показателей (белок, клейковина, натура)
    после завершения полевых испытаний.
    """
    trial_id = serializers.IntegerField(source='trial.id', read_only=True)
    trial_region = serializers.CharField(source='trial.region.name', read_only=True)
    trial_oblast = serializers.CharField(source='trial.region.oblast.name', read_only=True)
    indicator_name = serializers.CharField(source='indicator.name', read_only=True)
    indicator_unit = serializers.CharField(source='indicator.unit', read_only=True)
    participant_data = TrialParticipantSerializer(source='participant', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = TrialLaboratoryResult
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_indicator(self, value):
        """Проверить что показатель качественный"""
        if not value.is_quality:
            raise serializers.ValidationError(
                f'Показатель "{value.name}" не является качественным. '
                f'Для лабораторных результатов можно использовать только показатели '
                f'с is_quality=True (белок, клейковина, натура зерна и т.д.)'
            )
        return value
    
    def validate_trial(self, value):
        """Проверить что испытание завершено"""
        if value.status not in ['completed', 'lab_sample_sent', 'lab_completed']:
            raise serializers.ValidationError(
                f'Испытание #{value.id} должно быть завершено (status=completed) '
                f'перед внесением лабораторных результатов. '
                f'Текущий статус: {value.get_status_display()}'
            )
        return value


class DocumentSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(source='application.application_number', read_only=True, allow_null=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = Document
        fields = '__all__'
        extra_kwargs = {
            'uploaded_by': {'read_only': True}  # Устанавливается автоматически
        }


class TrialPlanWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи планов испытаний"""
    
    # Явно определяем опциональные поля для работы с null=True, blank=True
    trial_type = serializers.PrimaryKeyRelatedField(
        queryset=TrialType.objects.filter(is_deleted=False),
        required=False,
        allow_null=True,
        help_text="Тип испытания по умолчанию (опционально)"
    )
    
    class Meta:
        model = TrialPlan
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},  # Устанавливается автоматически
            'total_varieties': {'read_only': True},  # Вычисляется автоматически
        }
    
    def validate(self, data):
        """Валидация данных перед созданием"""
        return data
    
    def create(self, validated_data):
        """Создать план с автоматическим обновлением статистики"""
        plan = super().create(validated_data)
        plan.update_statistics()
        return plan
    
    def update(self, instance, validated_data):
        """Обновить план с автоматическим обновлением статистики"""
        plan = super().update(instance, validated_data)
        plan.update_statistics()
        return plan


class TrialPlanSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения планов испытаний с новой структурой
    
    Возвращает структуру:
    {
        "id": 2,
        "year": 2026,
        "oblast": {
            "id": 2,
            "name": "Акмолинская область",
            "cultures": [...]
        }
    }
    """
    
    # Новая структура ответа (только для чтения)
    oblast = serializers.SerializerMethodField()
    cultures = serializers.SerializerMethodField()
    
    class Meta:
        model = TrialPlan
        fields = ['id', 'year', 'oblast', 'cultures']
    
    def get_oblast(self, obj):
        """Получить область"""
        return {
            'id': obj.oblast.id,
            'name': obj.oblast.name
        }
    
    def get_cultures(self, obj):
        """
        Получить культуры плана с типами испытаний и участниками
        
        Новая структура: TrialPlan → TrialPlanCulture → TrialPlanCultureTrialType → TrialPlanParticipant → TrialPlanTrial
        """
        from .models import TrialPlanCulture, TrialPlanCultureTrialType
        
        cultures = TrialPlanCulture.objects.filter(
            trial_plan=obj, 
            is_deleted=False
        ).order_by('culture__name').prefetch_related(
            'trial_types__participants__trials__region',
            'trial_types__trial_type',
            'trial_types__participants__application'
        )
        
        result = []
        for tc in cultures:
            # Получить типы испытаний для этой культуры
            trial_types = TrialPlanCultureTrialType.objects.filter(
                trial_plan_culture=tc,
                is_deleted=False
            ).order_by('trial_type__name')
            
            trial_types_list = []
            for tt in trial_types:
                # Получить участников этого типа испытания
                participants = tt.participants.filter(is_deleted=False).order_by('participant_number')
                
                participants_list = []
                for p in participants:
                    # Получить испытания участника
                    trials = p.trials.filter(is_deleted=False).select_related('region')
                    
                    participant_data = {
                        'id': p.id,
                        'participant_number': p.participant_number,
                        'maturity_group': p.maturity_group,
                        'statistical_group': p.statistical_group,
                        'seeds_provision': p.seeds_provision,
                        'patents_sort_id': p.patents_sort_id,
                        'application_id': p.application.id if p.application else None,
                        'application_submit_year': p.application.submission_date.year if p.application and p.application.submission_date else None,
                        'trials': [
                            {
                                'id': t.id,
                                'region_id': t.region.id,
                                'region_name': t.region.name,
                                'predecessor': t.predecessor,
                                'predecessor_culture_name': self._get_predecessor_culture_name(t.predecessor),
                                'seeding_rate': t.seeding_rate,
                                'season': t.season
                            }
                            for t in trials
                        ],
                        'created_by': p.created_by.id,
                        'created_at': p.created_at,
                        'updated_at': p.updated_at
                    }
                    participants_list.append(participant_data)
                
                trial_type_data = {
                    'id': tt.id,
                    'trial_type_id': tt.trial_type.id,
                    'trial_type_name': tt.trial_type.name,
                    'season': tt.season,
                    'participants': participants_list,
                    'created_by': tt.created_by.id,
                    'created_at': tt.created_at,
                    'updated_at': tt.updated_at
                }
                trial_types_list.append(trial_type_data)
            
            culture_data = {
                'id': tc.id,
                'culture': tc.culture.id,
                'culture_name': tc.culture.name,
                'culture_group': tc.culture.group_culture.name if tc.culture.group_culture else None,
                'trial_types': trial_types_list,
                'created_by': tc.created_by.id,
                'created_at': tc.created_at,
                'updated_at': tc.updated_at
            }
            result.append(culture_data)
        
        return result
    
    def _get_predecessor_culture_name(self, predecessor):
        """
        Получить название культуры предшественника, если predecessor содержит culture_id
        """
        if not predecessor:
            return None
        
        # Если predecessor это "fallow" или другие строковые значения
        if isinstance(predecessor, str):
            if predecessor == "fallow":
                return "Пар"
            # Проверяем, является ли строка числом (culture_id)
            try:
                culture_id = int(predecessor)
                # Получаем название культуры по ID
                from .models import Culture
                try:
                    culture = Culture.objects.get(id=culture_id, is_deleted=False)
                    return culture.name
                except Culture.DoesNotExist:
                    return None
            except ValueError:
                return predecessor  # Возвращаем как есть, если не число
        
        # Если predecessor это число (culture_id)
        if isinstance(predecessor, int):
            from .models import Culture
            try:
                culture = Culture.objects.get(id=predecessor, is_deleted=False)
                return culture.name
            except Culture.DoesNotExist:
                return None
        
        return None


class TrialPlanTrialSerializer(serializers.ModelSerializer):
    """Сериализатор для испытания в плане (только чтение)"""
    
    region_id = serializers.IntegerField(source='region.id', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    trial_type_id = serializers.IntegerField(source='trial_type.id', read_only=True, allow_null=True)
    trial_type_name = serializers.CharField(source='trial_type.name', read_only=True, allow_null=True)
    
    class Meta:
        model = TrialPlanTrial
        fields = ['region_id', 'region_name', 'predecessor', 'seeding_rate', 'season', 'trial_type_id', 'trial_type_name']


class TrialPlanTrialCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания испытания в плане"""
    
    region_id = serializers.IntegerField(write_only=True, help_text="ID региона")
    
    class Meta:
        model = TrialPlanTrial
        fields = ['region_id', 'predecessor', 'seeding_rate', 'season', 'trial_type']
        extra_kwargs = {
            'predecessor': {'required': True},
            'seeding_rate': {'required': True},
            'season': {'required': False},
            'trial_type': {'required': False}
        }
    
    def validate_region_id(self, value):
        """Валидация region_id"""
        from .models import Region
        try:
            Region.objects.get(id=value, is_deleted=False)
        except Region.DoesNotExist:
            raise serializers.ValidationError(f"Region with ID {value} not found")
        return value
    
    def validate_predecessor(self, value):
        """Валидация предшественника"""
        return validate_and_normalize_predecessor(value)
    
    def validate_seeding_rate(self, value):
        """Валидация нормы высева"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise serializers.ValidationError("seeding_rate must be a positive number")
        return value
    
    def validate_season(self, value):
        """Валидация сезона"""
        if value is not None:
            valid_seasons = ['spring', 'autumn', 'summer', 'winter']
            if value not in valid_seasons:
                raise serializers.ValidationError(f"season must be one of: {', '.join(valid_seasons)}")
        return value


class TrialPlanParticipantSerializer(serializers.ModelSerializer):
    """Сериализатор для участника плана"""
    
    trials = TrialPlanTrialSerializer(source='trials.all', many=True, read_only=True)
    application_id = serializers.IntegerField(source='application.id', read_only=True)
    application = serializers.IntegerField(write_only=True, required=False, help_text="ID заявки")
    
    class Meta:
        model = TrialPlanParticipant
        fields = [
            'id', 'patents_sort_id', 'statistical_group', 'seeds_provision', 
            'participant_number', 'maturity_group', 'application_id', 'application', 'trials'
        ]
    
    def validate_statistical_group(self, value):
        """Валидация статистической группы"""
        if value not in [0, 1]:
            raise serializers.ValidationError("statistical_group должен быть 0 (стандарт) или 1 (испытываемый)")
        return value
    
    def validate_seeds_provision(self, value):
        """Валидация обеспеченности семенами"""
        allowed_values = ['provided', 'not_provided']  # Соответствует модели TrialPlanParticipant
        if value not in allowed_values:
            raise serializers.ValidationError(f"seeds_provision must be one of: {', '.join(allowed_values)}")
        return value
    
    def validate_trials(self, value):
        """Валидация испытаний участника"""
        for trial in value:
            # Валидация предшественника - обязательное поле
            predecessor = trial.get('predecessor')
            # Используем вспомогательную функцию для валидации и нормализации
            trial['predecessor'] = validate_and_normalize_predecessor(predecessor)
            
            # Валидация нормы высева
            seeding_rate = trial.get('seeding_rate')
            if seeding_rate is not None:
                if not isinstance(seeding_rate, (int, float)) or seeding_rate <= 0:
                    raise serializers.ValidationError(
                        "seeding_rate must be a positive number"
                    )
            
            # Валидация сезона (опционально)
            season = trial.get('season')
            if season is not None:
                valid_seasons = ['spring', 'autumn', 'summer', 'winter']
                if season not in valid_seasons:
                    raise serializers.ValidationError(
                        f"season must be one of: {', '.join(valid_seasons)}"
                    )
            
            # Валидация trial_type (опционально)
            trial_type = trial.get('trial_type')
            if trial_type is not None:
                # Проверяем что trial_type существует
                try:
                    TrialType.objects.get(id=trial_type, is_deleted=False)
                except TrialType.DoesNotExist:
                    raise serializers.ValidationError(
                        f"trial_type with ID {trial_type} not found"
                    )
        
        return value


class TrialPlanParticipantCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания участника плана с trials"""
    
    trials = TrialPlanTrialCreateSerializer(many=True, required=False)
    application = serializers.IntegerField(write_only=True, required=False, help_text="ID заявки")
    
    class Meta:
        model = TrialPlanParticipant
        fields = [
            'patents_sort_id', 'statistical_group', 'seeds_provision', 
            'maturity_group', 'application', 'trials'
        ]
    
    def validate_statistical_group(self, value):
        """Валидация статистической группы"""
        if value not in [0, 1]:
            raise serializers.ValidationError("statistical_group должен быть 0 (стандарт) или 1 (испытываемый)")
        return value
    
    def validate_seeds_provision(self, value):
        """Валидация обеспеченности семенами"""
        allowed_values = ['provided', 'not_provided']  # Соответствует модели TrialPlanParticipant
        if value not in allowed_values:
            raise serializers.ValidationError(f"seeds_provision must be one of: {', '.join(allowed_values)}")
        return value
    
    def validate_trials(self, value):
        """Валидация испытаний участника"""
        for trial in value:
            # Валидация предшественника - обязательное поле
            predecessor = trial.get('predecessor')
            # Используем вспомогательную функцию для валидации и нормализации
            trial['predecessor'] = validate_and_normalize_predecessor(predecessor)
            
            # Валидация нормы высева
            seeding_rate = trial.get('seeding_rate')
            if seeding_rate is not None:
                if not isinstance(seeding_rate, (int, float)) or seeding_rate <= 0:
                    raise serializers.ValidationError(
                        "seeding_rate must be a positive number"
                    )
            
            # Валидация сезона (опционально)
            season = trial.get('season')
            if season is not None:
                valid_seasons = ['spring', 'autumn', 'summer', 'winter']
                if season not in valid_seasons:
                    raise serializers.ValidationError(
                        f"season must be one of: {', '.join(valid_seasons)}"
                    )
            
            # Валидация trial_type (опционально)
            trial_type = trial.get('trial_type')
            if trial_type is not None:
                # Проверяем что trial_type существует
                try:
                    TrialType.objects.get(id=trial_type, is_deleted=False)
                except TrialType.DoesNotExist:
                    raise serializers.ValidationError(
                        f"trial_type with ID {trial_type} not found"
                    )
        
        return value


class TrialPlanAddParticipantsSerializer(serializers.Serializer):
    """Сериализатор для добавления участников в план"""
    
    participants = TrialPlanParticipantCreateSerializer(many=True)
    
    def validate_participants(self, value):
        """Валидация участников"""
        if not value:
            raise serializers.ValidationError("Список участников не может быть пустым")
        
        return value


class TrialPlanCultureSerializer(serializers.ModelSerializer):
    """Сериализатор для связи плана с культурой"""
    
    culture_name = serializers.CharField(source='culture.name', read_only=True)
    culture_group = serializers.CharField(source='culture.group_culture.name', read_only=True)
    
    class Meta:
        model = TrialPlanCulture
        fields = [
            'id', 'culture', 'culture_name', 'culture_group', 
            'created_by', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'created_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class TrialPlanAddCultureSerializer(serializers.Serializer):
    """
    Сериализатор для добавления культуры в план
    
    Принимает либо culture_id (локальный ID), либо patents_culture_id (ID из Patents Service)
    """
    
    culture_id = serializers.IntegerField(
        required=False,
        help_text="ID культуры в Trials Service (локальный ID)"
    )
    patents_culture_id = serializers.IntegerField(
        required=False,
        help_text="ID культуры в Patents Service"
    )
    
    def validate(self, data):
        """Валидация: должен быть указан либо culture_id, либо patents_culture_id"""
        culture_id = data.get('culture_id')
        patents_culture_id = data.get('patents_culture_id')
        
        if not culture_id and not patents_culture_id:
            raise serializers.ValidationError(
                "Необходимо указать либо culture_id, либо patents_culture_id"
            )
        
        if culture_id and patents_culture_id:
            raise serializers.ValidationError(
                "Укажите только один параметр: culture_id или patents_culture_id"
            )
        
        # Если передан patents_culture_id, найти соответствующую локальную культуру
        if patents_culture_id:
            try:
                culture = Culture.objects.get(
                    culture_id=patents_culture_id,
                    is_deleted=False
                )
                # Заменяем patents_culture_id на culture_id для дальнейшей обработки
                data['culture_id'] = culture.id
                data.pop('patents_culture_id', None)
            except Culture.DoesNotExist:
                raise serializers.ValidationError({
                    'patents_culture_id': f'Культура с Patents ID {patents_culture_id} не найдена в локальной базе. '
                                         f'Возможно, нужно синхронизировать культуры.'
                })
        
        # Проверить что culture_id существует
        if culture_id:
            try:
                Culture.objects.get(id=culture_id, is_deleted=False)
            except Culture.DoesNotExist:
                raise serializers.ValidationError({
                    'culture_id': f'Культура с ID {culture_id} не найдена'
                })
        
        return data
