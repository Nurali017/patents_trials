from django.contrib import admin
from .models import (
    Oblast, Region, ClimateZone, Indicator, GroupCulture, Culture, Originator, SortOriginator, SortRecord, 
    Application, ApplicationDecisionHistory, PlannedDistribution, TrialType, Trial, TrialParticipant, TrialResult, 
    TrialLaboratoryResult, Document,
    # Модели реестра
    RegisterCategory, RegisterUsage, RegisterPeriod, RegisterPlantType, RegisterGrowingCondition,
    RegisterForm, RegisterPestResistance, RegisterDiseaseResistance, SortRegisterData
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
    list_display = ['name', 'unit', 'category', 'is_quality', 'is_required', 'is_recommended', 'is_auto_calculated', 'created_at', 'is_deleted']
    search_fields = ['name', 'code', 'description']
    list_filter = ['category', 'is_quality', 'is_required', 'is_recommended', 'is_auto_calculated', 'created_at', 'is_deleted']
    filter_horizontal = ['group_cultures']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'name', 'unit', 'description', 'is_numeric')
        }),
        ('Категоризация', {
            'fields': ('category', 'is_quality', 'sort_order')
        }),
        ('Обязательность', {
            'fields': ('is_required', 'is_recommended'),
            'description': 'Обязательные показатели по методике и рекомендуемые дополнительные'
        }),
        ('Авторасчеты', {
            'fields': ('is_auto_calculated', 'calculation_formula'),
            'classes': ('collapse',),
            'description': 'Показатели, которые вычисляются автоматически на основе других данных'
        }),
        ('Валидация', {
            'fields': ('validation_rules',),
            'classes': ('collapse',),
            'description': 'Правила валидации значений показателя'
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
    list_filter = ['created_at', 'synced_at', 'is_deleted', 'regions']
    readonly_fields = ['group_culture_id', 'synced_at']
    filter_horizontal = ['regions']


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


@admin.register(ApplicationDecisionHistory)
class ApplicationDecisionHistoryAdmin(admin.ModelAdmin):
    """Админка для истории решений"""
    list_display = ['application', 'oblast', 'year', 'decision', 'decision_date', 'decided_by']
    list_filter = ['decision', 'year', 'decision_date']
    search_fields = ['application__application_number', 'oblast__name', 'decision_justification']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'decision_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('application', 'oblast', 'year', 'decision')
        }),
        ('Детали решения', {
            'fields': ('decision_date', 'decision_justification', 'decided_by')
        }),
        ('Данные испытаний', {
            'fields': ('average_yield', 'years_tested_total')
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Админка для заявок на испытания"""
    list_display = ['application_number', 'sort_record', 'applicant', 'status', 'submission_date', 'created_at']
    search_fields = ['application_number', 'applicant', 'purpose']
    list_filter = ['status', 'submission_date', 'created_at', 'is_deleted']
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
            'fields': ()  # target_oblasts теперь through поле
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
    list_display = ['__str__', 'culture', 'trial_type', 'region', 'area_ha', 'status', 'laboratory_status', 'harvest_date', 'responsible_person', 'start_date']
    search_fields = ['region__name']
    list_filter = ['status', 'laboratory_status', 'trial_type', 'planting_season', 'region__oblast', 'culture', 'growing_conditions', 'start_date', 'created_at', 'is_deleted']
    filter_horizontal = ['indicators']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('status', 'culture')
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
        ('Показатели', {
            'fields': ('indicators',),
            'classes': ('collapse',)
        }),
        ('Лабораторные анализы', {
            'fields': ('laboratory_status', 'laboratory_sent_date', 'laboratory_completed_date', 'laboratory_sample_weight', 'laboratory_sample_source', 'laboratory_notes'),
            'classes': ('collapse',),
            'description': 'Информация о лабораторных анализах качественных показателей'
        }),
        ('Даты', {
            'fields': ('start_date',)
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
    list_display = ['participant', 'indicator', 'value', 'measurement_date', 'created_at']
    search_fields = ['participant__sort_record__name', 'indicator__name', 'participant__trial__region__name']
    list_filter = ['measurement_date', 'participant__trial__region', 'indicator', 'created_at', 'is_deleted']
    date_hierarchy = 'measurement_date'
    readonly_fields = ['value', 'trial', 'sort_record', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('participant', 'indicator', 'measurement_date')
        }),
        ('Данные результатов', {
            'fields': ('value',),
            'description': 'Значение показателя'
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
    list_display = ['trial', 'indicator', 'participant', 'value', 'analysis_date', 'created_at']
    search_fields = ['trial__region__name', 'indicator__name', 'participant__sort_record__name']
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
            'fields': ('analysis_date', 'sample_weight_kg', 'notes')
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
