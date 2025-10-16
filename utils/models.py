"""
Базовые модели для Trials Service
"""
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet для мягкого удаления"""
    
    def delete(self):
        """Мягкое удаление для QuerySet"""
        return self.update(deleted_at=timezone.now())
    
    def hard_delete(self):
        """Физическое удаление для QuerySet"""
        return super().delete()
    
    def alive(self):
        """Только неудаленные записи"""
        return self.filter(deleted_at__isnull=True)
    
    def dead(self):
        """Только удаленные записи"""
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Manager для мягкого удаления"""
    
    def get_queryset(self):
        """По умолчанию возвращаем только неудаленные записи"""
        return SoftDeleteQuerySet(self.model, using=self._db).alive()
    
    def all_with_deleted(self):
        """Все записи включая удаленные"""
        return SoftDeleteQuerySet(self.model, using=self._db)
    
    def deleted_only(self):
        """Только удаленные записи"""
        return SoftDeleteQuerySet(self.model, using=self._db).dead()


class SoftDeleteModel(models.Model):
    """
    Абстрактная модель с мягким удалением
    
    Вместо физического удаления записи из БД, устанавливается deleted_at
    """
    deleted_at = models.DateTimeField(
        verbose_name='Удалено',
        null=True,
        blank=True,
        default=None,
        db_index=True
    )
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Для доступа ко всем записям
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление объекта"""
        self.deleted_at = timezone.now()
        self.save(using=using)
    
    def hard_delete(self, using=None, keep_parents=False):
        """Физическое удаление объекта"""
        super().delete(using=using, keep_parents=keep_parents)
    
    def restore(self):
        """Восстановление удаленного объекта"""
        self.deleted_at = None
        self.save()
    
    @property
    def is_deleted(self):
        """Проверка, удален ли объект"""
        return self.deleted_at is not None


class TimeStampedModel(models.Model):
    """
    Абстрактная модель с автоматическими временными метками
    """
    created_at = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлено',
        auto_now=True
    )
    
    class Meta:
        abstract = True


class SoftDeleteTimeStampedModel(SoftDeleteModel, TimeStampedModel):
    """
    Абстрактная модель с мягким удалением и временными метками
    """
    class Meta:
        abstract = True


