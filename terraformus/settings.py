import os
from pathlib import Path
from decouple import config, Csv
from dj_database_url import parse as dburl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

AUTH_USER_MODEL = 'core.User'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# SSL config
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='*', cast=Csv())
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST', default=True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'ALLOWALL'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=1025, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
RECIPIENT_ADDRESS = config('RECIPIENT_ADDRESS', default='admin@example.com')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'terraformus.core',
    'django.contrib.humanize',
    'django_recaptcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'debug_toolbar',
    # 'rest_framework',
]


# Humanize django contrib

# THOUSAND_SEPARATOR = '.'


# Allauth configurations

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {'signup': 'terraformus.core.forms.CustomSignupForm',
                 'reset_password': 'terraformus.core.forms.CustomResetPasswordForm'}

# django-recaptcha

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'terraformus.urls'

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

WSGI_APPLICATION = 'terraformus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}

if config('DATABASE_URL', default=''):
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    "show_ui_builder": True,

    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "terraformus",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "terraformus",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "terraformus Admin",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "img/logo/terraformus-logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "",

    # Welcome text on the login screen
    "welcome_sign": "",

    # Copyright on the footer
    "copyright": "terraformus",

    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "auth.User",

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Terraformus Website",  "url": "home"},
    ],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "core.User",
        "core.HomePageControl",
        "core.Solution",
        "core.Strategy",
        "core.ExternalAsset",
        "core.LifeCycle",
        "core.LifeCycleInput",
        "core.LifeCycleWaste",
        "core.StrategySolution",
        "core.Profile",
        "core.Report",
    ],

    # Use modals instead of popups
    "related_modal_active": False,

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}
