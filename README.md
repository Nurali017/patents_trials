# 🌾 Trials Service - Микросервис управления испытаниями

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

Независимый микросервис для управления полным жизненным циклом испытаний сортов на хозяйственную полезность.

## 🎯 Назначение

**Trials Service** — это автономный микросервис, который управляет:
- 📊 Планированием полевых испытаний
- 📈 Сбором и хранением результатов измерений
- 📋 Протоколами испытаний
- 🗂️ Справочниками (показатели, регионы)

## 🏗️ Архитектура

### Принципы микросервисной архитектуры

- ✅ **Полная автономность**: Собственная кодовая база и отдельная БД
- ✅ **Независимое развертывание**: Можно запускать отдельно от других сервисов
- ✅ **Интеграция через API**: Взаимодействие с Patents Service только через HTTP API
- ✅ **Разделение ответственности**: Мастер-система для всего, что касается испытаний

### Взаимодействие сервисов

```
┌──────────────────┐       API V2      ┌──────────────────┐
│ Trials Service   │ ◄───────────────  │ Patents Service  │
│  (port 8001)     │   Запросы данных  │  (port 8000)     │
│                  │   о сортах        │                  │
└────────┬─────────┘                   └────────┬─────────┘
         │                                      │
         ▼                                      ▼
┌──────────────────┐                   ┌──────────────────┐
│   trials_db      │                   │    patent        │
│  PostgreSQL      │                   │   PostgreSQL     │
│   :5433          │                   │    :5432         │
└──────────────────┘                   └──────────────────┘
```

**Важно:** Нет прямых связей между БД! Только API интеграция.

## 📁 Структура проекта

```
trials/
├── trials/                  # Django проект
│   ├── settings.py         # Настройки (отдельная БД!)
│   ├── urls.py            # URL конфигурация
│   └── wsgi.py            # WSGI конфигурация
├── trials_app/            # Основное приложение
│   ├── models.py          # Модели (trials, results, indicators, regions)
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF сериализаторы
│   ├── patents_integration.py  # HTTP клиент для Patents API
│   └── management/        # Django команды
│       └── commands/
│           └── wait_for_db.py  # Ожидание готовности БД
├── utils/                 # Утилиты и миксины
├── docker-compose.yml     # Оркестрация (БД + Сервис)
├── Dockerfile            # Образ сервиса
├── start.sh              # Интерактивное меню запуска
├── start-db.sh           # Запуск только БД
├── start-service.sh      # Запуск только сервиса
├── stop.sh               # Остановка сервисов
├── status.sh             # Статус и мониторинг
├── requirements.txt      # Python зависимости
├── env.example           # Пример переменных окружения
├── QUICKSTART.md         # Подробное руководство
├── SERVICES_INTEGRATION.md  # Интеграция сервисов
├── CHEATSHEET.md         # Шпаргалка по командам
└── INTEGRATION_SUMMARY.md   # Бизнес-логика
```

## 🚀 Быстрый старт

### Вариант 1: Запустить всё вместе (рекомендуется)

```bash
# Интерактивное меню
./start.sh

# Или напрямую
docker-compose up -d
```

### Вариант 2: Раздельный запуск (БД и сервис отдельно)

```bash
# Шаг 1: Запустить БД
./start-db.sh

# Шаг 2: Запустить микросервис
./start-service.sh
```

### Вариант 3: Docker Compose команды

```bash
# Всё вместе
docker-compose up -d

# Только БД
docker-compose up -d trials-db

# Только сервис
docker-compose up -d trials-service
```

### Первоначальная настройка

Миграции применяются **автоматически** при запуске сервиса!

Если нужно создать суперпользователя:
```bash
docker exec -it trials_service python manage.py createsuperuser
```

## 🌐 Доступные сервисы

| Сервис | URL | Описание |
|--------|-----|----------|
| 🌐 API | http://localhost:8001/api/v1/ | REST API |
| 📚 Swagger | http://localhost:8001/swagger/ | API документация |
| ⚙️ Admin | http://localhost:8001/admin/ | Админ-панель Django |
| 🗄️ PostgreSQL | localhost:5433 | База данных trials_db |

## 📡 API Endpoints

### Испытания (Trials)
- `POST /api/v1/trials/` - Создать испытание
- `GET /api/v1/trials/` - Список испытаний (с фильтрацией)
- `GET /api/v1/trials/{id}/` - Детали испытания
- `PUT /api/v1/trials/{id}/` - Обновить испытание

### Результаты (Trial Results)
- `POST /api/v1/trials/{trial_id}/results/` - Добавить результаты
- `GET /api/v1/trials/{trial_id}/results/` - Получить результаты

### Справочники
- `GET, POST /api/v1/indicators/` - Показатели (урожайность, влажность и т.д.)
- `GET, POST /api/v1/regions/` - Регионы испытаний

### Интеграция с Patents Service

Trials Service **запрашивает** данные из Patents Service:
- `GET /api/v2/patents/sorts/all/` - Список сортов (для выбора)
- `GET /api/v2/patents/sorts/{id}/` - Детали сорта (валидация)

Patents Service **не знает** о Trials Service.

## 🔧 Конфигурация

### Environment переменные

```env
# Django
DEBUG=1
SECRET_KEY=trials-secret-key-change-in-production

# База данных (ОТДЕЛЬНАЯ!)
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=trials_db          # Своя БД, не patent!
SQL_USER=admin
SQL_PASSWORD=CHANGE_ME
SQL_HOST=trials-db              # Docker container name
SQL_PORT=5432                   # Внутренний порт (внешний 5433)

# Интеграция с Patents Service
PATENTS_SERVICE_URL=http://localhost:8000
```

### Порты

| Сервис | Внешний | Внутренний | Описание |
|--------|---------|------------|----------|
| Trials API | 8001 | 8001 | Django сервер |
| Trials DB | 5433 | 5432 | PostgreSQL |

**Почему 5433?** Чтобы не конфликтовать с Patents DB на порту 5432.

### База данных

**Своя отдельная БД `trials_db`:**
- ✅ `trials` - Испытания (хранит `sort_id` из Patents)
- ✅ `trial_results` - Результаты испытаний
- ✅ `indicators` - Показатели
- ✅ `regions` - Регионы

**НЕТ общих таблиц с Patents!**
Связь с сортами через:
- Хранение `sort_id`, `culture_id` (внешние ID)
- Денормализация (`sort_name`, `culture_name`)
- Валидация через API Patents Service

## 🛠️ Разработка

### Полезные команды

```bash
# Статус сервисов
./status.sh

# Логи
docker-compose logs -f                  # Все
docker-compose logs -f trials-service   # Только сервис

# Django shell
docker exec -it trials_service python manage.py shell

# Миграции
docker exec trials_service python manage.py makemigrations
docker exec trials_service python manage.py migrate

# Создать суперпользователя
docker exec -it trials_service python manage.py createsuperuser
```

### Подключение к БД

```bash
# Через Docker
docker exec -it trials_postgres psql -U admin -d trials_db

# Локальный клиент (если установлен psql)
psql postgresql://admin:CHANGE_ME@localhost:5433/trials_db
```

### Проверка работоспособности

```bash
# API доступен?
curl http://localhost:8001/api/v1/trials/

# БД готова?
docker exec trials_postgres pg_isready -U admin -d trials_db

# Patents Service доступен?
curl http://localhost:8000/api/v2/patents/sorts/all/
```

## 🔄 Интеграция с Patents Service

### Принцип работы

1. **Фронтенд запрашивает список сортов** → Patents Service API
2. **Пользователь выбирает сорт** → получает `sort_id`
3. **Создание испытания** → Trials Service с `sort_id`
4. **Trials валидирует sort_id** → запрос к Patents API
5. **Сохранение данных** → в свою БД `trials_db`

### Пример создания испытания

```bash
# 1. Получить список сортов (фронтенд)
curl http://localhost:8000/api/v2/patents/sorts/all/

# 2. Создать испытание (фронтенд → Trials)
curl -X POST http://localhost:8001/api/v1/trials/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Испытание пшеницы 2025",
    "year": 2025,
    "region_id": 10,
    "sort_id": 456
  }'

# 3. Trials валидирует (сервер-сервер)
# GET http://localhost:8000/api/v2/patents/sorts/456/
# Автоматически!
```

Подробнее: `SERVICES_INTEGRATION.md`

## 📚 Документация

- 📖 **QUICKSTART.md** - Подробное руководство по запуску
- 🔗 **SERVICES_INTEGRATION.md** - Интеграция с Patents Service
- ⚡ **CHEATSHEET.md** - Шпаргалка по командам
- 📋 **INTEGRATION_SUMMARY.md** - Бизнес-логика и процессы
- 🏗️ **ARCHITECTURE.md** - Архитектура системы

## ❓ FAQ

**Q: Можно ли запустить Trials без Patents Service?**  
A: Да, можно. Trials полностью автономен. Интеграция нужна только при создании испытаний с сортами.

**Q: Нужна ли общая БД?**  
A: Нет! Каждый сервис использует свою БД. Связь только через API.

**Q: Как избежать конфликта портов?**  
A: Trials использует порты 8001 (API) и 5433 (DB), Patents - 8000 и 5432.

**Q: Что если Patents Service недоступен?**  
A: Trials продолжит работать, но создание новых испытаний будет невозможно.

## 🆘 Поддержка

Если что-то не работает:
1. Проверьте статус: `./status.sh`
2. Посмотрите логи: `docker-compose logs -f`
3. Убедитесь что порты 5433 и 8001 свободны
4. Проверьте что Docker запущен

---

**Создан как независимый микросервис** 🎯
