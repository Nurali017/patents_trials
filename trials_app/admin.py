from django.contrib import admin
from .models import (
    Oblast, Region, ClimateZone, Indicator, GroupCulture, Culture, Originator, SortOriginator, SortRecord, 
    Application, PlannedDistribution, TrialType, Trial, TrialParticipant, TrialResult, 
    TrialLaboratoryResult, Document, AnnualDecisionTable, AnnualDecisionItem
)

@admin.register(Oblast)
class OblastAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at', 'is_deleted']
    search_fields = ['name', 'code']
    list_filter = ['created_at', 'is_deleted']

@admin.register(ClimateZone)
class ClimateZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at', 'is_deleted']
    search_fields = ['name', 'code', 'description']
    list_filter = ['created_at', 'is_deleted']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'oblast', 'climate_zone', 'address', 'created_at', 'is_deleted']
    search_fields = ['name', 'oblast__name', 'climate_zone__name', 'address']
    list_filter = ['oblast', 'climate_zone', 'created_at', 'is_deleted']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'oblast', 'climate_zone')
        }),
        ('Адрес', {
            'fields': ('address',)
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'category', 'is_quality', 'is_universal', 'created_at', 'is_deleted']
    search_fields = ['name', 'code', 'description']
    list_filter = ['category', 'is_quality', 'is_universal', 'created_at', 'is_deleted']
    filter_horizontal = ['group_cultures']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'name', 'unit', 'description', 'is_numeric')
        }),
        ('Категоризация', {
            'fields': ('category', 'is_quality', 'sort_order')
        }),
        ('Применимость', {
            'fields': ('is_universal', 'group_cultures'),
            'description': 'Если показатель универсальный, он применим ко всем культурам. Иначе укажите группы культур.'
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TrialType)
class TrialTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'requires_area', 'requires_standard', 'sort_order', 'is_deleted']
    search_fields = ['name', 'code', 'name_full']
    list_filter = ['category', 'requires_area', 'requires_standard', 'is_deleted']
    list_editable = ['sort_order']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'name', 'name_full', 'category', 'description')
        }),
        ('Требования', {
            'fields': ('requires_area', 'requires_standard', 'default_area_ha')
        }),
        ('Отображение', {
            'fields': ('sort_order',)
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GroupCulture)
class GroupCultureAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'group_culture_id', 'synced_at', 'created_at', 'is_deleted']
    search_fields = ['name', 'description', 'code']
    list_filter = ['created_at', 'synced_at', 'is_deleted']
    readonly_fields = ['group_culture_id', 'synced_at']


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'group_culture', 'culture_id', 'synced_at', 'created_at', 'is_deleted']
    search_fields = ['name', 'code']
    list_filter = ['group_culture', 'created_at', 'synced_at', 'is_deleted']
    readonly_fields = ['culture_id', 'synced_at']
    actions = ['sync_with_patents']
    
    def sync_with_patents(self, request, queryset):
        """Синхронизировать выбранные культуры с Patents Service"""
        count = 0
        for culture in queryset:
            if culture.sync_from_patents():
                count += 1
        self.message_user(request, f'Синхронизировано {count} культур')
    sync_with_patents.short_description = "Синхронизировать с Patents Service"


@admin.register(Originator)
class OriginatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'originator_id', 'synced_at', 'created_at', 'is_deleted']
    search_fields = ['name']
    list_filter = ['created_at', 'synced_at', 'is_deleted']
    readonly_fields = ['originator_id', 'synced_at']
    actions = ['sync_with_patents']
    
    def sync_with_patents(self, request, queryset):
        """Синхронизировать выбранных оригинаторов с Patents Service"""
        count = 0
        for originator in queryset:
            if originator.sync_from_patents():
                count += 1
        self.message_user(request, f'Синхронизировано {count} оригинаторов')
    sync_with_patents.short_description = "Синхронизировать с Patents Service"


class SortOriginatorInline(admin.TabularInline):
    model = SortOriginator
    extra = 1
    fields = ['originator', 'percentage']


@admin.register(SortRecord)
class SortRecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'public_code', 'sort_id', 'patents_status', 'culture', 'lifestyle', 'synced_at', 'created_at']
    search_fields = ['name', 'public_code', 'applicant']
    list_filter = ['patents_status', 'culture', 'lifestyle', 'characteristic', 'development_cycle', 'patent_nis', 'created_at', 'synced_at', 'is_deleted']
    readonly_fields = ['sort_id', 'synced_at', 'created_at', 'updated_at']
    inlines = [SortOriginatorInline]
    actions = ['sync_with_patents']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('sort_id', 'name', 'public_code', 'patents_status')
        }),
        ('Характеристики', {
            'fields': ('lifestyle', 'characteristic', 'development_cycle')
        }),
        ('Культура', {
            'fields': ('culture',)
        }),
        ('Дополнительно', {
            'fields': ('applicant', 'patent_nis', 'note', 'trial_notes')
        }),
        ('Синхронизация', {
            'fields': ('synced_at',),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def sync_with_patents(self, request, queryset):
        """Синхронизировать выбранные сорта с Patents Service"""
        count = 0
        for sort_record in queryset:
            if sort_record.sync_from_patents():
                count += 1
        self.message_user(request, f'Синхронизировано {count} сортов')
    sync_with_patents.short_description = "Синхронизировать с Patents Service"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Админка для заявок на испытания"""
    list_display = ['application_number', 'sort_record', 'applicant', 'status', 'submission_date', 'created_at']
    search_fields = ['application_number', 'applicant', 'purpose']
    list_filter = ['status', 'submission_date', 'created_at', 'is_deleted']
    filter_horizontal = ['target_oblasts']
    date_hierarchy = 'submission_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('application_number', 'submission_date', 'status')
        }),
        ('Сорт', {
            'fields': ('sort_record',)
        }),
        ('Заявитель', {
            'fields': ('applicant', 'applicant_inn_bin', 'contact_person_name', 'contact_person_phone', 'contact_person_email', 'maturity_group', 'purpose')
        }),
        ('Целевые области', {
            'fields': ('target_oblasts',)
        }),
        ('Системные поля', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Запретить редактирование created_by для существующих объектов"""
        if obj:  # Редактирование
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields


@admin.register(PlannedDistribution)
class PlannedDistributionAdmin(admin.ModelAdmin):
    """Админка для плановых распределений заявок по ГСУ"""
    list_display = ['application', 'region', 'trial_type', 'planting_season', 'status', 'year_started', 'year_completed', 'created_at']
    search_fields = ['application__application_number', 'region__name', 'notes']
    list_filter = ['status', 'trial_type', 'region__oblast', 'planting_season', 'year_started', 'created_at', 'is_deleted']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('application', 'region', 'trial_type', 'planting_season')
        }),
        ('Статус и период', {
            'fields': ('status', 'year_started', 'year_completed')
        }),
        ('Дополнительно', {
            'fields': ('notes',)
        }),
        ('Системные поля', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Запретить редактирование created_by для существующих объектов"""
        if obj:  # Редактирование
            return self.readonly_fields
        return self.readonly_fields


@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'culture', 'trial_type', 'region', 'area_ha', 'status', 'laboratory_status', 'decision', 'harvest_date', 'responsible_person', 'start_date']
    search_fields = ['description', 'sort_records__name', 'region__name', 'laboratory_code']
    list_filter = ['status', 'laboratory_status', 'trial_type', 'planting_season', 'decision', 'region__oblast', 'culture', 'growing_conditions', 'start_date', 'created_at', 'is_deleted']
    filter_horizontal = ['sort_records', 'indicators']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('description', 'status', 'culture')
        }),
        ('Тип испытания и площадь', {
            'fields': ('trial_type', 'area_ha', 'planting_season')
        }),
        ('Регион и ответственный', {
            'fields': ('region', 'responsible_person')
        }),
        ('Агрономические параметры', {
            'fields': ('predecessor_culture', 'agro_background', 'growing_conditions', 'cultivation_technology', 'growing_method', 'harvest_timing', 'harvest_date', 'additional_info'),
            'classes': ('collapse',)
        }),
        ('Сорта и показатели', {
            'fields': ('sort_records', 'indicators'),
            'classes': ('collapse',)
        }),
        ('Лабораторные анализы', {
            'fields': ('laboratory_status', 'laboratory_code', 'laboratory_sent_date', 'laboratory_completed_date', 'laboratory_sample_weight', 'laboratory_sample_source', 'laboratory_notes'),
            'classes': ('collapse',),
            'description': 'Информация о лабораторных анализах качественных показателей'
        }),
        ('Даты', {
            'fields': ('start_date',)
        }),
        ('Решение', {
            'fields': ('decision', 'decision_justification', 'decision_recommendations', 'decision_date', 'decided_by'),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrialParticipant)
class TrialParticipantAdmin(admin.ModelAdmin):
    list_display = ['trial', 'participant_number', 'sort_record', 'statistical_group', 'statistical_result', 'application', 'created_at']
    search_fields = ['sort_record__name', 'application__application_number', 'trial__region__name']
    list_filter = ['statistical_group', 'statistical_result', 'trial__region', 'created_at', 'is_deleted']
    readonly_fields = ['statistical_result', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('trial', 'sort_record', 'participant_number')
        }),
        ('Группировка', {
            'fields': ('statistical_group', 'statistical_result', 'application')
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TrialResult)
class TrialResultAdmin(admin.ModelAdmin):
    list_display = ['participant', 'indicator', 'value', 'plot_1', 'plot_2', 'plot_3', 'plot_4', 'measurement_date', 'created_at']
    search_fields = ['participant__sort_record__name', 'indicator__name', 'participant__trial__region__name']
    list_filter = ['measurement_date', 'participant__trial__region', 'indicator', 'created_at', 'is_deleted']
    date_hierarchy = 'measurement_date'
    readonly_fields = ['value', 'trial', 'sort_record', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('participant', 'indicator', 'measurement_date')
        }),
        ('Данные по делянкам', {
            'fields': ('plot_1', 'plot_2', 'plot_3', 'plot_4', 'value'),
            'description': 'Если делянки заполнены, value рассчитывается автоматически'
        }),
        ('Текстовое значение', {
            'fields': ('text_value', 'notes'),
            'classes': ('collapse',)
        }),
        ('Обратная совместимость', {
            'fields': ('trial', 'sort_record'),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TrialLaboratoryResult)
class TrialLaboratoryResultAdmin(admin.ModelAdmin):
    """Админка для лабораторных результатов испытаний"""
    list_display = ['trial', 'indicator', 'participant', 'value', 'laboratory_code', 'analysis_date', 'created_at']
    search_fields = ['trial__region__name', 'indicator__name', 'laboratory_code', 'participant__sort_record__name']
    list_filter = ['analysis_date', 'indicator', 'trial__region__oblast', 'created_at', 'is_deleted']
    date_hierarchy = 'analysis_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('trial', 'indicator', 'participant')
        }),
        ('Значение', {
            'fields': ('value', 'text_value')
        }),
        ('Лабораторные данные', {
            'fields': ('laboratory_code', 'analysis_date', 'sample_weight_kg', 'notes')
        }),
        ('Системные поля', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Запретить редактирование created_by для существующих объектов"""
        if obj:  # Редактирование
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'application', 'trial', 'uploaded_by', 'uploaded_at', 'is_deleted']
    search_fields = ['title', 'description', 'application__application_number']
    list_filter = ['document_type', 'uploaded_at', 'is_deleted']
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'document_type', 'file', 'description')
        }),
        ('Связь (выберите одно)', {
            'fields': ('application', 'trial'),
            'description': 'Документ может быть привязан к заявке ИЛИ к испытанию'
        }),
        ('Системные поля', {
            'fields': ('uploaded_by', 'uploaded_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


class AnnualDecisionItemInline(admin.TabularInline):
    """Inline для элементов годовой таблицы"""
    model = AnnualDecisionItem
    extra = 0
    fields = ['row_number', 'sort_record', 'maturity_group', 'average_yield', 'decision', 'decision_date']
    readonly_fields = ['average_yield', 'decision_date']
    
    def has_add_permission(self, request, obj=None):
        """Запретить добавление через inline если таблица finalized"""
        if obj and obj.status == 'finalized':
            return False
        return super().has_add_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        """Запретить редактирование через inline если таблица finalized"""
        if obj and obj.status == 'finalized':
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """Запретить удаление через inline если таблица finalized"""
        if obj and obj.status == 'finalized':
            return False
        return super().has_delete_permission(request, obj)


@admin.register(AnnualDecisionTable)
class AnnualDecisionTableAdmin(admin.ModelAdmin):
    """Админка для годовых таблиц решений"""
    list_display = ['title', 'year', 'oblast', 'culture', 'status', 'items_display', 'progress_display', 'created_at']
    search_fields = ['title', 'oblast__name', 'culture__name']
    list_filter = ['year', 'oblast', 'culture', 'status', 'created_at', 'is_deleted']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'finalized_date', 'items_display', 'progress_display', 'statistics_display']
    inlines = [AnnualDecisionItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('year', 'oblast', 'culture', 'title')
        }),
        ('Статус', {
            'fields': ('status', 'finalized_date', 'finalized_by')
        }),
        ('Статистика', {
            'fields': ('items_display', 'progress_display', 'statistics_display'),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def items_display(self, obj):
        """Количество сортов"""
        count = obj.get_items_count()
        return f"{count} сортов"
    items_display.short_description = "Сортов в таблице"
    
    def progress_display(self, obj):
        """Прогресс принятия решений"""
        progress = obj.get_progress_percentage()
        decided = obj.get_decisions_count()
        total = obj.get_items_count()
        return f"{decided}/{total} ({progress}%)"
    progress_display.short_description = "Прогресс решений"
    
    def statistics_display(self, obj):
        """Статистика решений"""
        stats = obj.get_statistics()
        return f"✅ {stats['approved']} | ❌ {stats['removed']} | 🔄 {stats['continue']} | ⏳ {stats['pending']}"
    statistics_display.short_description = "Статистика"
    
    def get_readonly_fields(self, request, obj=None):
        """Запретить редактирование некоторых полей для finalized таблиц"""
        readonly = list(self.readonly_fields)
        if obj and obj.status == 'finalized':
            readonly.extend(['year', 'oblast', 'culture', 'status'])
        if obj:
            readonly.append('created_by')
        return readonly
    
    actions = ['finalize_tables']
    
    def finalize_tables(self, request, queryset):
        """Завершить выбранные таблицы"""
        count = 0
        errors = []
        for table in queryset:
            if table.status == 'finalized':
                errors.append(f'{table.title} - уже завершена')
                continue
            
            if not table.is_all_decisions_made():
                errors.append(f'{table.title} - не все решения приняты ({table.get_decisions_count()}/{table.get_items_count()})')
                continue
            
            table.status = 'finalized'
            table.finalized_by = request.user
            table.finalized_date = timezone.now().date()
            table.save()
            count += 1
        
        if count > 0:
            self.message_user(request, f'Завершено {count} таблиц')
        if errors:
            self.message_user(request, 'Ошибки: ' + '; '.join(errors), level='warning')
    
    finalize_tables.short_description = "Завершить таблицы"


@admin.register(AnnualDecisionItem)
class AnnualDecisionItemAdmin(admin.ModelAdmin):
    """Админка для элементов годовой таблицы"""
    list_display = ['row_number', 'sort_record', 'annual_table', 'maturity_group', 'years_tested', 'average_yield', 'decision', 'decision_date', 'decided_by']
    search_fields = ['sort_record__name', 'annual_table__title', 'decision_justification']
    list_filter = ['decision', 'years_tested', 'annual_table__oblast', 'annual_table__year', 'decision_date', 'is_deleted']
    date_hierarchy = 'decision_date'
    readonly_fields = ['yields_by_year', 'average_yield', 'deviation_from_standard', 'last_year_data', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('annual_table', 'row_number', 'sort_record', 'maturity_group')
        }),
        ('Данные испытаний', {
            'fields': ('years_tested', 'year_started', 'yields_by_year', 'average_yield', 'deviation_from_standard'),
            'classes': ('collapse',)
        }),
        ('Показатели качества', {
            'fields': ('last_year_data',),
            'classes': ('collapse',)
        }),
        ('Решение', {
            'fields': ('decision', 'decision_justification', 'decision_recommendations', 'recommended_zones')
        }),
        ('Продление испытаний', {
            'fields': ('continue_reason', 'continue_until_year'),
            'classes': ('collapse',)
        }),
        ('Снятие с испытаний', {
            'fields': ('removal_reason',),
            'classes': ('collapse',)
        }),
        ('Метаданные решения', {
            'fields': ('decision_date', 'decided_by')
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at', 'is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Запретить редактирование для finalized таблиц"""
        readonly = list(self.readonly_fields)
        if obj and obj.annual_table.status == 'finalized':
            readonly.extend(['decision', 'decision_justification', 'decision_recommendations', 'recommended_zones', 'continue_reason', 'continue_until_year', 'removal_reason'])
        return readonly
    
    actions = ['refresh_trial_data', 'reset_decisions']
    
    def refresh_trial_data(self, request, queryset):
        """Обновить данные из испытаний для выбранных элементов"""
        count = 0
        for item in queryset:
            if item.annual_table.status == 'finalized':
                continue
            item.aggregate_trial_data()
            count += 1
        self.message_user(request, f'Обновлено {count} элементов')
    refresh_trial_data.short_description = "Обновить данные из испытаний"
    
    def reset_decisions(self, request, queryset):
        """Сбросить решения для выбранных элементов"""
        count = 0
        for item in queryset:
            if item.annual_table.status == 'finalized':
                continue
            item.decision = 'pending'
            item.decision_date = None
            item.decided_by = None
            item.save()
            count += 1
        self.message_user(request, f'Сброшено {count} решений')
    reset_decisions.short_description = "Сбросить решения"
