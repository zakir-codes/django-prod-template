from .base import *
import environ
import os
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging # For referencing logging.INFO/ERROR etc.

# Load production environment
# Ensure this file is present in your production environment or where docker-compose expects it
environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))

# DEBUG is already handled by env.bool("DEBUG") in base.py.
# No need to explicitly set DEBUG = False here if .env.prod sets DEBUG=False.

# Database: PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# Email backend for production (SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="webmaster@yourdomain.com")
SERVER_EMAIL = env("SERVER_EMAIL", default="errors@yourdomain.com") # Used by AdminEmailHandler

# Security best practices
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
# X_FRAME_OPTIONS is DEFAULTER TO 'DENY' by Django's ClickjackingMiddleware if not set.
# SECURE_BROWSER_XSS_FILTER = True # Deprecated since Django 3.1
# SECURE_CONTENT_TYPE_NOSNIFF = True # Default True since Django 1.9

# Static files storage for production (e.g., Whitenoise or cloud storage)
# You'll likely need to install 'whitenoise' if you use it: poetry add whitenoise
# INSTALLED_APPS += ['whitenoise.runserver_nostatic'] # Add before other apps for static serving in dev
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware') # Insert early
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Consider django-storages for cloud storage (S3, GCS, Azure Blob)

# Sentry Integration specific adjustments
# Sentry is already initialized in base.py.
# If you need to override `traces_sample_rate` or `profiles_sample_rate` for prod:
# SENTRY_TRACES_SAMPLE_RATE = env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.01) # e.g., 1% in prod
# SENTRY_PROFILES_SAMPLE_RATE = env.float("SENTRY_PROFILES_SAMPLE_RATE", default=0.01) # e.g., 1% in prod

# Adjust logging for production (leveraging the base function)
# The LOGGING dict is already generated in base.py by get_base_logging_config.
# You can further customize it here if needed, but it's often not necessary.
# Example: Ensure console handler uses JSON formatter for log aggregators
LOGGING['handlers']['console']['formatter'] = 'json'
LOGGING['handlers']['console']['level'] = 'INFO' # Keep console output concise
LOGGING['loggers']['django.request']['level'] = 'ERROR' # Only log request errors to console/sentry
# Ensure root logger is INFO or WARNING
LOGGING['loggers']['']['level'] = 'INFO'
LOGGING['loggers']['apps']['level'] = 'INFO'

# If you uncommented 'file' handler in logging_config.py, ensure its path is appropriate
# LOGGING['handlers']['file']['level'] = 'INFO'