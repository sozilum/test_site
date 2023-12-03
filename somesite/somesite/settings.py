"""
Django settings for somesite project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from pathlib import Path
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#Задание базовой дерриктории для базы данных
# DATABASE_DIR = BASE_DIR / "database"
#Если папка существует не будет ошибки
# DATABASE_DIR.mkdir(exist_ok=True)


import sentry_sdk

sentry_sdk.init(
    dsn="https://571f3f028731a09001b7e2b341db5b0c@o4505920631537664.ingest.sentry.io/4505920640057344",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x60_dzrn=ma(+njiqg!t!8_+pm3&wtkp^9-j-4d=b*h&#v6i$('


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 1

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1'
]# + getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

INTERNAL_IPS =[
    '127.0.0.1'
]

# if DEBUG:
#     import socket
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS.append('10.0.2.2')
#     INTERNAL_IPS.extend(
#         [ip[: ip.rfind('.')] + '.1' for ip in ips]
#     )


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    
    'debug_toolbar',
    'rest_framework',
    'django_filters',
    # 'drf_spectacular',

    'shopapp.apps.ShopappConfig',
    'requestdataapp.apps.RequestdataappConfig',
    'myauthapp.apps.MyauthConfig',
    'myapiapp.apps.MyapiappConfig',
    'BlogApp.apps.BlogappConfig',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'requestdataapp.middlwares.set_useragent_on_requset_middlware',
    'requestdataapp.middlwares.CountRequestsMiddlwate',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    # 'requestdataapp.middlwares.throttling_middlware', Закомичено так-как срабатывает при перенаправлениях 
]

ROOT_URLCONF = 'somesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'templates'],
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

WSGI_APPLICATION = 'somesite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': DATABASE_DIR / 'db.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.dummy.DummyCache'
        # 'BACKEND':'django.core.cache.backends.filebased.FileBasedCache',
        # 'LOCATION':'/var/tmp/django_cache',
    },
}

CACHE_MIDDLEWARE_SECONDS = 200#Вермя сохранения кеша


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

#Здесь указываеться язык поумолчанию если язык для перевода не был найден
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True

LOCALE_PATHS = [
    BASE_DIR / 'locale/'
]

LANGUAGES = [
    ('en', _('Engilsh')),
    ('ru', _('Russian'))
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy('authapp:users_list')
LOGIN_URL = reverse_lazy('authapp:login')

# # Простое логирование 
# LOGLEVEL = getenv("DJANGO_LOGLEVEL", "info").upper()
# logging.config.dictConfig({
#     "version":1,
#     "disable_existing_loggers":False,
#     "formatters":{
#         "console":{
#             "format":"%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(message)s",
#         },
#     },
#     "handlers":{
#         "console":{
#             "class": "logging.StreamHandler",
#             "formatter": "console",
#         },
#     },
#     "loggers":{
#         "":{
#             "level":LOGLEVEL,
#             "handlers":[
#                 "console",
#             ],
#         },
#     },
# })


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS':[
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS ={
    'TITLE':'My site Project API',
    'DESCRIPTION':'My site with shop app and custom auth',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

LOGFILE_NAME = BASE_DIR / 'log.txt'
LOGFILE_SIZE = 5 * 1024 * 1024
LOGFILE_COUNT = 3

LOGGING = {
    'version':1,
    'disable_existing_loggers':False,
    'formatters':{
        'verbose':{
            'format':'%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers':{
        'console':{
            'class':'logging.StreamHandler',
            'formatter':'verbose',
        },
        'logfile':{
            #Для ротации по датам/дням
            # 'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':LOGFILE_NAME,
            'maxBytes':LOGFILE_SIZE,
            'backupCount':LOGFILE_COUNT,
            'formatter':'verbose',
        },
    },
    'root':{
        'handlers':[
            'console',
            'logfile',
        ],
        'level':'INFO',
    }
}

#Конфигурация для sql запросов
# LOGGING = {
#     'version':1,
#     'filters':{
#         'require_debug_true':{
#             '()':'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers':{
#         'console':{
#             'level':'DEBUG',
#             'filters':['require_debug_true'],
#             'class':'logging.StreamHandler',
#         }
#     },
#     'loggers':{
#         'django.db.backends':{
#             'level':'DEBUG',
#             'handlers':['console'],
#         }
#     }
# }