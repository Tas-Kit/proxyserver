import os
from proxyserver.settings.basic import *

setting_path = 'proxyserver/settings/'
DEBUG = False
JWT_AUTH['JWT_PUBLIC_KEY'] = open(setting_path + 'staging.key.pub').read()
SECRET_KEY = os.environ['SECRET_KEY']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# INSTALLED_APPS.append('djangosecure')
# INSTALLED_APPS.append('sslserver')
# MIDDLEWARE.append('djangosecure.middleware.SecurityMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'HOST': 'psqldb',
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'PORT': 5432,
    }
}

URLS = {
    'webfront': 'http://webfront:8000/',
    'webmain': 'http://webmain:3000/',
    'authserver': 'http://authserver:8000/',
    'taskservice': 'http://taskservice:8000/',
    'base': 'https://localhost:10003/'
}
