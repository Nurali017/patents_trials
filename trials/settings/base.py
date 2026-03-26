import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = []

# Настройки для работы за HTTPS прокси
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
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
    'storages',

    'trials_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

CORS_ALLOW_CREDENTIALS = True

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1000,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': None,
    'LOGOUT_URL': None,
    'DEFAULT_AUTO_SCHEMA_CLASS': 'trials.swagger.NoFilterAutoSchema',
}

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TEST_NON_SERIALIZED_APPS = ['trials_app']

LOGIN_URL = None
LOGOUT_URL = None

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_BACKEND = os.environ.get('MEDIA_BACKEND', 'filesystem').strip().lower() or 'filesystem'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LEGACY_MEDIA_ROOT = os.environ.get('LEGACY_MEDIA_ROOT', MEDIA_ROOT)

MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'http://minio:9000')
MINIO_BUCKET = os.environ.get('MINIO_BUCKET', 'trials-media')
MINIO_REGION = os.environ.get('MINIO_REGION', 'us-east-1')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', '')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', '')
MINIO_PRESIGNED_URL_EXPIRY_SECONDS = int(
    os.environ.get('MINIO_PRESIGNED_URL_EXPIRY_SECONDS', '600')
)

if MEDIA_BACKEND == 'minio':
    DEFAULT_FILE_STORAGE = 'trials_app.storage.MinioMediaStorage'

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

# Пороговые значения для балльной оценки сортов
EVALUATION_THRESHOLDS = {
    'quality': {
        'protein_content': {
            'excellent': 15.0,
            'good': 13.0,
            'satisfactory': 11.0,
            'poor': 9.0
        },
        'gluten_content': {
            'excellent': 30.0,
            'good': 25.0,
            'satisfactory': 20.0,
            'poor': 15.0
        },
        'vitreousness': {
            'excellent': 90.0,
            'good': 80.0,
            'satisfactory': 70.0,
            'poor': 60.0
        },
        'thousand_seed_weight': {
            'excellent': 50.0,
            'good': 45.0,
            'satisfactory': 40.0,
            'poor': 35.0
        },
        'minimum_indicators': 2,
        'minimum_years_tested': 2,
    },
    'resistance': {
        'lodging_resistance': {
            'excellent': 5.0,
            'good': 4.0,
            'satisfactory': 3.0,
            'poor': 2.0,
            'critical': 3.0
        },
        'winter_hardiness': {
            'excellent': 5.0,
            'good': 4.0,
            'satisfactory': 3.0,
            'poor': 2.0,
            'critical': 3.0
        },
        'drought_resistance': {
            'excellent': 5.0,
            'good': 4.0,
            'satisfactory': 3.0,
            'poor': 2.0
        },
        'shattering_resistance': {
            'excellent': 5.0,
            'good': 4.0,
            'satisfactory': 3.0,
            'poor': 2.0
        },
        'sprouting_resistance': {
            'excellent': 5.0,
            'good': 4.0,
            'satisfactory': 3.0,
            'poor': 2.0
        },
        'minimum_indicators': 2,
        'minimum_years_tested': 2,
        'critical_indicators': ['lodging_resistance', 'winter_hardiness']
    },
    'yield': {
        'deviation_significant_positive': 8.0,
        'deviation_moderate_positive': 3.0,
        'deviation_moderate_negative': -3.0,
        'deviation_significant_negative': -8.0,
        'statistical_significance_threshold': 50.0,
    },
    'violations': {
        'critical_score_threshold': 2.0,
        'minimum_years_tested': 2,
        'minimum_coverage_percent': 40.0,
    }
}
