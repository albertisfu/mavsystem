"""
Django settings for mavalpa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = []

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL = '/login/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'almacen.apps.AlmacenConfig',
    'produccion.apps.ProduccionConfig',
    'django.contrib.humanize',
    'selectize',
    'panel',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_LOADERS =['django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader']



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             BASE_DIR + '/templates/',
             BASE_DIR + 'almacen/templates/',
             BASE_DIR + '/almacen/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'almacen.context_processors.usuario',
            ],
        },
    },
]



ROOT_URLCONF = 'mavalpa.urls'

WSGI_APPLICATION = 'mavalpa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mavsystem',
#         'USER': 'xxxxx',
#         'PASSWORD': 'xxxxx*',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

#MEDIA_ROOT = BASE_DIR
MEDIA_ROOT = os.path.join(BASE_DIR, 'site_media', 'media')
MEDIA_URL = '/site_media/media/'
SITE_MEDIA_URL = '/site_media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'site_media', 'static')
STATIC_URL = '/site_media/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'files'),

)

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'xxxxx'
EMAIL_HOST_PASSWORD = 'xxxxx'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


#IVA
IVA = 0.16

