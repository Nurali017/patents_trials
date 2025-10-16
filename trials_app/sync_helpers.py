"""
Вспомогательные функции для синхронизации с Patents Service

Реализует паттерн Lazy Loading - загрузка данных только когда они нужны
"""

from django.utils import timezone
from datetime import timedelta
from .models import SortRecord, Culture, GroupCulture, Originator
from .patents_integration import patents_api
import logging

logger = logging.getLogger(__name__)


class SyncStrategy:
    """
    Стратегии синхронизации данных
    
    LAZY - Загружать только при первом обращении
    EAGER - Загружать сразу все данные
    CACHED - Использовать кеш с TTL (Time To Live)
    """
    LAZY = 'lazy'
    EAGER = 'eager'
    CACHED = 'cached'


def get_or_sync_sort(sort_id, strategy=SyncStrategy.CACHED, cache_ttl_days=7):
    """
    Получить сорт из локальной БД или синхронизировать с Patents Service
    
    Args:
        sort_id: ID сорта в Patents Service
        strategy: Стратегия синхронизации (LAZY, EAGER, CACHED)
        cache_ttl_days: Количество дней для кеша (для CACHED стратегии)
    
    Returns:
        SortRecord или None
    
    Example:
        # Ленивая загрузка - использует кеш если есть
        sort = get_or_sync_sort(456, strategy='cached', cache_ttl_days=7)
        
        # Всегда загружать свежие данные
        sort = get_or_sync_sort(456, strategy='eager')
    """
    try:
        # Попытка найти в локальной БД
        sort_record = SortRecord.objects.get(sort_id=sort_id, is_deleted=False)
        
        # Проверяем нужно ли обновить
        needs_sync = False
        
        if strategy == SyncStrategy.EAGER:
            needs_sync = True
        elif strategy == SyncStrategy.CACHED:
            if sort_record.synced_at is None:
                needs_sync = True
            else:
                cache_cutoff = timezone.now() - timedelta(days=cache_ttl_days)
                if sort_record.synced_at < cache_cutoff:
                    needs_sync = True
        # LAZY - не синхронизируем если есть
        
        if needs_sync:
            logger.info(f'Обновление данных сорта {sort_id} из Patents Service')
            sort_record.sync_from_patents()
        
        return sort_record
        
    except SortRecord.DoesNotExist:
        # Нет в локальной БД - загружаем из Patents
        logger.info(f'Загрузка нового сорта {sort_id} из Patents Service')
        sort_data = patents_api.get_sort(sort_id)
        
        if not sort_data:
            logger.warning(f'Сорт {sort_id} не найден в Patents Service')
            return None
        
        # Создаем локальную запись
        sort_record = _create_sort_from_patents(sort_data)
        return sort_record


def get_or_sync_culture(culture_id, strategy=SyncStrategy.CACHED, cache_ttl_days=30):
    """
    Получить культуру из локальной БД или синхронизировать с Patents Service
    
    Args:
        culture_id: ID культуры в Patents Service
        strategy: Стратегия синхронизации
        cache_ttl_days: Количество дней для кеша (по умолчанию 30, культуры меняются редко)
    
    Returns:
        Culture или None
    """
    try:
        culture = Culture.objects.get(culture_id=culture_id, is_deleted=False)
        
        needs_sync = False
        if strategy == SyncStrategy.EAGER:
            needs_sync = True
        elif strategy == SyncStrategy.CACHED:
            if culture.synced_at is None:
                needs_sync = True
            else:
                cache_cutoff = timezone.now() - timedelta(days=cache_ttl_days)
                if culture.synced_at < cache_cutoff:
                    needs_sync = True
        
        if needs_sync:
            logger.info(f'Обновление данных культуры {culture_id} из Patents Service')
            culture.sync_from_patents()
        
        return culture
        
    except Culture.DoesNotExist:
        logger.info(f'Загрузка новой культуры {culture_id} из Patents Service')
        culture_data = patents_api.get_culture(culture_id)
        
        if not culture_data:
            logger.warning(f'Культура {culture_id} не найдена в Patents Service')
            return None
        
        culture = _create_culture_from_patents(culture_data)
        return culture


def get_or_sync_originator(originator_id, strategy=SyncStrategy.CACHED, cache_ttl_days=30):
    """
    Получить оригинатора из локальной БД или синхронизировать с Patents Service
    
    Args:
        originator_id: ID оригинатора в Patents Service
        strategy: Стратегия синхронизации
        cache_ttl_days: Количество дней для кеша
    
    Returns:
        Originator или None
    """
    try:
        originator = Originator.objects.get(originator_id=originator_id, is_deleted=False)
        
        needs_sync = False
        if strategy == SyncStrategy.EAGER:
            needs_sync = True
        elif strategy == SyncStrategy.CACHED:
            if originator.synced_at is None:
                needs_sync = True
            else:
                cache_cutoff = timezone.now() - timedelta(days=cache_ttl_days)
                if originator.synced_at < cache_cutoff:
                    needs_sync = True
        
        if needs_sync:
            logger.info(f'Обновление данных оригинатора {originator_id} из Patents Service')
            originator.sync_from_patents()
        
        return originator
        
    except Originator.DoesNotExist:
        logger.info(f'Загрузка нового оригинатора {originator_id} из Patents Service')
        originator_data = patents_api.get_originator(originator_id)
        
        if not originator_data:
            logger.warning(f'Оригинатор {originator_id} не найден в Patents Service')
            return None
        
        originator = Originator.objects.create(
            originator_id=originator_id,
            name=originator_data.get('name', ''),
            synced_at=timezone.now()
        )
        return originator


def _create_sort_from_patents(sort_data):
    """
    Создать локальную запись сорта из данных Patents Service
    
    Args:
        sort_data: dict с данными сорта из Patents API
    
    Returns:
        SortRecord
    """
    # Создать/обновить культуру
    culture_obj = None
    culture_data = sort_data.get('culture', {})
    if culture_data and culture_data.get('id'):
        culture_obj = _create_culture_from_patents(culture_data)
    
    # Создать запись о сорте
    sort_record = SortRecord.objects.create(
        sort_id=sort_data['id'],
        name=sort_data.get('name', ''),
        public_code=sort_data.get('code'),  # API V2 использует 'code' вместо 'public_code'
        lifestyle=sort_data.get('lifestyle'),
        characteristic=sort_data.get('characteristic'),
        development_cycle=sort_data.get('development_cycle'),
        applicant=sort_data.get('applicant', ''),
        patent_nis=sort_data.get('patent_nis', False),
        note=sort_data.get('note', ''),
        culture=culture_obj,
        synced_at=timezone.now()
    )
    
    # Синхронизировать оригинаторов
    originators_data = sort_data.get('ariginators', []) or sort_data.get('originators', [])
    if originators_data:
        sort_record._sync_originators(originators_data)
    
    logger.info(f'Создана локальная запись сорта: {sort_record.name} (ID: {sort_record.sort_id})')
    return sort_record


def _create_culture_from_patents(culture_data):
    """
    Создать/обновить локальную запись культуры из данных Patents Service
    
    Args:
        culture_data: dict с данными культуры из Patents API
    
    Returns:
        Culture
    """
    # Создать/обновить группу культуры
    group_culture = None
    group_data = culture_data.get('group', {}) or culture_data.get('group_culture', {})
    if group_data and group_data.get('id'):
        group_culture, _ = GroupCulture.objects.update_or_create(
            group_culture_id=group_data['id'],
            defaults={
                'name': group_data.get('name', ''),
                'description': group_data.get('description', ''),
                'code': group_data.get('code', ''),
                'synced_at': timezone.now()
            }
        )
    
    # Создать/обновить культуру
    culture, created = Culture.objects.update_or_create(
        culture_id=culture_data['id'],
        defaults={
            'name': culture_data.get('name', ''),
            'code': culture_data.get('code', ''),
            'group_culture': group_culture,
            'synced_at': timezone.now()
        }
    )
    
    action = 'Создана' if created else 'Обновлена'
    logger.info(f'{action} локальная запись культуры: {culture.name} (ID: {culture.culture_id})')
    return culture


def bulk_sync_sorts(sort_ids, force_update=False):
    """
    Массовая синхронизация нескольких сортов
    
    Args:
        sort_ids: список ID сортов
        force_update: принудительно обновить даже если есть в кеше
    
    Returns:
        dict: статистика синхронизации
        {
            'success': [sort_record1, sort_record2, ...],
            'failed': [(sort_id, error_message), ...],
            'cached': [sort_record1, ...]  # если не было force_update
        }
    """
    result = {
        'success': [],
        'failed': [],
        'cached': []
    }
    
    strategy = SyncStrategy.EAGER if force_update else SyncStrategy.CACHED
    
    for sort_id in sort_ids:
        try:
            sort_record = get_or_sync_sort(sort_id, strategy=strategy)
            if sort_record:
                if force_update:
                    result['success'].append(sort_record)
                else:
                    result['cached'].append(sort_record)
            else:
                result['failed'].append((sort_id, 'Не найден в Patents Service'))
        except Exception as e:
            logger.error(f'Ошибка синхронизации сорта {sort_id}: {e}')
            result['failed'].append((sort_id, str(e)))
    
    return result


def check_sync_health():
    """
    Проверить состояние синхронизации
    
    Returns:
        dict: статистика с рекомендациями
    """
    from django.db.models import Count, Q
    
    # Проверяем устаревшие данные
    week_ago = timezone.now() - timedelta(days=7)
    month_ago = timezone.now() - timedelta(days=30)
    
    stats = {
        'sorts': {
            'total': SortRecord.objects.filter(is_deleted=False).count(),
            'never_synced': SortRecord.objects.filter(is_deleted=False, synced_at__isnull=True).count(),
            'outdated_week': SortRecord.objects.filter(is_deleted=False, synced_at__lt=week_ago).count(),
            'outdated_month': SortRecord.objects.filter(is_deleted=False, synced_at__lt=month_ago).count(),
        },
        'cultures': {
            'total': Culture.objects.filter(is_deleted=False).count(),
            'never_synced': Culture.objects.filter(is_deleted=False, synced_at__isnull=True).count(),
            'outdated_month': Culture.objects.filter(is_deleted=False, synced_at__lt=month_ago).count(),
        },
        'originators': {
            'total': Originator.objects.filter(is_deleted=False).count(),
            'never_synced': Originator.objects.filter(is_deleted=False, synced_at__isnull=True).count(),
            'outdated_month': Originator.objects.filter(is_deleted=False, synced_at__lt=month_ago).count(),
        },
        'recommendations': []
    }
    
    # Рекомендации
    if stats['sorts']['never_synced'] > 0:
        stats['recommendations'].append(
            f"⚠️ {stats['sorts']['never_synced']} сортов никогда не синхронизировались"
        )
    
    if stats['sorts']['outdated_week'] > 10:
        stats['recommendations'].append(
            f"⚠️ {stats['sorts']['outdated_week']} сортов не обновлялись больше недели"
        )
    
    if stats['cultures']['never_synced'] > 0:
        stats['recommendations'].append(
            f"⚠️ {stats['cultures']['never_synced']} культур никогда не синхронизировались"
        )
    
    if not stats['recommendations']:
        stats['recommendations'].append("✅ Все данные актуальны")
    
    return stats

