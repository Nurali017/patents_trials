from django.db import models
from django.contrib.auth.models import User

# Базовая модель с soft delete для независимого микросервиса
class SoftDeleteModel(models.Model):
    """Базовая модель с поддержкой мягкого удаления"""
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление"""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def hard_delete(self):
        """Полное удаление"""
        super().delete()

class Oblast(SoftDeleteModel):
    """Области"""
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ClimateZone(SoftDeleteModel):
    """Природно-климатические зоны"""
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Название природно-климатической зоны"
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Код зоны (например: forest-steppe)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Описание климатической зоны"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Природно-климатическая зона"
        verbose_name_plural = "Природно-климатические зоны"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Region(SoftDeleteModel):
    """
    Сортоиспытательные участки (ГСУ)
    
    Каждый участок относится к области и природно-климатической зоне
    """
    name = models.CharField(max_length=255)
    oblast = models.ForeignKey(
        Oblast, 
        on_delete=models.CASCADE, 
        related_name='regions',
        help_text="Область"
    )
    climate_zone = models.ForeignKey(
        ClimateZone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='regions',
        help_text="Природно-климатическая зона"
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Адрес сортоиспытательного участка"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Сортоучасток (ГСУ)"
        verbose_name_plural = "Сортоучастки (ГСУ)"
        ordering = ['oblast__name', 'name']
        unique_together = ['name', 'oblast']
    
    def __str__(self):
        return f"{self.name} ({self.oblast.name})"

class Indicator(SoftDeleteModel):
    """
    Показатели испытаний
    
    Показатели привязаны к культурам - от культуры зависит какие данные нужно собирать.
    Например:
    - Пшеница: урожайность, белок, клейковина, натура зерна
    - Картофель: урожайность, крахмалистость, размер клубней
    - Овощи: урожайность, товарность, лежкость
    
    Категории показателей:
    - common: Общие показатели (урожайность, устойчивость и т.д.)
    - quality: Показатели качества (белок, крахмал, витамины и т.д.)
    - specific: Специфические показатели для конкретных культур
    """
    CATEGORY_CHOICES = [
        ('common', 'Общий показатель'),
        ('quality', 'Показатель качества'),
        ('specific', 'Специфический показатель'),
    ]
    
    code = models.CharField(
        max_length=100,
        unique=True,
        help_text="Уникальный код показателя (например: yield, protein_content)"
    )
    name = models.CharField(max_length=255, help_text="Название показателя")
    unit = models.CharField(max_length=50, blank=True, null=True, help_text="Единица измерения")
    description = models.TextField(blank=True, null=True, help_text="Описание показателя")
    is_numeric = models.BooleanField(default=True, help_text="Числовой показатель?")
    
    # Категоризация
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='common',
        help_text="Категория показателя"
    )
    is_quality = models.BooleanField(
        default=False,
        help_text="Показатель качества (дополнительные показатели)"
    )
    
    # Порядок отображения
    sort_order = models.IntegerField(
        default=0,
        help_text="Порядок отображения в списках"
    )
    
    # Привязка к ГРУППАМ культур
    group_cultures = models.ManyToManyField(
        'GroupCulture',
        related_name='indicators',
        blank=True,
        help_text="Группы культур, для которых применим этот показатель"
    )
    
    # Для универсальных показателей (применимы ко всем культурам)
    is_universal = models.BooleanField(
        default=False,
        help_text="Универсальный показатель (применим ко всем культурам)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Показатель"
        verbose_name_plural = "Показатели"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name
    
    def is_applicable_for_culture(self, culture):
        """
        Проверить применимость показателя для культуры
        
        Проверяет через группу культуры (новая логика)
        """
        if self.is_universal:
            return True
        
        # Проверить через группу культуры
        if culture.group_culture:
            return self.group_cultures.filter(id=culture.group_culture.id).exists()
        
        return False
    
    def get_applicable_cultures(self):
        """
        Получить все культуры, для которых применим показатель
        
        Returns:
            QuerySet: Culture objects
        """
        if self.is_universal:
            return Culture.objects.filter(is_deleted=False)
        
        # Получить культуры через группы
        return Culture.objects.filter(
            group_culture__in=self.group_cultures.all(),
            is_deleted=False
        )

class GroupCulture(SoftDeleteModel):
    """
    Группы культур (Зерновые, Овощные и т.д.)
    
    Локальная копия данных из Patents Service для автономной работы
    """
    group_culture_id = models.IntegerField(
        help_text="ID группы культур в Patents Service",
        db_index=True,
        unique=True
    )
    name = models.CharField(
        max_length=128,
        help_text="Название группы культур"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание группы"
    )
    code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Код группы"
    )
    
    # Метаданные
    synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Группа культур"
        verbose_name_plural = "Группы культур"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def sync_from_patents(self):
        """Синхронизировать данные с Patents Service"""
        from .patents_integration import patents_api
        from django.utils import timezone
        
        # TODO: Добавить метод get_group_culture в patents_api
        # group_data = patents_api.get_group_culture(self.group_culture_id)
        # if group_data:
        #     self.name = group_data.get('name', self.name)
        #     self.description = group_data.get('description', '')
        #     self.code = group_data.get('code', '')
        #     self.synced_at = timezone.now()
        #     self.save()
        #     return True
        return False


class Culture(SoftDeleteModel):
    """
    Культуры растений (Пшеница яровая, Ячмень и т.д.)
    
    Локальная копия данных из Patents Service для автономной работы
    """
    culture_id = models.IntegerField(
        help_text="ID культуры в Patents Service",
        db_index=True,
        unique=True
    )
    name = models.CharField(
        max_length=128,
        help_text="Название культуры"
    )
    code = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Код культуры"
    )
    group_culture = models.ForeignKey(
        GroupCulture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cultures',
        help_text="Группа культур"
    )
    
    # Метаданные
    synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Культура"
        verbose_name_plural = "Культуры"
        ordering = ['group_culture__name', 'name']
    
    def __str__(self):
        if self.group_culture:
            return f"{self.group_culture.name} - {self.name}"
        return self.name
    
    def sync_from_patents(self):
        """Синхронизировать данные с Patents Service"""
        from .patents_integration import patents_api
        from django.utils import timezone
        
        culture_data = patents_api.get_culture(self.culture_id)
        if culture_data:
            self.name = culture_data.get('name', self.name)
            self.code = culture_data.get('code', '')
            
            # Группа культуры
            group_data = culture_data.get('group', {}) or culture_data.get('group_culture', {})
            if group_data and group_data.get('id'):
                group_culture, _ = GroupCulture.objects.update_or_create(
                    group_culture_id=group_data['id'],
                    defaults={
                        'name': group_data.get('name', ''),
                        'description': group_data.get('description', ''),
                        'code': group_data.get('code', '')
                    }
                )
                self.group_culture = group_culture
            
            self.synced_at = timezone.now()
            self.save()
            return True
        return False


class Originator(SoftDeleteModel):
    """
    Оригинаторы (создатели сортов)
    
    Локальная копия данных из Patents Service для автономной работы
    """
    originator_id = models.IntegerField(
        help_text="ID оригинатора в Patents Service",
        db_index=True,
        unique=True
    )
    name = models.CharField(
        max_length=512,
        help_text="Название оригинатора"
    )
    
    # Метаданные
    synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Оригинатор"
        verbose_name_plural = "Оригинаторы"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def sync_from_patents(self):
        """Синхронизировать данные с Patents Service"""
        from .patents_integration import patents_api
        from django.utils import timezone
        
        originator_data = patents_api.get_originator(self.originator_id)
        if originator_data:
            self.name = originator_data.get('name', self.name)
            self.synced_at = timezone.now()
            self.save()
            return True
        return False


class SortOriginator(models.Model):
    """
    Связь сорта с оригинаторами (с процентами вклада)
    
    Хранит кто и какой процент вклада внес в создание сорта
    """
    sort_record = models.ForeignKey(
        'SortRecord',
        on_delete=models.CASCADE,
        related_name='sort_originators'
    )
    originator = models.ForeignKey(
        Originator,
        on_delete=models.CASCADE,
        related_name='sort_originators'
    )
    percentage = models.PositiveIntegerField(
        default=100,
        help_text="Процент вклада оригинатора (сумма должна быть 100)"
    )
    
    class Meta:
        verbose_name = "Оригинатор сорта"
        verbose_name_plural = "Оригинаторы сортов"
        unique_together = ['sort_record', 'originator']
    
    def __str__(self):
        return f"{self.originator.name} - {self.percentage}%"


class SortRecord(SoftDeleteModel):
    """
    Локальная копия данных сорта из Patents Service
    
    ПРИНЦИП: Репликация данных для автономной работы
    
    Хранит ВСЕ основные поля сорта локально:
    - Основные данные (id, name, public_code, status)
    - Характеристики (lifestyle, characteristic, development_cycle)
    - Связь с культурой (culture_id, culture_name)
    - Дополнительные данные (applicant, patent_nis, note)
    
    Синхронизация с Patents Service:
    - При создании - получить данные из Patents API
    - При обновлении - обновить локальную копию
    - Периодическая синхронизация (опционально)
    """
    # === Основные данные сорта (из Patents Service) ===
    sort_id = models.IntegerField(
        help_text="ID сорта в Patents Service",
        db_index=True,
        unique=True
    )
    name = models.CharField(
        max_length=255,
        default='',
        help_text="Название сорта (заполняется при синхронизации)"
    )
    public_code = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Публичный код сорта"
    )
    
    # === Статус в Patents Service ===
    STATUS_CHOICES = [
        (1, 'MAIN - Основной реестр'),
        (2, 'TESTING - Испытания'),
        (3, 'ARCHIVE - Архив'),
    ]
    patents_status = models.IntegerField(
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="Статус сорта в Patents Service (1=MAIN, 2=TESTING, 3=ARCHIVE)"
    )
    
    # === Характеристики сорта ===
    LIFESTYLE_CHOICES = [
        (1, 'Яровой'),
        (2, 'Озимый'),
        (3, 'Дерево'),
        (4, 'Кустарник'),
        (5, 'Полукустарник'),
        (6, 'Трава'),
    ]
    lifestyle = models.IntegerField(
        choices=LIFESTYLE_CHOICES,
        null=True,
        blank=True,
        help_text="Жизненная форма"
    )
    
    CHARACTERISTIC_CHOICES = [
        (1, 'Сорт'),
        (2, 'Гибрид'),
        (3, 'Линия'),
        (4, 'Клон'),
    ]
    characteristic = models.IntegerField(
        choices=CHARACTERISTIC_CHOICES,
        null=True,
        blank=True,
        help_text="Характеристика"
    )
    
    DEVELOPMENT_CYCLE_CHOICES = [
        (1, 'Однолетний'),
        (2, 'Многолетний'),
    ]
    development_cycle = models.IntegerField(
        choices=DEVELOPMENT_CYCLE_CHOICES,
        null=True,
        blank=True,
        help_text="Цикл развития"
    )
    
    # === Связь с культурой (через локальную таблицу) ===
    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sort_records',
        help_text="Культура сорта"
    )
    
    # === Дополнительные данные ===
    applicant = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        default='',
        help_text="Заявитель"
    )
    patent_nis = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text="Патент НИИС"
    )
    note = models.TextField(
        blank=True,
        null=True,
        default='',
        help_text="Примечание из Patents Service"
    )
    
    # === Примечания специфичные для испытаний ===
    trial_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Примечания по сорту в контексте испытаний (локальные)"
    )
    
    # === Метаданные синхронизации ===
    synced_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Дата последней синхронизации с Patents Service"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Запись о сорте"
        verbose_name_plural = "Записи о сортах"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.public_code or f'ID:{self.sort_id}'})"
    
    def sync_from_patents(self, sync_originators=True):
        """
        Синхронизировать данные с Patents Service
        
        Args:
            sync_originators: Синхронизировать оригинаторов (default: True)
        
        Обновляет все поля из Patents API включая оригинаторов
        """
        from .patents_integration import patents_api
        from django.utils import timezone
        
        sort_data = patents_api.get_sort(self.sort_id)
        if not sort_data:
            return False
        
        # Основные данные
        self.name = sort_data.get('name', self.name)
        self.public_code = sort_data.get('code')  # API V2 использует 'code' вместо 'public_code'
        self.lifestyle = sort_data.get('lifestyle')
        self.characteristic = sort_data.get('characteristic')
        self.development_cycle = sort_data.get('development_cycle')
        self.applicant = sort_data.get('applicant', '')
        self.patent_nis = sort_data.get('patent_nis', False)
        self.note = sort_data.get('note', '')
        
        # Статус из Patents (1=MAIN, 2=TESTING, 3=ARCHIVE)
        self.patents_status = sort_data.get('status')
        
        # Культура - создать/обновить локальную запись
        culture_data = sort_data.get('culture', {})
        if culture_data and culture_data.get('id'):
            culture_obj, _ = Culture.objects.update_or_create(
                culture_id=culture_data['id'],
                defaults={
                    'name': culture_data.get('name', ''),
                    'code': culture_data.get('code', '')
                }
            )
            # Синхронизировать культуру с группой
            culture_obj.sync_from_patents()
            self.culture = culture_obj
        
        self.synced_at = timezone.now()
        self.save()
        
        # Синхронизация оригинаторов
        if sync_originators:
            self._sync_originators(sort_data.get('ariginators', []))
        
        return True
    
    def _sync_originators(self, originators_data):
        """
        Синхронизировать список оригинаторов
        
        Args:
            originators_data: список оригинаторов из Patents API
            
            Формат API:
            [{
                "id": 820,
                "ariginator": {
                    "id": 7769,
                    "name": "ТОО КазНИИЗиР"
                },
                "percentage": 100
            }]
        """
        # Удаляем старые связи
        SortOriginator.objects.filter(sort_record=self).delete()
        
        # Создаем новые
        for orig_data in originators_data:
            # Новая структура: вложенный объект 'ariginator'
            ariginator_obj = orig_data.get('ariginator') or orig_data.get('originator')
            
            if ariginator_obj:
                originator_id = ariginator_obj.get('id')
                originator_name = ariginator_obj.get('name')
            else:
                # Старая структура (на всякий случай)
                originator_id = orig_data.get('ariginator_id') or orig_data.get('originator_id')
                originator_name = orig_data.get('ariginator_name') or orig_data.get('name')
            
            percentage = orig_data.get('percentage', 100)
            
            if originator_id and originator_name:
                # Создать или обновить оригинатора
                originator, _ = Originator.objects.update_or_create(
                    originator_id=originator_id,
                    defaults={'name': originator_name}
                )
                
                # Создать связь
                SortOriginator.objects.create(
                    sort_record=self,
                    originator=originator,
                    percentage=percentage
                )


class Application(SoftDeleteModel):
    """
    Заявка на сортоиспытание
    
    Одна заявка может иметь несколько испытаний в разных областях.
    Управляет полным жизненным циклом от подачи до включения в реестр.
    """
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Подана'),
        ('distributed', 'Распределена по областям'),
        ('in_progress', 'Испытания проводятся'),
        ('completed', 'Испытания завершены'),
        ('registered', 'Включен в реестр'),
        ('rejected', 'Отклонен'),
    ]
    
    # Группы спелости D-коды
    MATURITY_GROUP_CHOICES = [
        ('D01', 'D01'),
        ('D02', 'D02'),
        ('D03', 'D03'),
        ('D04', 'D04'),
        ('D05', 'D05'),
        ('D06', 'D06'),
        ('D07', 'D07'),
        ('D08', 'D08'),
        ('D09', 'D09'),
        ('D10', 'D10'),
    ]
    
    application_number = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Уникальный номер заявки (например, APP-2025-001)"
    )
    submission_date = models.DateField(
        help_text="Дата подачи заявки"
    )
    sort_record = models.ForeignKey(
        SortRecord, 
        on_delete=models.CASCADE, 
        related_name='applications',
        help_text="Сорт, который испытывается"
    )
    
    # === Информация о заявителе ===
    applicant = models.CharField(
        max_length=512,
        help_text="Организация-заявитель"
    )
    applicant_inn_bin = models.CharField(
        max_length=12,
        help_text="ИНН/БИН заявителя (12 цифр)",
        blank=True,
        null=True
    )
    
    # === Контактное лицо ===
    contact_person_name = models.CharField(
        max_length=255,
        help_text="ФИО контактного лица",
        blank=True,
        null=True
    )
    contact_person_phone = models.CharField(
        max_length=50,
        help_text="Телефон контактного лица",
        blank=True,
        null=True
    )
    contact_person_email = models.CharField(
        max_length=255,
        help_text="Email контактного лица",
        blank=True,
        null=True
    )
    
    # === Характеристики сорта ===
    maturity_group = models.CharField(
        max_length=3,
        choices=MATURITY_GROUP_CHOICES,
        help_text="Группа спелости D-коды (D01-D10)",
        blank=True,
        null=True
    )
    
    purpose = models.TextField(
        help_text="Цель испытаний",
        blank=True,
        null=True
    )
    
    # Целевые области для испытаний
    target_oblasts = models.ManyToManyField(
        Oblast,
        related_name='applications',
        help_text="Целевые области для проведения испытаний"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='created_applications'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Заявка на испытание"
        verbose_name_plural = "Заявки на испытания"
        ordering = ['-submission_date', '-created_at']
    
    def __str__(self):
        return f"{self.application_number} - {self.sort_record.name}"
    
    def get_missing_mandatory_documents(self):
        """
        Проверить наличие обязательных документов и вернуть список отсутствующих
        
        Returns:
            list: Список типов отсутствующих обязательных документов
        """
        # Базовые обязательные документы
        mandatory_docs = [
            'application_for_testing',
            'breeding_questionnaire',
            'variety_description',
            'plant_photo_with_ruler',
        ]
        
        # Дополнительные документы (условно обязательные)
        # TODO: Добавить логику определения когда нужны эти документы
        # - right_to_submit - если заявитель посредник/правопреемник
        # - gmo_free - если сорт иностранной селекции
        
        uploaded_docs = self.documents.filter(is_deleted=False).values_list('document_type', flat=True)
        missing_docs = [doc for doc in mandatory_docs if doc not in uploaded_docs]
        
        return missing_docs
    
    def is_ready_for_submission(self):
        """
        Проверить готовность заявки к подаче
        
        Returns:
            bool: True если все обязательные документы загружены
        """
        return len(self.get_missing_mandatory_documents()) == 0


class PlannedDistribution(SoftDeleteModel):
    """
    Плановое распределение заявки по ГСУ
    
    Создается при распределении заявки (distribute).
    На основе записи позже создается Trial вручную сортопытом.
    
    STATUS LIFECYCLE:
    1. planned → Trial еще не создан
    2. trial_created → Trial создан и идет (active/completed/lab_*)
    3. trial_completed → Trial полностью завершен (approved/continue/rejected)
    4. cancelled → Испытание отменено
    """
    application = models.ForeignKey(
        'Application',
        on_delete=models.CASCADE,
        related_name='planned_distributions_records',
        help_text="Заявка"
    )
    region = models.ForeignKey(
        'Region',
        on_delete=models.PROTECT,
        related_name='planned_distributions',
        help_text="ГСУ для проведения испытания"
    )
    trial_type = models.ForeignKey(
        'TrialType',
        on_delete=models.PROTECT,
        related_name='planned_distributions',
        null=True,
        blank=True,
        help_text="Тип испытания"
    )
    planting_season = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Сезон посадки (spring/autumn/summer)"
    )
    
    # Статус распределения (многолетние испытания)
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('in_progress', 'Испытания идут'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        help_text="Статус распределения"
    )
    
    # Годы испытаний (для многолетних испытаний)
    year_started = models.IntegerField(
        null=True,
        blank=True,
        help_text="Год начала испытаний"
    )
    year_completed = models.IntegerField(
        null=True,
        blank=True,
        help_text="Год завершения испытаний (если завершено)"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_distributions',
        help_text="Кто создал распределение"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Примечания
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Дополнительные заметки"
    )
    
    class Meta:
        verbose_name = "Плановое распределение"
        verbose_name_plural = "Плановые распределения"
        ordering = ['-created_at']
        # Уникальность: одна заявка не может быть распределена в один регион дважды
        unique_together = [['application', 'region']]
    
    def __str__(self):
        return f"{self.application.application_number} → {self.region.name}"
    
    def get_trials(self):
        """
        Получить все Trial для этого PlannedDistribution
        
        Returns:
            QuerySet: Все Trial для данной заявки в данном регионе
        """
        from trials_app.models import Trial
        return Trial.objects.filter(
            region=self.region,
            participants__application=self.application,
            is_deleted=False
        ).distinct().order_by('start_date')
    
    def get_latest_trial(self):
        """Получить последний Trial"""
        return self.get_trials().last()
    
    def get_latest_decision(self):
        """Получить последнее решение"""
        latest = self.get_latest_trial()
        return latest.decision if latest else None
    
    def get_years_count(self):
        """Количество лет испытаний"""
        trials = self.get_trials()
        if not trials.exists():
            return 0
        years = set()
        for trial in trials:
            if trial.year:
                years.add(trial.year)
            elif trial.start_date:
                years.add(trial.start_date.year)
        return len(years)


class TrialType(SoftDeleteModel):
    """
    Типы испытаний (КСИ, ООС, ДЮС-ТЕСТ и т.д.)
    
    Справочник видов сортоиспытаний согласно методике.
    Используется для планирования и статистики.
    """
    CATEGORY_CHOICES = [
        ('mandatory', 'Обязательное'),
        ('additional', 'Дополнительное'),
        ('special', 'Специальное'),
        ('reproduction', 'Размножение'),
        ('demonstration', 'Демонстрационное'),
    ]
    
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Код типа испытания (например: competitive, oos, dus)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Название типа испытания"
    )
    name_full = models.CharField(
        max_length=512,
        blank=True,
        help_text="Полное название с расшифровкой"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='mandatory',
        help_text="Категория испытания"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Описание и методика"
    )
    
    # Требования
    requires_area = models.BooleanField(
        default=True,
        help_text="Требуется указание площади"
    )
    requires_standard = models.BooleanField(
        default=True,
        help_text="Требуется стандартный сорт для сравнения"
    )
    default_area_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Рекомендуемая площадь, га"
    )
    
    # Порядок отображения
    sort_order = models.IntegerField(
        default=0,
        help_text="Порядок в списках"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Тип испытания"
        verbose_name_plural = "Типы испытаний"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Trial(SoftDeleteModel):
    """
    Испытание сорта на конкретном участке
    
    Каждое испытание независимо и имеет свое решение.
    Сорта добавляются через связь sort_records.
    
    ЖИЗНЕННЫЙ ЦИКЛ:
    1. planned → Испытание запланировано, но еще не начато
    2. active → Испытание активно проводится, выполняются полевые работы
    3. completed_008 → Полевые испытания завершены, данные уборки внесены в Форму 008
    4. lab_sample_sent → Образцы отправлены в лабораторию для анализа
    5. lab_completed → Лабораторные анализы завершены
    6. completed → Испытание полностью завершено, все данные собраны и обработаны
    7. approved/continue/rejected → Решение комиссии
    """
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('active', 'Проводится'),
        ('completed_008', 'Уборка завершена'),
        ('lab_sample_sent', 'Образец в лаборатории'),
        ('lab_completed', 'Лабораторный анализ завершен'),
        ('completed', 'Завершено'),
    ]
    
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='trials')
    
    # Тип и площадь испытания
    trial_type = models.ForeignKey(
        TrialType,
        on_delete=models.PROTECT,
        related_name='trials',
        null=True,
        blank=True,
        help_text="Тип испытания (КСИ, ООС, ДЮС и т.д.)"
    )
    area_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Площадь испытания, га"
    )
    planting_season = models.CharField(
        max_length=20,
        choices=[('spring', 'Весна'), ('autumn', 'Осень')],
        default='spring',
        help_text="Сезон посева"
    )
    
    # === Культура испытания ===
    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trials',
        help_text="Культура, которая испытывается"
    )
    
    # === Агрономические параметры ===
    
    # Предшественник
    predecessor_culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trials_as_predecessor',
        help_text="Предшествующая культура"
    )
    
    # Агрономический фон
    AGRO_BACKGROUND_CHOICES = [
        ('favorable', 'Благоприятный'),
        ('moderate', 'Умеренный'),
        ('unfavorable', 'Неблагоприятный'),
    ]
    agro_background = models.CharField(
        max_length=20,
        choices=AGRO_BACKGROUND_CHOICES,
        null=True,
        blank=True,
        help_text="Агрономический фон"
    )
    
    # Условия выращивания
    GROWING_CONDITIONS_CHOICES = [
        ('rainfed', 'Богара'),
        ('irrigated', 'Орошение'),
        ('mixed', 'Смешанное'),
    ]
    growing_conditions = models.CharField(
        max_length=20,
        choices=GROWING_CONDITIONS_CHOICES,
        null=True,
        blank=True,
        help_text="Условия выращивания"
    )
    
    # Технология возделывания
    CULTIVATION_TECHNOLOGY_CHOICES = [
        ('traditional', 'Обычная'),
        ('minimal', 'Минимальная обработка'),
        ('no_till', 'No-till (нулевая)'),
        ('organic', 'Органическая'),
    ]
    cultivation_technology = models.CharField(
        max_length=20,
        choices=CULTIVATION_TECHNOLOGY_CHOICES,
        null=True,
        blank=True,
        help_text="Технология возделывания"
    )
    
    # Способ выращивания
    GROWING_METHOD_CHOICES = [
        ('soil_traditional', 'Традиционное в почве'),
        ('hydroponics', 'Гидропоника'),
        ('greenhouse', 'Защищенный грунт'),
        ('raised_beds', 'Приподнятые грядки'),
        ('containers', 'Контейнерное'),
    ]
    growing_method = models.CharField(
        max_length=20,
        choices=GROWING_METHOD_CHOICES,
        null=True,
        blank=True,
        help_text="Способ выращивания"
    )
    
    # Сроки уборки
    HARVEST_TIMING_CHOICES = [
        ('very_early', 'Очень ранняя'),
        ('early', 'Ранняя'),
        ('medium_early', 'Среднеранняя'),
        ('medium', 'Средняя'),
        ('medium_late', 'Среднепоздняя'),
        ('late', 'Поздняя'),
        ('very_late', 'Очень поздняя'),
    ]
    harvest_timing = models.CharField(
        max_length=20,
        choices=HARVEST_TIMING_CHOICES,
        null=True,
        blank=True,
        help_text="Сроки уборки"
    )
    
    harvest_date = models.DateField(
        null=True,
        blank=True,
        help_text="Конкретная дата уборки"
    )
    
    # Дополнительная информация
    additional_info = models.TextField(
        blank=True,
        null=True,
        help_text="Дополнительные примечания"
    )
    
    
    indicators = models.ManyToManyField(Indicator, related_name='trials')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    start_date = models.DateField()
    
    # Год испытания (для многолетних испытаний)
    year = models.IntegerField(
        null=True,
        blank=True,
        help_text="Год проведения испытания (автоматически из start_date если не указан)"
    )
    
    responsible_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ФИО ответственного сортопыта"
    )
    
    
    # === Лабораторные анализы ===
    laboratory_status = models.CharField(
        max_length=20,
        choices=[
            ('not_required', 'Не требуется'),
            ('pending', 'Ожидается'),
            ('sent', 'Отправлено в лабораторию'),
            ('completed', 'Анализы завершены'),
        ],
        null=True,
        blank=True,
        help_text="Статус лабораторных анализов"
    )
    laboratory_sent_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата отправки образца в лабораторию"
    )
    laboratory_completed_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата завершения лабораторных анализов"
    )
    laboratory_sample_weight = models.FloatField(
        null=True,
        blank=True,
        help_text="Вес отправленного образца, кг"
    )
    laboratory_sample_source = models.TextField(
        blank=True,
        null=True,
        help_text="Источник образца (из какой делянки, какого участника)"
    )
    laboratory_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Дополнительные примечания по лабораторным анализам"
    )
    
    # Связь с планом испытаний
    trial_plan = models.ForeignKey(
        'TrialPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trials',
        help_text="План, из которого создано испытание"
    )
    
    # Метаданные
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_trials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Испытание"
        verbose_name_plural = "Испытания"
        ordering = ['-created_at']
    
    def __str__(self):
        sort_record = self.get_sort_record()
        sort_name = sort_record.name if sort_record else "Без сорта"
        year = self.year or (self.start_date.year if self.start_date else "???")
        return f"{sort_name} - {self.region.name} ({year})"
    
    def save(self, *args, **kwargs):
        """Автоматически устанавливаем year из start_date если не указан"""
        if not self.year and self.start_date:
            self.year = self.start_date.year
        super().save(*args, **kwargs)
    
    def get_sort_record(self):
        """Получить сорт (через participants)"""
        first_participant = self.participants.first()
        return first_participant.sort_record if first_participant else None
    
    def get_standard_participants(self):
        """Получить стандартные сорта в опыте"""
        return self.participants.filter(statistical_group=0)
    
    def get_tested_participants(self):
        """Получить испытываемые сорта"""
        return self.participants.filter(statistical_group=1)
    
    def calculate_trial_statistics(self):
        """
        Рассчитать статистику опыта (Sx, P%, НСР, E)
        
        Returns:
            dict: {
                'sx': float,              # Стандартное отклонение
                'accuracy_percent': float, # Точность опыта (P%)
                'lsd': float,             # НСР
                'error_mean': float       # Ошибка средней (E)
            }
        """
        import math
        from django.db.models import Avg, StdDev
        
        # Найти стандарт(ы)
        standards = self.get_standard_participants()
        if not standards.exists():
            return None
        
        # Берем первый стандарт для расчета (или можно усреднять по всем)
        standard = standards.first()
        
        # Получить урожайность стандарта (показатель с кодом 'yield')
        try:
            from trials_app.models import Indicator
            yield_indicator = Indicator.objects.get(code='yield')
        except:
            return None
        
        # Получить результаты стандарта
        results = TrialResult.objects.filter(
            participant=standard,
            indicator=yield_indicator
        ).first()
        
        if not results:
            return None
        
        # Используем только итоговое значение
        if results.value is None:
            return None
        
        # Для упрощенной статистики используем только value
        # В реальной системе статистика рассчитывается по множественным испытаниям
        mean = results.value
        
        # Упрощенные значения (требуют доработки для реальной статистики)
        sx = 0  # Стандартное отклонение - требует множественных измерений
        accuracy = 0  # Точность опыта - требует множественных измерений
        lsd = 0  # НСР - требует множественных измерений
        error_mean = 0  # Ошибка средней - требует множественных измерений
        
        return {
            'sx': round(sx, 2),
            'accuracy_percent': round(accuracy, 1),
            'lsd': round(lsd, 2),
            'error_mean': round(error_mean, 1)
        }
    
    def get_completion_status(self):
        """
        Проверить заполненность данных
        
        Returns:
            dict: {
                'is_complete': bool,
                'filled_percent': float,
                'missing_data': list
            }
        """
        participants_count = self.participants.count()
        indicators_count = self.indicators.count()
        
        if participants_count == 0 or indicators_count == 0:
            return {
                'is_complete': False,
                'filled_percent': 0,
                'missing_data': ['Нет участников или показателей']
            }
        
        total_required = participants_count * indicators_count
        filled = 0
        missing = []
        
        for participant in self.participants.all():
            for indicator in self.indicators.all():
                # Проверяем наличие результата
                has_result = TrialResult.objects.filter(
                    participant=participant,
                    indicator=indicator,
                    value__isnull=False
                ).exists()
                
                if has_result:
                    filled += 1
                else:
                    missing.append(
                        f"{participant.sort_record.name} - {indicator.name}"
                    )
        
        return {
            'is_complete': filled == total_required,
            'filled_percent': round((filled / total_required * 100), 1) if total_required > 0 else 0,
            'missing_data': missing
        }

class TrialParticipant(SoftDeleteModel):
    """
    Участник сортоопыта
    
    Каждый Trial может иметь несколько участников (сортов).
    Участники делятся на стандарты (группа=0) и испытываемые (группа=1).
    
    БИЗНЕС-ПРАВИЛО: Культура сорта ДОЛЖНА совпадать с культурой испытания!
    """
    trial = models.ForeignKey(
        Trial,
        on_delete=models.CASCADE,
        related_name='participants',
        help_text="Сортоопыт"
    )
    sort_record = models.ForeignKey(
        SortRecord,
        on_delete=models.CASCADE,
        related_name='trial_participations',
        help_text="Сорт-участник"
    )
    
    # Статистическая группа
    STAT_GROUP_CHOICES = [
        (0, 'Стандарт'),
        (1, 'Испытываемый'),
    ]
    statistical_group = models.IntegerField(
        choices=STAT_GROUP_CHOICES,
        default=1,
        help_text="0 = стандарт, 1 = испытываемый"
    )
    
    # Результат статистической обработки (рассчитывается автоматически)
    STAT_RESULT_CHOICES = [
        (-1, 'Существенно ниже стандарта'),
        (0, 'Несущественное отклонение'),
        (1, 'Существенно выше стандарта'),
    ]
    statistical_result = models.IntegerField(
        choices=STAT_RESULT_CHOICES,
        null=True,
        blank=True,
        help_text="Результат сравнения со стандартом (автоматически)"
    )
    
    participant_number = models.IntegerField(
        help_text="Номер участника в опыте (порядковый)"
    )
    
    # Связь с заявкой (опционально)
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trial_participations',
        help_text="Заявка, по которой сорт включен в опыт (если есть)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Участник сортоопыта"
        verbose_name_plural = "Участники сортоопытов"
        ordering = ['trial', 'participant_number']
        unique_together = [
            ['trial', 'sort_record'],
            ['trial', 'participant_number']
        ]
    
    def clean(self):
        """
        Валидация бизнес-правил при добавлении участника
        """
        from django.core.exceptions import ValidationError
        
        # ПРАВИЛО 1: Культура сорта должна совпадать с культурой испытания
        if self.trial and self.trial.culture and self.sort_record and self.sort_record.culture:
            if self.trial.culture.id != self.sort_record.culture.id:
                raise ValidationError({
                    'sort_record': f'Сорт "{self.sort_record.name}" относится к культуре "{self.sort_record.culture.name}", '
                                  f'но испытание проводится для культуры "{self.trial.culture.name}". '
                                  f'Можно добавить только сорта культуры "{self.trial.culture.name}".'
                })
        
        # ПРАВИЛО 2: Если культура испытания указана, у сорта должна быть культура
        if self.trial and self.trial.culture and self.sort_record and not self.sort_record.culture:
            raise ValidationError({
                'sort_record': f'У сорта "{self.sort_record.name}" не указана культура. '
                              f'Для участия в испытании культуры "{self.trial.culture.name}" необходимо указать культуру сорта.'
            })
        
        # ПРАВИЛО 3: Должен быть хотя бы один стандарт в опыте (проверка при добавлении испытываемых)
        if self.statistical_group == 1:  # Испытываемый сорт
            # Проверяем есть ли стандарты
            has_standards = TrialParticipant.objects.filter(
                trial=self.trial,
                statistical_group=0,
                is_deleted=False
            ).exists()
            
            # Если нет стандартов и это не первый участник - предупреждение
            total_participants = TrialParticipant.objects.filter(
                trial=self.trial,
                is_deleted=False
            ).count()
            
            if not has_standards and total_participants > 0:
                # Мягкое предупреждение - не блокируем, но информируем
                import warnings
                warnings.warn(
                    f'В испытании "{self.trial}" нет стандартных сортов. '
                    f'Рекомендуется добавить хотя бы один стандарт (statistical_group=0) для сравнения.',
                    UserWarning
                )
    
    def save(self, *args, **kwargs):
        """Вызываем валидацию перед сохранением"""
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        group_mark = " (Стандарт)" if self.statistical_group == 0 else ""
        stat_mark = ""
        if self.statistical_result == 1:
            stat_mark = " ++"
        elif self.statistical_result == -1:
            stat_mark = " --"
        return f"{self.trial} - #{self.participant_number} {self.sort_record.name}{group_mark}{stat_mark}"
    
    @property
    def is_standard(self):
        """Стандарт ли этот сорт"""
        return self.statistical_group == 0
    
    def calculate_statistical_result(self):
        """
        Рассчитать статистический результат на основе НСР
        
        Сравнивает отклонение от стандарта с НСР:
        - Если |отклонение| > НСР и положительное → +1
        - Если |отклонение| > НСР и отрицательное → -1
        - Иначе → 0
        """
        if self.is_standard:
            self.statistical_result = 0
            return
        
        # Получить статистику опыта
        stats = self.trial.calculate_trial_statistics()
        if not stats:
            return
        
        lsd = stats['lsd']
        
        # Получить урожайность участника
        try:
            from trials_app.models import Indicator
            yield_indicator = Indicator.objects.get(code='yield')
        except:
            return
        
        result = TrialResult.objects.filter(
            participant=self,
            indicator=yield_indicator
        ).first()
        
        if not result or result.value is None:
            return
        
        # Получить урожайность стандарта
        standard = self.trial.get_standard_participants().first()
        if not standard:
            return
        
        standard_result = TrialResult.objects.filter(
            participant=standard,
            indicator=yield_indicator
        ).first()
        
        if not standard_result or standard_result.value is None:
            return
        
        # Отклонение от стандарта
        deviation = result.value - standard_result.value
        
        # Сравнение с НСР
        if abs(deviation) > lsd:
            self.statistical_result = 1 if deviation > 0 else -1
        else:
            self.statistical_result = 0
        
        self.save()


class TrialResult(SoftDeleteModel):
    """
    Результаты участника (гибридный подход)
    
    Хранит как итоговое значение (value), так и опциональные данные по делянкам.
    Если делянки заполнены, value рассчитывается автоматически как среднее.
    """
    participant = models.ForeignKey(
        TrialParticipant,
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True,
        help_text="Участник сортоопыта"
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        related_name='trial_results',
        help_text="Показатель"
    )
    
    # Итоговое значение (обязательно)
    value = models.FloatField(
        null=True,
        blank=True,
        help_text="Среднее значение или общее значение"
    )
    
    
    # Текстовое значение (для качественных показателей)
    text_value = models.TextField(
        blank=True,
        null=True,
        help_text="Текстовое значение (для нечисловых показателей)"
    )
    
    measurement_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата измерения"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Примечания"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trial_results_created',
        help_text="Кто внес данные (сортопыт)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Для обратной совместимости
    trial = models.ForeignKey(
        Trial,
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True
    )
    sort_record = models.ForeignKey(
        SortRecord,
        on_delete=models.CASCADE,
        related_name='trial_results',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Результат испытания"
        verbose_name_plural = "Результаты испытаний"
        ordering = ['-measurement_date']
        unique_together = ['participant', 'indicator']
    
    def __str__(self):
        return f"{self.participant.sort_record.name} - {self.indicator.name}: {self.value}"
    
    def save(self, *args, **kwargs):
        """Сохранение результата"""
        # Для обратной совместимости
        if self.participant:
            self.trial = self.participant.trial
            self.sort_record = self.participant.sort_record
        
        super().save(*args, **kwargs)
        
        # После сохранения пересчитать статистический результат участника
        if self.participant and self.indicator.code == 'yield':
            self.participant.calculate_statistical_result()

class TrialLaboratoryResult(SoftDeleteModel):
    """
    Лабораторные результаты для конкретного испытания (качественные показатели)
    
    ВАЖНО: Каждый Trial отправляет СВОЙ образец в лабораторию!
    Один Trial → один набор лабораторных результатов.
    
    Вносятся лабораторией ПОСЛЕ завершения основных полевых испытаний.
    Только для показателей с is_quality=True (белок, клейковина, натура зерна и т.д.)
    
    Связь: Trial → TrialLaboratoryResult → Indicator (is_quality=True)
    
    Пример:
        Trial #15 (Алматинская область) → образец LAB-2025-001-ALM → белок 14.5%
        Trial #16 (Акмолинская область) → образец LAB-2025-002-AKM → белок 13.8%
        Trial #17 (Костанайская область) → образец LAB-2025-003-KST → белок 15.2%
    """
    trial = models.ForeignKey(
        Trial,
        on_delete=models.CASCADE,
        related_name='laboratory_results',
        help_text="Испытание, для которого проводился анализ"
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        related_name='trial_laboratory_results',
        help_text="Показатель качества"
    )
    
    # Опциональная связь с конкретным участником
    # (если в Trial несколько сортов и каждый анализируется отдельно)
    participant = models.ForeignKey(
        TrialParticipant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='laboratory_results',
        help_text="Участник, от которого взята проба (опционально)"
    )
    
    # Значение
    value = models.FloatField(
        null=True,
        blank=True,
        help_text="Числовое значение показателя"
    )
    text_value = models.TextField(
        blank=True,
        null=True,
        help_text="Текстовое значение (для нечисловых показателей)"
    )
    
    # Метаданные лабораторного анализа
    laboratory_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Код пробы в лаборатории (LAB-2025-001-ALM)"
    )
    analysis_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата проведения анализа"
    )
    sample_weight_kg = models.FloatField(
        null=True,
        blank=True,
        help_text="Вес отправленного образца, кг"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Примечания от лаборатории"
    )
    
    # Кто внес данные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trial_laboratory_results_created',
        help_text="Сотрудник лаборатории, внесший данные"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Лабораторный результат испытания"
        verbose_name_plural = "Лабораторные результаты испытаний"
        ordering = ['-analysis_date', '-created_at']
        unique_together = ['trial', 'indicator', 'participant']
    
    def __str__(self):
        trial_info = f"Trial #{self.trial.id}"
        if self.participant:
            trial_info += f" - {self.participant.sort_record.name}"
        return f"{trial_info} - {self.indicator.name}: {self.value}"
    
    def clean(self):
        """Валидация: разрешены только качественные показатели"""
        from django.core.exceptions import ValidationError
        
        if self.indicator and not self.indicator.is_quality:
            raise ValidationError({
                'indicator': f'Показатель "{self.indicator.name}" не является качественным. '
                            f'Для лабораторных результатов можно использовать только показатели '
                            f'с is_quality=True (белок, клейковина, натура зерна и т.д.)'
            })
        
        # Проверка что Trial завершен
        if self.trial and self.trial.status not in ['completed_008', 'lab_sample_sent', 'lab_completed']:
            raise ValidationError({
                'trial': f'Испытание #{self.trial.id} должно быть завершено (status=completed_008) '
                        f'перед внесением лабораторных результатов. '
                        f'Текущий статус: {self.trial.get_status_display()}'
            })
    
    def save(self, *args, **kwargs):
        """Вызываем валидацию перед сохранением"""
        self.clean()
        super().save(*args, **kwargs)


class Document(SoftDeleteModel):
    """
    Документы
    
    Могут быть привязаны к заявке или к конкретному испытанию.
    
    Обязательные документы для заявки:
    - Заявление на испытание (application_for_testing)
    - Анкета селекционного достижения (breeding_questionnaire)
    - Описание сорта (variety_description)
    - Фото растения с линейкой (plant_photo_with_ruler)
    - Документ о праве подачи (right_to_submit) - если заявитель посредник/правопреемник
    - Документ об отсутствии ГМО (gmo_free) - если сорт иностранной селекции
    """
    DOCUMENT_TYPES = [
        # Обязательные документы для заявки
        ('application_for_testing', 'Заявление на испытание'),
        ('breeding_questionnaire', 'Анкета селекционного достижения'),
        ('variety_description', 'Описание сорта'),
        ('plant_photo_with_ruler', 'Фото растения с линейкой'),
        ('right_to_submit', 'Документ о праве подачи'),
        ('gmo_free', 'Документ об отсутствии ГМО'),
        # Прочие документы
        ('report', 'Отчет'),
        ('protocol', 'Протокол'),
        ('certificate', 'Сертификат'),
        ('decision', 'Решение комиссии'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES, default='other')
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    
    # Документ может быть привязан к заявке ИЛИ к испытанию
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='documents', 
        null=True, 
        blank=True,
        help_text="Заявка, к которой относится документ"
    )
    trial = models.ForeignKey(
        Trial, 
        on_delete=models.CASCADE, 
        related_name='documents', 
        null=True, 
        blank=True,
        help_text="Испытание, к которому относится документ"
    )
    
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Флаги для обязательных документов
    is_mandatory = models.BooleanField(
        default=False,
        help_text="Обязательный документ для заявки"
    )
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"


class TrialPlan(SoftDeleteModel):
    """
    План сортоиспытаний на год
    
    Упрощенная модель с JSON полем participants для гибкости структуры.
    Хранит участников (сорта) с их параметрами испытаний по ГСУ.
    
    Структура participants:
    {
        "participants": [
            {
                "patents_sort_id": 1774,
                "statistical_group": 0,
                "seeds_provision": "provided",
                "participant_number": 2,
                "maturity_group": "D03",
                "application": 22,  // опционально, если из заявки
                "trials": [
                    {
                        "region_id": 1,
                        "predecessor": "fallow",  // или culture_id (например: 5)
                        "seeding_rate": 4.5
                    }
                ]
            }
        ]
    }
    """
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('structured', 'Структурировано'),
        ('distributed', 'Распределено'),
        ('finalized', 'Завершено'),
    ]
    
    # Основные поля
    year = models.IntegerField(help_text="Год проведения испытаний")
    oblast = models.ForeignKey(
        Oblast,
        on_delete=models.CASCADE,
        related_name='trial_plans',
        help_text="Область для испытаний"
    )
    trial_type = models.ForeignKey(
        TrialType,
        on_delete=models.PROTECT,
        related_name='trial_plans',
        null=True,
        blank=True,
        help_text="Тип испытания по умолчанию (КСИ, ООС, ДЮС). Реальный тип - в TrialPlanTrial.trial_type"
    )
    # culture убрано - теперь через TrialPlanCulture
    
    total_participants = models.IntegerField(
        default=0,
        help_text="Общее количество участников в плане"
    )
    
    # Статус плана
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        help_text="Статус плана испытаний"
    )
    
    # JSON поле с участниками и их параметрами
    participants = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON структура с участниками плана"
    )
    
    # Пользователь и метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_trial_plans',
        help_text="Кто создал план"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "План испытаний"
        verbose_name_plural = "Планы испытаний"
        ordering = ['-year', '-created_at']
        # unique_together убран, так как:
        # 1. trial_type теперь опциональный дефолт (не источник истины)
        # 2. Может быть несколько планов для одной области/года (разные культуры)
        # 3. Реальная уникальность определяется на уровне TrialPlanCulture
    
    def __str__(self):
        return f"План {self.year} ({self.oblast.name})"
    
    def get_participants_count(self):
        """Получить количество участников"""
        return TrialPlanParticipant.objects.filter(
            culture_trial_type__trial_plan_culture__trial_plan=self,
            is_deleted=False
        ).count()
    
    def get_applications_count(self):
        """Получить количество заявок в плане"""
        return TrialPlanParticipant.objects.filter(
            culture_trial_type__trial_plan_culture__trial_plan=self,
            is_deleted=False,
            application__isnull=False
        ).values('application').distinct().count()
    
    def get_registry_sorts_count(self):
        """Получить количество сортов из реестра (без заявок)"""
        return TrialPlanParticipant.objects.filter(
            culture_trial_type__trial_plan_culture__trial_plan=self,
            is_deleted=False,
            application__isnull=True
        ).count()
    
    def get_trials_count(self):
        """Получить общее количество сортоопытов (по всем участникам по всем регионам)"""
        return TrialPlanTrial.objects.filter(
            participant__culture_trial_type__trial_plan_culture__trial_plan=self,
            is_deleted=False
        ).count()
    
    def update_statistics(self):
        """Обновить статистику плана"""
        self.total_participants = self.get_participants_count()
        self.save()


class TrialPlanParticipant(SoftDeleteModel):
    """
    Участник плана испытаний
    
    Связывает тип испытания культуры с конкретным сортом (участником)
    
    Новая структура: TrialPlan → TrialPlanCulture → TrialPlanCultureTrialType → TrialPlanParticipant
    """
    # Привязка к типу испытания культуры
    culture_trial_type = models.ForeignKey(
        'TrialPlanCultureTrialType',
        on_delete=models.CASCADE,
        related_name='participants',
        help_text="Тип испытания культуры в плане"
    )
    
    # Данные сорта
    patents_sort_id = models.IntegerField(help_text="ID сорта в Patents Service")
    statistical_group = models.IntegerField(
        choices=[(0, 'Стандарт'), (1, 'Испытываемый')],
        default=1,
        help_text="Статистическая группа"
    )
    seeds_provision = models.CharField(
        max_length=20,
        choices=[
            ('provided', 'Предоставлены'),
            ('not_provided', 'Не предоставлены'),
        ],
        default='provided',
        help_text="Обеспеченность семенами"
    )
    participant_number = models.IntegerField(help_text="Номер участника в плане")
    maturity_group = models.CharField(
        max_length=10,
        help_text="Группа спелости (например: M02, M03)"
    )
    
    # Связь с заявкой (опционально)
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Связанная заявка (если участник из заявки)"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_trial_plan_participants',
        help_text="Кто добавил участника"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Участник плана"
        verbose_name_plural = "Участники планов"
        ordering = ['participant_number']
        unique_together = [
            ['culture_trial_type', 'participant_number', 'is_deleted']
        ]
    
    @property
    def trial_plan(self):
        """Получить план через culture_trial_type"""
        return self.culture_trial_type.trial_plan_culture.trial_plan
    
    @property  
    def trial_type(self):
        """Получить тип испытания"""
        return self.culture_trial_type.trial_type
    
    @property
    def culture(self):
        """Получить культуру"""
        return self.culture_trial_type.trial_plan_culture.culture
    
    def __str__(self):
        return f"Участник {self.participant_number} (сорт {self.patents_sort_id}) в {self.culture_trial_type}"


class TrialPlanTrial(SoftDeleteModel):
    """
    Испытание в плане
    
    Связывает участника плана с конкретным регионом (ГСУ) для проведения испытания.
    Тип испытания определяется на уровне TrialPlanCultureTrialType (через participant.culture_trial_type).
    """
    # Сезон посадки
    SEASON_CHOICES = [
        ('spring', 'Весна'),
        ('autumn', 'Осень'),
        ('summer', 'Лето'),
        ('winter', 'Зима'),
    ]
    
    participant = models.ForeignKey(
        TrialPlanParticipant,
        on_delete=models.CASCADE,
        related_name='trials',
        help_text="Участник плана"
    )
    
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        help_text="Регион (ГСУ) для проведения испытания"
    )
    
    # Параметры испытания
    predecessor = models.CharField(
        max_length=50,
        help_text="Предшественник (например: 'fallow', 'wheat', 'barley')"
    )
    seeding_rate = models.FloatField(
        help_text="Норма высева"
    )
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        default='spring',
        help_text="Сезон посадки/посева (на уровне trial)"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_trial_plan_trials',
        help_text="Кто создал испытание"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def trial_type(self):
        """Получить тип испытания через участника"""
        return self.participant.trial_type
    
    @property
    def trial_plan(self):
        """Получить план через участника"""
        return self.participant.trial_plan
    
    class Meta:
        verbose_name = "Испытание в плане"
        verbose_name_plural = "Испытания в планах"
        ordering = ['region__name']
    
    def __str__(self):
        return f"Испытание {self.participant.patents_sort_id} в {self.region.name}"


class TrialPlanCulture(SoftDeleteModel):
    """
    Связь плана с культурами
    
    Один план может содержать несколько культур
    """
    trial_plan = models.ForeignKey(
        TrialPlan,
        on_delete=models.CASCADE,
        related_name='cultures',
        help_text="План испытаний"
    )
    culture = models.ForeignKey(
        Culture,
        on_delete=models.CASCADE,
        help_text="Культура"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_trial_plan_cultures',
        help_text="Кто добавил культуру в план"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Культура в плане"
        verbose_name_plural = "Культуры в планах"
        unique_together = [
            ['trial_plan', 'culture', 'is_deleted']
        ]
    
    def __str__(self):
        return f"Культура {self.culture.name} в плане {self.trial_plan.id}"


class TrialPlanCultureTrialType(SoftDeleteModel):
    """
    Типы испытаний для культуры в плане
    
    Связывает культуру с типами испытаний (КСИ, ООС, ДЮС и т.д.)
    Один план культуры может иметь несколько типов испытаний.
    
    Структура: TrialPlan → TrialPlanCulture → TrialPlanCultureTrialType → TrialPlanParticipant
    """
    trial_plan_culture = models.ForeignKey(
        TrialPlanCulture,
        on_delete=models.CASCADE,
        related_name='trial_types',
        help_text="Культура в плане испытаний"
    )
    trial_type = models.ForeignKey(
        TrialType,
        on_delete=models.PROTECT,
        related_name='plan_culture_trial_types',
        help_text="Тип испытания (КСИ, ООС, ДЮС)"
    )
    
    # Сезон посадки для этого типа испытания
    SEASON_CHOICES = [
        ('spring', 'Весна'),
        ('autumn', 'Осень'),
        ('summer', 'Лето'),
        ('winter', 'Зима'),
    ]
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        default='spring',
        help_text="Сезон посадки/посева для данного типа испытания"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_trial_plan_culture_trial_types',
        help_text="Кто добавил тип испытания"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Тип испытания в культуре плана"
        verbose_name_plural = "Типы испытаний в культурах планов"
        unique_together = [
            ['trial_plan_culture', 'trial_type', 'is_deleted']
        ]
    
    def __str__(self):
        return f"{self.trial_type.name} для {self.trial_plan_culture.culture.name} в плане {self.trial_plan_culture.trial_plan.id}"


class AnnualDecisionTable(SoftDeleteModel):
    """
    Годовая таблица решений по сортам
    
    Один документ на год + область (+ опционально культура).
    Содержит все сорта с решениями за год.
    
    Пример: "Годовая таблица решений 2024 - Костанайская область - Картофель"
    """
    
    year = models.IntegerField(
        help_text="Год составления таблицы (например: 2024)"
    )
    oblast = models.ForeignKey(
        Oblast,
        on_delete=models.CASCADE,
        related_name='annual_decision_tables',
        help_text="Область"
    )
    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='annual_decision_tables',
        help_text="Культура (опционально, для фильтрации)"
    )
    
    # Статус таблицы
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('finalized', 'Завершена'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Статус таблицы"
    )
    
    # Название таблицы
    title = models.CharField(
        max_length=512,
        blank=True,
        help_text="Название таблицы (автоматически генерируется)"
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='annual_tables_created',
        help_text="Кто создал таблицу"
    )
    finalized_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='annual_tables_finalized',
        help_text="Кто завершил таблицу"
    )
    finalized_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата завершения таблицы"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Годовая таблица решений"
        verbose_name_plural = "Годовые таблицы решений"
        ordering = ['-year', '-created_at']
        unique_together = [['year', 'oblast', 'culture']]
    
    def __str__(self):
        culture_str = f" - {self.culture.name}" if self.culture else ""
        return f"Таблица {self.year} - {self.oblast.name}{culture_str}"
    
    def save(self, *args, **kwargs):
        """Автоматически генерировать название"""
        if not self.title:
            culture_str = f" - {self.culture.name}" if self.culture else ""
            self.title = f"Годовая таблица решений {self.year} - {self.oblast.name}{culture_str}"
        super().save(*args, **kwargs)
    
    def get_items_count(self):
        """Количество сортов в таблице"""
        return self.items.filter(is_deleted=False).count()
    
    def get_decisions_count(self):
        """Количество принятых решений"""
        return self.items.filter(
            is_deleted=False
        ).exclude(decision='pending').count()
    
    def get_progress_percentage(self):
        """Процент завершенности"""
        total = self.get_items_count()
        if total == 0:
            return 0
        decided = self.get_decisions_count()
        return round((decided / total) * 100, 1)
    
    def is_all_decisions_made(self):
        """Все ли решения приняты"""
        return self.get_items_count() == self.get_decisions_count()
    
    def get_statistics(self):
        """Статистика по решениям"""
        items = self.items.filter(is_deleted=False)
        return {
            'total': items.count(),
            'approved': items.filter(decision='approved').count(),
            'removed': items.filter(decision='removed').count(),
            'continue': items.filter(decision='continue').count(),
            'pending': items.filter(decision='pending').count(),
        }


class AnnualDecisionItem(SoftDeleteModel):
    """
    Элемент годовой таблицы решений (одна строка = один сорт)
    
    Содержит:
    - Агрегированные данные испытаний по годам
    - Решение по сорту (одобрено/снято/продолжить)
    - Обоснование решения
    """
    
    # Связь с таблицей
    annual_table = models.ForeignKey(
        AnnualDecisionTable,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Годовая таблица"
    )
    
    # Порядковый номер в таблице
    row_number = models.IntegerField(
        help_text="Порядковый номер строки (№ п/п)"
    )
    
    # Сорт
    sort_record = models.ForeignKey(
        SortRecord,
        on_delete=models.CASCADE,
        related_name='annual_decision_items',
        help_text="Сорт"
    )
    
    # === Данные испытаний (агрегированные) ===
    
    # Группа спелости
    maturity_group = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Группа спелости (1, 2, 3, 4, 5)"
    )
    
    # Урожайность по годам
    yields_by_year = models.JSONField(
        default=dict,
        help_text="Урожайность по годам: {2022: 125, 2023: 210, 2024: 97}"
    )
    
    # Средняя урожайность
    average_yield = models.FloatField(
        null=True,
        blank=True,
        help_text="Средняя урожайность за все годы (ц/га)"
    )
    
    # Отклонение от стандарта
    deviation_from_standard = models.FloatField(
        null=True,
        blank=True,
        help_text="Отклонение от стандарта (ц/га)"
    )
    
    # Показатели последнего года
    last_year_data = models.JSONField(
        default=dict,
        help_text="""
        Все показатели качества последнего года:
        {
            "tuber_weight": 142,
            "taste_score": 5,
            "marketable_percentage": 92.5,
            "damage_resistance": 95,
            "diseases": {...},
            "pests": {...},
            "biochemistry": {...}
        }
        """
    )
    
    # Период испытаний
    years_tested = models.IntegerField(
        help_text="Количество лет испытаний (1, 2 или 3)"
    )
    year_started = models.IntegerField(
        help_text="Год начала испытаний (например: 2022)"
    )
    
    # === РЕШЕНИЕ ===
    
    DECISION_CHOICES = [
        ('pending', 'Ожидает решения'),
        ('approved', 'Одобрено к включению в Госреестр'),
        ('continue', 'Продолжить испытания'),
        ('removed', 'Снять с испытаний'),
    ]
    decision = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES,
        default='pending',
        help_text="Решение по сорту"
    )
    
    # Обоснование решения
    decision_justification = models.TextField(
        blank=True,
        null=True,
        help_text="Обоснование принятого решения"
    )
    
    # Рекомендации по использованию
    decision_recommendations = models.TextField(
        blank=True,
        null=True,
        help_text="Рекомендации по возделыванию и использованию"
    )
    
    # Рекомендуемые зоны возделывания
    recommended_zones = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        Рекомендуемые климатические зоны и ГСУ:
        [
            {
                "climate_zone_id": 1,
                "climate_zone_name": "Лесостепная",
                "region_ids": [1, 2, 3]
            }
        ]
        """
    )
    
    # === Для продления испытаний ===
    continue_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Причина продления испытаний"
    )
    continue_until_year = models.IntegerField(
        null=True,
        blank=True,
        help_text="До какого года продлить испытания"
    )
    
    # === Для снятия с испытаний ===
    removal_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Причина снятия с испытаний"
    )
    
    # === Метаданные решения ===
    decision_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата принятия решения"
    )
    decided_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='annual_decisions_made',
        help_text="Кто принял решение"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Элемент годовой таблицы"
        verbose_name_plural = "Элементы годовых таблиц"
        ordering = ['annual_table', 'row_number']
        unique_together = [['annual_table', 'sort_record']]
    
    def __str__(self):
        return f"№{self.row_number} - {self.sort_record.name} ({self.get_decision_display()})"
    
    def aggregate_trial_data(self):
        """
        Агрегировать данные из испытаний сорта в области
        
        ЛОГИКА: Данные берутся из Trial через заявку
        Application → PlannedDistribution → Trial → TrialResult
        
        Собирает данные для:
        - yields_by_year - урожайность по годам
        - average_yield - средняя урожайность
        - deviation_from_standard - отклонение от стандарта
        - last_year_data - все показатели последнего года
        """
        # Найти заявку для этого сорта
        from trials_app.models import Application
        
        try:
            application = Application.objects.get(
                sort_record=self.sort_record,
                target_oblasts=self.annual_table.oblast,
                is_deleted=False
            )
        except Application.DoesNotExist:
            # Если нет заявки, попробовать найти напрямую через Trial
            # (для старых сортов из реестра без заявок)
            self._aggregate_from_trials_directly()
            return
        except Application.MultipleObjectsReturned:
            # Если несколько заявок, берем последнюю
            application = Application.objects.filter(
                sort_record=self.sort_record,
                target_oblasts=self.annual_table.oblast,
                is_deleted=False
            ).order_by('-created_at').first()
        
        # Найти PlannedDistribution для области
        distributions = PlannedDistribution.objects.filter(
            application=application,
            region__oblast=self.annual_table.oblast,
            is_deleted=False
        )
        
        # Собрать все Trial из distributions
        all_trials = []
        for distribution in distributions:
            trials = Trial.objects.filter(
                region=distribution.region,
                participants__application=application,
                is_deleted=False,
                status__in=['completed_008', 'lab_sample_sent', 'lab_completed', 'completed', 'approved', 'continue', 'rejected']
            ).distinct()
            all_trials.extend(trials)
        
        if not all_trials:
            return
        
        # Собрать урожайность по годам (среднее по всем ГСУ области)
        yields_by_year = {}
        last_year = None
        
        for trial in all_trials:
            year = trial.year or (trial.start_date.year if trial.start_date else None)
            if not year:
                continue
            
            # Отслеживать последний год
            if last_year is None or year > last_year:
                last_year = year
            
            # Получить урожайность для ДАННОГО СОРТА в этом Trial
            participant = trial.participants.filter(
                application=application,
                sort_record=self.sort_record,
                is_deleted=False
            ).first()
            
            if not participant:
                continue
            
            # Получить урожайность участника
            yield_result = TrialResult.objects.filter(
                participant=participant,
                indicator__code='yield',
                value__isnull=False,
                is_deleted=False
            ).first()
            
            if yield_result and yield_result.value:
                # Группировка по годам (среднее если несколько ГСУ в один год)
                if year not in yields_by_year:
                    yields_by_year[year] = []
                yields_by_year[year].append(yield_result.value)
        
        # Рассчитать средние по годам
        self.yields_by_year = {
            str(year): round(sum(values) / len(values), 1)
            for year, values in yields_by_year.items()
        }
        
        # Средняя урожайность за все годы
        if self.yields_by_year:
            all_yields = list(self.yields_by_year.values())
            self.average_yield = round(sum(all_yields) / len(all_yields), 1)
            self.years_tested = len(self.yields_by_year)
            self.year_started = min(int(y) for y in self.yields_by_year.keys())
        
        # Рассчитать отклонение от стандарта
        self._calculate_deviation_from_standard(all_trials, last_year)
        
        # Собрать показатели последнего года
        if last_year:
            self._aggregate_last_year_indicators(all_trials, last_year, application)
        
        self.save()
    
    def _aggregate_from_trials_directly(self):
        """
        Запасной вариант: агрегация напрямую из Trial
        (для сортов из реестра без заявок)
        """
        trials = Trial.objects.filter(
            sort_records=self.sort_record,
            region__oblast=self.annual_table.oblast,
            is_deleted=False
        ).order_by('year')
        
        if not trials.exists():
            return
        
        yields_by_year = {}
        for trial in trials:
            year = trial.year or (trial.start_date.year if trial.start_date else None)
            if not year:
                continue
            
            yield_results = trial.results.filter(
                indicator__code='yield',
                sort_record=self.sort_record,
                value__isnull=False,
                is_deleted=False
            )
            
            if yield_results.exists():
                avg_yield = sum(r.value for r in yield_results) / yield_results.count()
                if year not in yields_by_year:
                    yields_by_year[year] = []
                yields_by_year[year].append(avg_yield)
        
        self.yields_by_year = {
            str(year): round(sum(values) / len(values), 1)
            for year, values in yields_by_year.items()
        }
        
        if self.yields_by_year:
            all_yields = list(self.yields_by_year.values())
            self.average_yield = round(sum(all_yields) / len(all_yields), 1)
            self.years_tested = len(self.yields_by_year)
            self.year_started = min(int(y) for y in self.yields_by_year.keys())
        
        self.save()
    
    def _calculate_deviation_from_standard(self, trials, year):
        """
        Рассчитать отклонение от стандарта
        
        Находит стандартный сорт (statistical_group=0) и сравнивает урожайность
        """
        if not year or not self.average_yield:
            return
        
        # Найти стандартный сорт в области/культуре
        for trial in trials:
            trial_year = trial.year or (trial.start_date.year if trial.start_date else None)
            if trial_year != year:
                continue
            
            # Найти стандартного участника
            standard_participant = trial.participants.filter(
                statistical_group=0,  # Стандарт
                is_deleted=False
            ).first()
            
            if not standard_participant:
                continue
            
            # Получить урожайность стандарта
            standard_yield = TrialResult.objects.filter(
                participant=standard_participant,
                indicator__code='yield',
                value__isnull=False,
                is_deleted=False
            ).first()
            
            if standard_yield and standard_yield.value:
                # Отклонение = наша средняя - стандарт
                self.deviation_from_standard = round(self.average_yield - standard_yield.value, 1)
                return
        
        # Если стандарт не найден, установить 0 или "ст"
        self.deviation_from_standard = 0
    
    def _aggregate_last_year_indicators(self, trials, last_year, application):
        """
        Собрать все показатели качества последнего года
        
        Агрегирует данные из TrialResult для всех показателей
        """
        last_year_data = {}
        
        # Найти испытания последнего года
        last_year_trials = [
            t for t in trials
            if (t.year or (t.start_date.year if t.start_date else None)) == last_year
        ]
        
        if not last_year_trials:
            return
        
        # Собрать все показатели
        all_indicators = set()
        for trial in last_year_trials:
            # Найти участника этого сорта в trial
            participant = trial.participants.filter(
                application=application,
                sort_record=self.sort_record,
                is_deleted=False
            ).first()
            
            if not participant:
                continue
            
            # Получить все результаты участника
            results = TrialResult.objects.filter(
                participant=participant,
                value__isnull=False,
                is_deleted=False
            ).select_related('indicator')
            
            for result in results:
                indicator_code = result.indicator.code
                all_indicators.add(indicator_code)
                
                # Сохранить значение (если несколько Trial, будет перезаписано - берем последнее)
                if result.value is not None:
                    last_year_data[indicator_code] = result.value
        
        self.last_year_data = last_year_data
