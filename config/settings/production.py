import dj_database_url
import django_heroku

from .base import *
from .base import BASE_DIR, DATABASES

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost']

DATABASES['default'] = dj_database_url.config(conn_max_age=300, ssl_require=True)

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

# Security
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
