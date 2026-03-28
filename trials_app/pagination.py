from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Стандартная пагинация для API.

    Переопределяет глобальный PAGE_SIZE=1000 из settings,
    чтобы list endpoints возвращали разумное количество записей.
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
