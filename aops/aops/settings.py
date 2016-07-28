#coding=utf-8
"""
Django settings for aops project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

import djcelery

from options import GLOBAL_OPTIONS

djcelery.setup_loader()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# sys.path.insert(0, os.path.join(BASE_DIR, 'libs'))





# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e4@o6=&)u7b--a1w!ekm3qq%k276q^g2zm&c9-r@7w2hq#x&0q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = ( 'templates/',)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'djcelery',
    'cmdb',
    'account',
    'export',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aops.urls'

WSGI_APPLICATION = 'aops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

SQLITE_DB_PATH = os.path.join(BASE_DIR, 'db')



DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(SQLITE_DB_PATH, 'db.sqlite3'),
  }
}



HAYSTACK_CONNECTIONS = {
    'default': {
#        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join('%s/indexes' % (BASE_DIR), 'whoosh_index'),
    },
}

#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ('static/',)

LANGUAGES = (('en-us', u'English'),('zh-cn', u'简体中文'), ('zh-tw', u'繁體中文'))

if DEBUG:
    SESSION_COOKIE_AGE = 60*60*24  # 24小时
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
else:
    SESSION_COOKIE_AGE = 60 * 60 * 2  # 2小时
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True  #


# 声明变量
GB_OP = GLOBAL_OPTIONS(trans_type='lazy')

for option in GB_OP.OPTIONS:
    exec('%s = GB_OP.get_option("%s")' % (option, option))


SALT_SP_KEY = 'salt.spunkmars.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s : %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d : %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': BASE_DIR + '/logs/sys.log',
            'mode': 'a',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# BROKER_HOST = "redis.spunkmars.com"
#BROKER_BACKEND = "redis"
# REDIS_PORT = 6379
# REDIS_HOST = "localhost"
# BROKER_USER = ""
# BROKER_PASSWORD = ""
# BROKER_VHOST = "0"
# REDIS_DB = 0
# REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
#CELERY_RESULT_BACKEND = 'redis'
#CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
#CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TIMEZONE = TIME_ZONE

BROKER_URL = 'redis://redis.spunkmars.com:6379'
CELERY_RESULT_BACKEND = 'redis://redis.spunkmars.com:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False

