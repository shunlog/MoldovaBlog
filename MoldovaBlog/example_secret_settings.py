from pathlib import Path

# added here cause we need it here as well
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%p1um^13h%sh5b7v$3qh=mbx$9a9d*_y9yy)-xt$q+m&7a&v9o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'visitmoldova2023@gmail.com'
EMAIL_HOST_PASSWORD = 'xime ulub ewub fgqd'
EMAIL_USE_TLS = True

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATIC_ROOT = '/var/www/MoldovaBlog/static/'
MEDIA_ROOT = '/var/www/MoldovaBlog/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_HSTS_SECONDS = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
