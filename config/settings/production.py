import dj_database_url
import django_heroku

from .base import *
from .base import BASE_DIR, DATABASES

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get("DEBUG", default=0))
# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with ',' between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="127.0.0.1,0.0.0.0,localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", default="*").split(",")

DATABASES['default'] = dj_database_url.config(conn_max_age=300, ssl_require=True)

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Security
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
