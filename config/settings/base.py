# config/settings/base.py

from pathlib import Path
import environ
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Import our modular logging configuration function
from config.logging_config import get_base_logging_config

# Environment setup
env = environ.Env()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Core Django settings
# DJANGO_SECRET_KEY, DEBUG, ALLOWED_HOSTS will be loaded by .env.dev/.env.prod
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False) # Default to False, will be True in dev
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "drf_spectacular",

    # Local apps
    "apps.example_calculator_app",
    "apps.example_greeter_app",
]

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Add default authentication/permission classes for security
    # "DEFAULT_AUTHENTICATION_CLASSES": [
    #     "rest_framework.authentication.SessionAuthentication",
    #     "rest_framework.authentication.TokenAuthentication",
    # ],
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.IsAuthenticated",
    # ],
}

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.RequestLoggingMiddleware", # Our custom middleware
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles" # Use 'staticfiles' as recommended for collectstatic
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Sentry Configuration (initialized here, logging setup comes later)
SENTRY_DSN = env("SENTRY_DSN", default="") # Get DSN, default to empty string if not set
SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT", default="development")
SENTRY_RELEASE = env("SENTRY_RELEASE", default="local") # Use a default like 'local' for development

if SENTRY_DSN: # Only initialize Sentry if DSN is provided
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(
                transaction_style='url', # Or 'function_name'
                middleware_spans=True,
                signals_spans=True,
                cache_spans=False,
            ),
        ],
        # Set traces_sample_rate and profiles_sample_rate
        # We recommend adjusting these values in production.
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=1.0),
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE", default=1.0),

        environment=SENTRY_ENVIRONMENT,
        send_default_pii=env.bool("SENTRY_SEND_DEFAULT_PII", default=False), # Be careful with PII
        release=SENTRY_RELEASE,
        # Filter out noisy internal frames from your stack traces
        in_app_include=[
            'apps', # Include your 'apps' directory in 'in_app' frames
            'config', # Include your 'config' directory
        ],
        in_app_exclude=[
            'venv', 'site-packages', 'django', 'gunicorn', # Exclude common library paths
        ],
    )
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Sentry SDK initialized for environment: {SENTRY_ENVIRONMENT}, release: {SENTRY_RELEASE}")

# Apply logging configuration from our function
# The Sentry handler will be automatically included if SENTRY_DSN is present.
LOGGING = get_base_logging_config(
    debug_mode=DEBUG,
    sentry_dsn=SENTRY_DSN,
    sentry_environment=SENTRY_ENVIRONMENT,
)

# Email for mail_admins
ADMINS = [('Your Name', 'your_email@example.com')] # Define admins for mail_admins handler
MANAGERS = ADMINS