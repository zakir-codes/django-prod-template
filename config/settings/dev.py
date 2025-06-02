from .base import *
import environ
import os

# Load development .env file
# Ensure this file is present in your project root or where docker-compose expects it
environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

# DEBUG is already handled by env.bool("DEBUG") in base.py.
# No need to explicitly set DEBUG = True here if .env.dev sets DEBUG=True.

# Database: PostgreSQL via Docker Compose
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST", default="localhost"), # Default to localhost for direct dev runs
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

# Email for development (console backend is usually best)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # Use console backend for development

# If you use the SMTP backend for dev, load these
# EMAIL_HOST = env("EMAIL_HOST", default="localhost")
# EMAIL_PORT = env.int("EMAIL_PORT", default=1025)
# EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
# EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# Django Debug Toolbar (Optional but highly recommended for dev)
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]