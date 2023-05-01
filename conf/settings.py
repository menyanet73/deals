import os
from envparse import env
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'p8ce#s#g7h^4j$zdbtdoc1d!=9mc7*z5yj$(vx+q=+a=25f!-w'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

PREINSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
]

PROJECT_APPS = [
    'apps.deals'
]

INSTALLED_APPS = PREINSTALLED_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

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

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME', default='default_name'),
        'USER': env('POSTGRES_USER', default='default_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='default_password'),
        'HOST': env('POSTGRES_HOST', default='db'),
        'PORT': env('POSTGRES_PORT', default='5432')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

DEFAULT_ADMIN_LOGIN = env('DEFAULT_ADMIN_LOGIN', default='admin')
DEFAULT_ADMIN_EMAIL = env('DEFAULT_ADMIN_EMAIL', default='admin@some.email')
DEFAULT_ADMIN_PASSWORD = env('DEFAULT_ADMIN_PASSWORD', default='admin')

CHECK_DUPLICATES = env('CHECK_DUPLICATES', cast=bool, default=False)