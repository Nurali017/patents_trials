"""
Вспомогательные функции для Trials Service
"""
import logging
from functools import wraps
from django.core.cache import cache

logger = logging.getLogger(__name__)


def cache_result(timeout=300, key_prefix='trials'):
    """
    Декоратор для кэширования результатов функций
    
    Args:
        timeout: Время жизни кэша в секундах (по умолчанию 5 минут)
        key_prefix: Префикс для ключа кэша
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем ключ кэша
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Пытаемся получить из кэша
            result = cache.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return result
            
            # Выполняем функцию и кэшируем результат
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            logger.debug(f"Cache miss for {cache_key}, cached for {timeout}s")
            
            return result
        return wrapper
    return decorator


def validate_date_range(start_date, end_date):
    """
    Валидация диапазона дат
    
    Args:
        start_date: Начальная дата
        end_date: Конечная дата
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not start_date:
        return False, "Начальная дата обязательна"
    
    if end_date and end_date < start_date:
        return False, "Конечная дата не может быть раньше начальной"
    
    return True, None


def format_trial_status(status):
    """
    Форматирование статуса испытания для отображения
    
    Args:
        status: Код статуса
    
    Returns:
        dict: Информация о статусе
    """
    STATUS_INFO = {
        'planned': {
            'label': 'Запланировано',
            'color': 'blue',
            'icon': 'calendar'
        },
        'active': {
            'label': 'Активно',
            'color': 'green',
            'icon': 'play'
        },
        'completed': {
            'label': 'Завершено',
            'color': 'gray',
            'icon': 'check'
        },
        'cancelled': {
            'label': 'Отменено',
            'color': 'red',
            'icon': 'x'
        }
    }
    
    return STATUS_INFO.get(status, {
        'label': status,
        'color': 'gray',
        'icon': 'question'
    })


def safe_divide(numerator, denominator, default=0):
    """
    Безопасное деление с обработкой деления на ноль
    
    Args:
        numerator: Числитель
        denominator: Знаменатель
        default: Значение по умолчанию при делении на ноль
    
    Returns:
        float: Результат деления или значение по умолчанию
    """
    try:
        return float(numerator) / float(denominator)
    except (ZeroDivisionError, TypeError, ValueError):
        return default


