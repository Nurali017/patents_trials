"""
Интеграция с Patents Service через HTTP API

АРХИТЕКТУРА МИКРОСЕРВИСОВ:
- Trials Service и Patents Service - НЕЗАВИСИМЫЕ микросервисы
- Каждый имеет СВОЮ базу данных (trials_db и patent)
- Взаимодействие ТОЛЬКО через HTTP API (НЕТ прямого доступа к БД!)

ИНТЕГРАЦИЯ:
- Trials → Patents: HTTP запросы к API V2 Patents Service
- Фронтенд вызывает напрямую оба сервиса:
  * http://localhost:8000/api/v2/ - Patents Service (сорта, культуры)
  * http://localhost:8001/api/v1/ - Trials Service (испытания)

ПРИНЦИП РАБОТЫ:
1. Фронтенд получает список сортов от Patents Service
2. Пользователь выбирает сорт (получает sort_id)
3. При создании испытания Trials Service валидирует sort_id через Patents API
4. Trials сохраняет в свою БД: sort_id + денормализованные данные (sort_name)
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)


class PatentsServiceClient:
    """
    HTTP клиент для взаимодействия с Patents Service API
    
    Использует HTTP API для:
    - Валидации существования сортов
    - Получения информации о сортах и культурах
    - Синхронизации справочных данных
    
    Поддерживает аутентификацию через токен.
    """
    
    def __init__(self):
        self.base_url = os.environ.get('PATENTS_SERVICE_URL', 'http://localhost:8000')
        # Пробуем разные варианты API paths
        self.api_v2_url = f"{self.base_url}/api/v2/patents"
        self.api_v1_url = f"{self.base_url}/api"
        self.api_url = self.api_v2_url  # По умолчанию v2
        self.auth_url = f"{self.base_url}/api/v2/patents/auth/"
        self.timeout = 5  # секунд
        self._token = None  # Кешируемый токен
        
        # Учетные данные для сервис-сервис аутентификации
        self.service_username = os.environ.get('PATENTS_SERVICE_USERNAME')
        self.service_password = os.environ.get('PATENTS_SERVICE_PASSWORD')
    
    def get_auth_token(self, username=None, password=None):
        """
        Получить токен аутентификации от Patents Service
        
        Args:
            username: имя пользователя (если None, используется из env)
            password: пароль (если None, используется из env)
            
        Returns:
            str или None: токен аутентификации
        """
        username = username or self.service_username
        password = password or self.service_password
        
        if not username or not password:
            logger.warning("Credentials не настроены для Patents Service")
            return None
        
        try:
            response = requests.post(
                self.auth_url,
                json={
                    'username': username,
                    'password': password
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            token = data.get('token')
            
            if token:
                self._token = token
                logger.info("Успешно получен токен от Patents Service")
            
            return token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении токена от Patents Service: {e}")
            return None
    
    def _get_headers(self, custom_headers=None):
        """
        Подготовить заголовки для запроса с токеном аутентификации
        
        Args:
            custom_headers: дополнительные заголовки
            
        Returns:
            dict: заголовки для запроса
        """
        headers = custom_headers or {}
        
        # Если токен уже есть, используем его
        if self._token:
            headers['Authorization'] = f'Token {self._token}'
        # Иначе пытаемся получить новый токен
        elif self.service_username and self.service_password:
            token = self.get_auth_token()
            if token:
                headers['Authorization'] = f'Token {token}'
        
        return headers
    
    def _make_request(self, method, endpoint, **kwargs):
        """
        Выполнить HTTP запрос к Patents Service с аутентификацией
        
        Args:
            method: HTTP метод (GET, POST и т.д.)
            endpoint: путь API (например '/sorts/123/')
            **kwargs: дополнительные параметры для requests
            
        Returns:
            dict или None: JSON ответ или None при ошибке
        """
        url = f"{self.api_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)
        
        # Добавляем заголовки с токеном
        headers = self._get_headers(kwargs.pop('headers', None))
        kwargs['headers'] = headers
        
        try:
            response = requests.request(method, url, **kwargs)
            
            # Если получили 401, пробуем обновить токен и повторить
            if response.status_code == 401 and self.service_username:
                logger.info("Токен устарел, получаем новый...")
                self._token = None  # Сбрасываем старый токен
                headers = self._get_headers()
                kwargs['headers'] = headers
                response = requests.request(method, url, **kwargs)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Patents Service ({url}): {e}")
            return None
    
    def get_sort(self, sort_id):
        """
        Получить полную информацию о сорте
        
        Args:
            sort_id: ID сорта в Patents Service
            
        Returns:
            dict или None: Данные сорта
            
        Example:
            {
                "id": 456,
                "name": "Пшеница Акмола 3",
                "culture": {
                    "id": 1,
                    "name": "Пшеница яровая"
                },
                ...
            }
        """
        return self._make_request('GET', f'/sorts/{sort_id}/')
    
    def sort_exists(self, sort_id):
        """
        Проверить существует ли сорт
        
        Args:
            sort_id: ID сорта
            
        Returns:
            bool: True если сорт существует и доступен
        """
        sort_data = self.get_sort(sort_id)
        return sort_data is not None
    
    def get_sort_name(self, sort_id):
        """
        Получить название сорта
        
        Args:
            sort_id: ID сорта
            
        Returns:
            str или None: Название сорта
        """
        sort_data = self.get_sort(sort_id)
        return sort_data.get('name') if sort_data else None
    
    def get_culture(self, culture_id):
        """
        Получить полную информацию о культуре
        
        Args:
            culture_id: ID культуры
            
        Returns:
            dict или None: Данные культуры включая группу культуры
            {
                "id": 1,
                "name": "Пшеница яровая",
                "group_culture": {
                    "id": 1,
                    "name": "Зерновые"
                }
            }
        """
        return self._make_request('GET', f'/cultures/{culture_id}/')
    
    def get_culture_name(self, culture_id):
        """
        Получить только название культуры
        
        Args:
            culture_id: ID культуры
            
        Returns:
            str или None: Название культуры
        """
        culture_data = self.get_culture(culture_id)
        return culture_data.get('name') if culture_data else None
    
    def get_all_cultures(self, params=None):
        """
        Получить список всех культур из Patents Service
        
        Обрабатывает пагинацию и возвращает ВСЕ культуры.
        Поддерживает фильтрацию по группе культур и поиск по названию.
        
        Args:
            params: Параметры фильтрации (dict)
                - group: ID группы культур (основной параметр)
                - group_culture_id: алиас для group (для обратной совместимости)
                - culture_group: алиас для group (для обратной совместимости)
                - search: поиск по названию культуры
            
        Returns:
            list: Список культур с группами культур
        """
        # Преобразуем параметры фильтрации в формат Patents Service
        if params:
            # Если передан group_culture_id или culture_group, преобразуем в group
            if 'group_culture_id' in params and 'group' not in params:
                params = params.copy()
                params['group'] = params.pop('group_culture_id')
            elif 'culture_group' in params and 'group' not in params:
                params = params.copy()
                params['group'] = params.pop('culture_group')
        endpoints_to_try = [
            '/cultures/',      # endpoint с пагинацией
            '/cultures/all/',  # endpoint без пагинации (если есть)
        ]
        
        for endpoint in endpoints_to_try:
            data = self._make_request('GET', endpoint, params=params)
            if data is not None:
                if isinstance(data, list):
                    return data
                
                if isinstance(data, dict) and 'results' in data:
                    all_results = list(data.get('results', []))
                    next_url = data.get('next')
                    page = 2
                    
                    while next_url:
                        page_data = self._make_request('GET', endpoint, params={'page': page})
                        if page_data and isinstance(page_data, dict):
                            all_results.extend(page_data.get('results', []))
                            next_url = page_data.get('next')
                            page += 1
                        else:
                            break
                    
                    logger.info(f'Загружено {len(all_results)} культур')
                    return all_results
        
        logger.warning("Не удалось получить список культур")
        return []
    
    def get_all_group_cultures(self, params=None):
        """
        Получить список всех групп культур из Patents Service
        
        Обрабатывает пагинацию и возвращает ВСЕ группы культур.
        
        Args:
            params: Параметры фильтрации (dict)
            
        Returns:
            list: Список групп культур
        """
        endpoints_to_try = [
            '/group-cultures/',      # endpoint с пагинацией
            '/group-cultures/all/',  # endpoint без пагинации (если есть)
        ]
        
        for endpoint in endpoints_to_try:
            data = self._make_request('GET', endpoint, params=params)
            if data is not None:
                if isinstance(data, list):
                    return data
                
                if isinstance(data, dict) and 'results' in data:
                    all_results = list(data.get('results', []))
                    next_url = data.get('next')
                    page = 2
                    
                    while next_url:
                        page_data = self._make_request('GET', endpoint, params={'page': page})
                        if page_data and isinstance(page_data, dict):
                            all_results.extend(page_data.get('results', []))
                            next_url = page_data.get('next')
                            page += 1
                        else:
                            break
                    
                    logger.info(f'Загружено {len(all_results)} групп культур')
                    return all_results
        
        logger.warning("Не удалось получить список групп культур")
        return []
    
    def get_all_originators(self, params=None):
        """
        Получить список всех оригинаторов из Patents Service
        
        Обрабатывает пагинацию и возвращает ВСЕХ оригинаторов.
        
        Args:
            params: Параметры фильтрации (dict)
            
        Returns:
            list: Список оригинаторов
        """
        endpoints_to_try = [
            '/ariginators/',      # endpoint с пагинацией (основное написание в Patents)
            '/originators/',      # альтернативное написание
            '/originators/all/',  # без пагинации (если есть)
        ]
        
        for endpoint in endpoints_to_try:
            data = self._make_request('GET', endpoint, params=params)
            if data is not None:
                if isinstance(data, list):
                    return data
                
                if isinstance(data, dict) and 'results' in data:
                    all_results = list(data.get('results', []))
                    next_url = data.get('next')
                    page = 2
                    
                    while next_url:
                        logger.info(f'Загрузка страницы {page} оригинаторов...')
                        page_data = self._make_request('GET', endpoint, params={'page': page})
                        if page_data and isinstance(page_data, dict):
                            all_results.extend(page_data.get('results', []))
                            next_url = page_data.get('next')
                            page += 1
                        else:
                            break
                    
                    logger.info(f'Загружено всего {len(all_results)} оригинаторов из {data.get("count", "?")} доступных')
                    return all_results
        
        logger.warning("Не удалось получить список оригинаторов")
        return []
    
    def get_originator(self, originator_id):
        """
        Получить информацию об оригинаторе
        
        Args:
            originator_id: ID оригинатора
            
        Returns:
            dict или None: Данные оригинатора
        """
        endpoints_to_try = [
            f'/originators/{originator_id}/',
            f'/ariginators/{originator_id}/',
        ]
        
        for endpoint in endpoints_to_try:
            data = self._make_request('GET', endpoint)
            if data is not None:
                return data
        
        return None
    
    def create_originator(self, originator_data):
        """
        Создать нового оригинатора в Patents Service
        
        Args:
            originator_data: dict с данными оригинатора
            {
                "name": "Название оригинатора"
            }
            
        Returns:
            dict или None: Созданный оригинатор
        """
        # Пробуем разные варианты endpoint
        result = self._make_request('POST', '/originators/', json=originator_data)
        if result is None:
            result = self._make_request('POST', '/ariginators/', json=originator_data)
        return result
    
    def create_culture(self, culture_data):
        """
        Создать новую культуру в Patents Service
        
        Args:
            culture_data: dict с данными культуры
            {
                "name": "Новая культура",
                "group_culture": 1,
                "description": "..."
            }
            
        Returns:
            dict или None: Созданная культура
        """
        return self._make_request('POST', '/cultures/', json=culture_data)
    
    def update_culture(self, culture_id, culture_data):
        """
        Обновить культуру в Patents Service
        
        Args:
            culture_id: ID культуры
            culture_data: dict с обновленными данными
            
        Returns:
            dict или None: Обновленная культура
        """
        return self._make_request('PUT', f'/cultures/{culture_id}/', json=culture_data)
    
    def create_group_culture(self, group_data):
        """
        Создать новую группу культур в Patents Service
        
        Args:
            group_data: dict с данными группы
            {
                "name": "Новая группа",
                "description": "..."
            }
            
        Returns:
            dict или None: Созданная группа культур
        """
        return self._make_request('POST', '/group-cultures/', json=group_data)
    
    def get_all_sorts(self, params=None):
        """
        Получить список всех сортов (для справочников)
        
        Обрабатывает пагинацию и возвращает ВСЕ сорта из Patents Service.
        
        Args:
            params: Параметры фильтрации (dict)
            
        Returns:
            list: Список ВСЕХ сортов
        """
        # Пробуем разные варианты endpoint
        endpoints_to_try = [
            '/sorts/',          # v2 endpoint с пагинацией
            '/sorts/all/',      # v2 endpoint без пагинации (если есть)
        ]
        
        for endpoint in endpoints_to_try:
            data = self._make_request('GET', endpoint, params=params)
            if data is not None:
                # Если это список - вернуть как есть
                if isinstance(data, list):
                    return data
                
                # Если это dict с пагинацией - собрать все страницы
                if isinstance(data, dict) and 'results' in data:
                    all_results = []
                    all_results.extend(data.get('results', []))
                    
                    # Проходим по всем страницам
                    next_url = data.get('next')
                    page = 2
                    
                    while next_url:
                        logger.info(f'Загрузка страницы {page}...')
                        # Запрос следующей страницы
                        page_data = self._make_request('GET', endpoint, params={'page': page})
                        
                        if page_data and isinstance(page_data, dict):
                            all_results.extend(page_data.get('results', []))
                            next_url = page_data.get('next')
                            page += 1
                        else:
                            break
                    
                    logger.info(f'Загружено всего {len(all_results)} сортов из {data.get("count", "?")} доступных')
                    return all_results
        
        logger.warning("Не удалось получить список сортов ни с одного endpoint")
        return []
    
    def create_sort(self, sort_data):
        """
        Создать новый сорт в Patents Service
        
        Args:
            sort_data: dict с данными сорта
            {
                "name": "Название сорта",
                "code": "371/06",
                "culture": 1,
                "originators": [1, 2]
            }
            
        Returns:
            dict или None: Созданный сорт
        """
        return self._make_request('POST', '/sorts/', json=sort_data)
    
    def validate_sort_for_trial(self, sort_id):
        """
        Валидировать сорт для создания испытания
        
        Получает данные сорта и возвращает информацию для денормализации.
        Культуры НЕ денормализуются - получаются из Patents API при необходимости.
        
        Args:
            sort_id: ID сорта
            
        Returns:
            dict или None: Данные для сохранения в Trials
            {
                'sort_id': 456,
                'sort_name': 'Пшеница Акмола 3',
                'culture': {  // Полные данные культуры для фронтенда
                    'id': 1,
                    'name': 'Пшеница яровая'
                }
            }
        """
        sort_data = self.get_sort(sort_id)
        if not sort_data:
            return None
        
        return {
            'sort_id': sort_data.get('id'),
            'sort_name': sort_data.get('name'),
            'culture': sort_data.get('culture')  # Вся информация о культуре
        }


# Singleton экземпляр для использования в коде
patents_api = PatentsServiceClient()
