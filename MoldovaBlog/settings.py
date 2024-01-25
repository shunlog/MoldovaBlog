from .secret_settings import \
    (BASE_DIR, SECRET_KEY, DEBUG, ALLOWED_HOSTS, EMAIL_BACKEND,
     EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
     EMAIL_USE_TLS, STATIC_URL, MEDIA_ROOT, MEDIA_URL, DATABASES,
     DEFAULT_AUTO_FIELD, STATIC_ROOT, SECURE_HSTS_SECONDS, SECURE_SSL_REDIRECT,
     SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
from .validators import PasswordLengthValidator


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EET'
USE_I18N = True
USE_TZ = True
LOGIN_REDIRECT_URL = 'blog:index'
LOGOUT_REDIRECT_URL = 'blog:index'
ROOT_URLCONF = 'MoldovaBlog.urls'
WSGI_APPLICATION = 'MoldovaBlog.wsgi.application'

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
]

# WHY is this not the default?
# needed to make default form templates work,
# so we can override them
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "MoldovaBlog.validators.PasswordLengthValidator", "OPTIONS": {
        "min_length": 12,
        "max_length": 128
    }},
]
