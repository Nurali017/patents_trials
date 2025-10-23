import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'trials-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = ['*']

# Настройки для работы за HTTPS прокси
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Не перенаправлять, так как nginx уже обрабатывает HTTPS
USE_TLS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'django_filters',
    'corsheaders',
    
    # Независимый микросервис - используем стандартные модели Django
    'trials_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Раздача статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trials.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trials.wsgi.application'

# НАСТРОЙКИ БД - ОТДЕЛЬНАЯ БД ДЛЯ TRIALS SERVICE
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('SQL_DATABASE', 'trials_db'),  # Своя отдельная БД!
        'USER': os.environ.get('SQL_USER', 'admin'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'qwe1daSjewspds12'),
        'HOST': os.environ.get('SQL_HOST', 'trials-db'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}

# Используем стандартную модель Django User (независимый микросервис)
# AUTH_USER_MODEL по умолчанию 'auth.User'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Для Swagger
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Временно для разработки
    ],
}

# CORS - разрешаем оба фронтенда
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular trials frontend
    "http://localhost:3000",  # React trials frontend
    "http://localhost:3001",  # React trials frontend (альтернативный порт)
    "http://localhost:4201",  # Angular patents frontend (если другой порт)
]

CORS_ALLOW_CREDENTIALS = True

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,  # Отключить session auth для Swagger
    'LOGIN_URL': None,  # Отключить редирект на логин
    'LOGOUT_URL': None,
}

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Отключить редирект на логин для Swagger (режим разработки)
LOGIN_URL = None
LOGOUT_URL = None

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration для правильной раздачи статики
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
