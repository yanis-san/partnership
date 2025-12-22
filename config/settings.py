import environ
import os
from pathlib import Path

# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_ROBOTS=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
    SESSION_COOKIE_HTTPONLY=(bool, True),
    CSRF_COOKIE_HTTPONLY=(bool, True),
    SECURE_BROWSER_XSS_FILTER=(bool, True),
)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Read from .env file in project root
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# ============================================
# DJANGO CORE SETTINGS
# ============================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-1l&-s-h96u@6c^-@^_-vyi#5!0bg+s+^)(pqbdi!&qy7a#g8t+",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

# Comma-separated list of allowed hosts
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"]
)


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "partnerships",
    "students",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise pour les statiques
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Supports DATABASE_URL env variable for PostgreSQL, SQLite, MySQL, etc.

DATABASES = {"default": env.db(default="sqlite:///db.sqlite3")}

# Connection pooling settings
DATABASES["default"]["CONN_MAX_AGE"] = 600
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE", default="fr-fr")
TIME_ZONE = env("TIME_ZONE", default="Africa/Algiers")
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://whitenoise.readthedocs.io/

STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = BASE_DIR / env("STATIC_ROOT", default="staticfiles")

# WhiteNoise Configuration - STORAGES dict (Django 4.2+)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files (User Uploads)
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = BASE_DIR / env("MEDIA_ROOT", default="media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email Configuration
# https://docs.djangoproject.com/en/5.2/topics/email/

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default="noreply@instituttorii.com"
)
SERVER_EMAIL = env("SERVER_EMAIL", default="server@instituttorii.com")

# Admin notifications
ADMINS = env.list("ADMINS", default=["Admin <admin@instituttorii.com>"])
# Convert string format to tuple format
ADMINS = [
    tuple(admin.split("<")) if "<" in admin else (admin, "")
    for admin in ADMINS
]
ADMINS = [(name.strip(), email.strip(">")) for name, email in ADMINS]

MANAGERS = env.list("MANAGERS", default=[])
MANAGERS = [
    tuple(mgr.split("<")) if "<" in mgr else (mgr, "") for mgr in MANAGERS
]
MANAGERS = [(name.strip(), email.strip(">")) for name, email in MANAGERS]


# Security Settings
# https://docs.djangoproject.com/en/5.2/topics/security/

# HTTPS/SSL
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE")

# Cookies security
SESSION_COOKIE_HTTPONLY = env("SESSION_COOKIE_HTTPONLY")
CSRF_COOKIE_HTTPONLY = env("CSRF_COOKIE_HTTPONLY")
SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", default="Lax")
CSRF_COOKIE_SAMESITE = env("CSRF_COOKIE_SAMESITE", default="Lax")
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE", default=86400)

# Browser security headers
SECURE_BROWSER_XSS_FILTER = env("SECURE_BROWSER_XSS_FILTER")
X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", default="DENY")

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False
)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", default=False)

# CSP (Content Security Policy)
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    "style-src": ("'self'", "'unsafe-inline'"),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "data:", "cdn.jsdelivr.net"),
}

# Enable production security settings when DEBUG=False
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
# ============================================
# LOGGING
# ============================================

LOG_LEVEL = env("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}

# ============================================
# OPTIONAL: THIRD-PARTY SERVICES
# ============================================

# Sentry (Error tracking)
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# Redis Cache (optional)
REDIS_URL = env("REDIS_URL", default="")
if REDIS_URL:
    CACHES = {"default": env.cache_url("REDIS_URL")}

# ============================================
# WHITENOISE SETTINGS
# ============================================

WHITENOISE_COMPRESS = env("WHITENOISE_COMPRESS", default=True)
WHITENOISE_AUTOREFRESH = env("WHITENOISE_AUTOREFRESH", default=DEBUG)
WHITENOISE_MAX_AGE = env.int("WHITENOISE_MAX_AGE", default=31536000)

# ============================================
# ADMIN URL (SÉCURITÉ)
# ============================================

ADMIN_URL = env("ADMIN_URL", default="admin/")

# ============================================
# ROBOTS.TXT
# ============================================

ALLOW_ROBOTS = env("ALLOW_ROBOTS")
