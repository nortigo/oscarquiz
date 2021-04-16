import os
from environs import Env
from pathlib import Path

env = Env()
env.read_env()


# -----------------------------------------------------------------
# General settings
# -----------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# -----------------------------------------------------------------
# Applications
# -----------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Vendors
    'rest_framework',
    'rest_framework.authtoken',

    # Apps
    'oscarquiz',
]


# -----------------------------------------------------------------
# Middlewares
# -----------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------------------------------------------
# Templates
# -----------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -----------------------------------------------------------------
# Database
# -----------------------------------------------------------------
DATABASES = {
    'default': env.dj_db_url('DATABASE_URL'),
}


# -----------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# -----------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------
LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = False
USE_L10N = False
USE_TZ = False


# -----------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# -----------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '_static'
STATICFILES_DIRS = (
    str(BASE_DIR / 'static'),
)
