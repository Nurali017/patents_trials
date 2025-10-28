from django.db import models
from django.contrib.auth.models import User
from .base import SoftDeleteModel


class RegisterCategory(SoftDeleteModel):
    """
    Справочник категорий сортов (A-коды)
    A01 - простой гибрид, A02 - сложный гибрид, A17 - сорт и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код категории (A01, A02, A17 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название категории"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание категории"
    )
    
    class Meta:
        verbose_name = "Категория реестра"
        verbose_name_plural = "Категории реестра"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterUsage(SoftDeleteModel):
    """
    Справочник направлений использования (B-коды)
    B01 - амилозный, B02 - ароматичный, B80 - вина и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код направления (B01, B02, B80 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название направления использования"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание направления"
    )
    
    class Meta:
        verbose_name = "Направление использования"
        verbose_name_plural = "Направления использования"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterPeriod(SoftDeleteModel):
    """
    Справочник периодов потребления (C-коды)
    C01 - зимний, C02 - осенний, C12 - зимнее хранение и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код периода (C01, C02, C12 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название периода потребления"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание периода"
    )
    
    class Meta:
        verbose_name = "Период потребления"
        verbose_name_plural = "Периоды потребления"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterPlantType(SoftDeleteModel):
    """
    Справочник типов растения (E-коды)
    E01 - 00 типа, E02 - детерминантный, E61 - вьющийся и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код типа (E01, E02, E61 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название типа растения"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание типа"
    )
    
    class Meta:
        verbose_name = "Тип растения"
        verbose_name_plural = "Типы растений"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterGrowingCondition(SoftDeleteModel):
    """
    Справочник условий выращивания (F-коды)
    F01 - защищенный грунт, F14 - открытый грунт, F19 - орошение и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код условия (F01, F14, F19 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название условия выращивания"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание условия"
    )
    
    class Meta:
        verbose_name = "Условие выращивания"
        verbose_name_plural = "Условия выращивания"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterForm(SoftDeleteModel):
    """
    Справочник форм (G-коды)
    G01 - веретеновидная, G02 - кубовидная, G32 - удлиненно-кубовидная и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код формы (G01, G02, G32 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название формы"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание формы"
    )
    
    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterPestResistance(SoftDeleteModel):
    """
    Справочник устойчивости к вредителям (H-коды)
    H01 - нематодоустойчивый, H02 - устойчив к золотистой картофельной нематоде и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код устойчивости (H01, H02, H03 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название устойчивости к вредителям"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание устойчивости"
    )
    
    class Meta:
        verbose_name = "Устойчивость к вредителям"
        verbose_name_plural = "Устойчивость к вредителям"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class RegisterDiseaseResistance(SoftDeleteModel):
    """
    Справочник устойчивости к болезням (I-коды)
    I01 - устойчивость к ризомании, I02 - устойчив к раку и т.д.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Код устойчивости (I01, I02, I03 и т.д.)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название устойчивости к болезням"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание устойчивости"
    )
    
    class Meta:
        verbose_name = "Устойчивость к болезням"
        verbose_name_plural = "Устойчивость к болезням"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class SortRegisterData(SoftDeleteModel):
    """
    Дополнительные данные реестра для сорта
    
    Отдельная таблица для хранения характеристик реестра (A-I коды)
    без влияния на синхронизацию с Patents Service
    """
    sort_record = models.OneToOneField(
        'trials_app.SortRecord',
        on_delete=models.CASCADE,
        related_name='register_data',
        help_text="Сорт, для которого хранятся данные реестра"
    )
    
    # Характеристики реестра (A-I коды)
    category = models.ForeignKey(
        RegisterCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Категория сорта (A-код)"
    )
    usage_directions = models.ManyToManyField(
        RegisterUsage,
        blank=True,
        help_text="Направления использования (B-коды)"
    )
    consumption_periods = models.ManyToManyField(
        RegisterPeriod,
        blank=True,
        help_text="Периоды потребления (C-коды)"
    )
    plant_types = models.ManyToManyField(
        RegisterPlantType,
        blank=True,
        help_text="Типы растения (E-коды)"
    )
    growing_conditions = models.ManyToManyField(
        RegisterGrowingCondition,
        blank=True,
        help_text="Условия выращивания (F-коды)"
    )
    forms = models.ManyToManyField(
        RegisterForm,
        blank=True,
        help_text="Формы (G-коды)"
    )
    pest_resistance = models.ManyToManyField(
        RegisterPestResistance,
        blank=True,
        help_text="Устойчивость к вредителям (H-коды)"
    )
    disease_resistance = models.ManyToManyField(
        RegisterDiseaseResistance,
        blank=True,
        help_text="Устойчивость к болезням (I-коды)"
    )
    
    # Метаданные реестра
    is_in_register = models.BooleanField(
        default=False,
        help_text="Включен ли сорт в реестр"
    )
    register_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата включения в реестр"
    )
    register_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Номер в реестре"
    )
    notes = models.TextField(
        blank=True,
        help_text="Дополнительные примечания по реестру"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='register_data_created',
        help_text="Кто создал запись реестра"
    )
    
    class Meta:
        verbose_name = "Данные реестра сорта"
        verbose_name_plural = "Данные реестра сортов"
        ordering = ['-created_at']
    
    def __str__(self):
        sort_name = self.sort_record.name if self.sort_record else "Неизвестный сорт"
        status = "В реестре" if self.is_in_register else "Не в реестре"
        return f"{sort_name} - {status}"
    
    def get_usage_directions_display(self):
        """Получить строку с направлениями использования"""
        return ", ".join([f"{u.code} - {u.name}" for u in self.usage_directions.all()])
    
    def get_consumption_periods_display(self):
        """Получить строку с периодами потребления"""
        return ", ".join([f"{p.code} - {p.name}" for p in self.consumption_periods.all()])
    
    def get_plant_types_display(self):
        """Получить строку с типами растения"""
        return ", ".join([f"{t.code} - {t.name}" for t in self.plant_types.all()])
    
    def get_growing_conditions_display(self):
        """Получить строку с условиями выращивания"""
        return ", ".join([f"{c.code} - {c.name}" for c in self.growing_conditions.all()])
    
    def get_forms_display(self):
        """Получить строку с формами"""
        return ", ".join([f"{f.code} - {f.name}" for f in self.forms.all()])
    
    def get_pest_resistance_display(self):
        """Получить строку с устойчивостью к вредителям"""
        return ", ".join([f"{p.code} - {p.name}" for p in self.pest_resistance.all()])
    
    def get_disease_resistance_display(self):
        """Получить строку с устойчивостью к болезням"""
        return ", ".join([f"{d.code} - {d.name}" for d in self.disease_resistance.all()])
