"""
Сервис для фильтрации данных по культуре
"""
from ...models import Culture


class CultureFilterService:
    """
    Сервис для фильтрации данных по культуре Patents

    Предоставляет методы:
    - Фильтрация списка элементов по ID культуры
    - Получение информации о культуре для metadata
    """

    @staticmethod
    def filter_items(items, patents_culture_id):
        """
        Фильтрация элементов по ID культуры из Patents

        Args:
            items: Список элементов (detailed_items)
            patents_culture_id: ID культуры из Patents (или None)

        Returns:
            Отфильтрованный список элементов
        """
        if patents_culture_id is None:
            return items

        filtered_items = []
        for item in items:
            # Проверяем culture_id через sort_record
            if (item.get('sort_record', {}).get('culture_id') == patents_culture_id or
                item.get('culture', {}).get('culture_id') == patents_culture_id):
                filtered_items.append(item)

        return filtered_items

    @staticmethod
    def get_culture_info(patents_culture_id):
        """
        Получить информацию о культуре для metadata

        Args:
            patents_culture_id: ID культуры из Patents

        Returns:
            Словарь с информацией о культуре или None
        """
        if patents_culture_id is None:
            return None

        try:
            culture = Culture.objects.get(culture_id=patents_culture_id, is_deleted=False)
            return {
                'patents_culture_id': patents_culture_id,
                'culture_name': culture.name
            }
        except Culture.DoesNotExist:
            return {
                'patents_culture_id': patents_culture_id,
                'culture_name': f'Culture ID {patents_culture_id}'
            }
