# config/logging_config.py

import os
import sys
import logging # Import logging to reference levels

def get_base_logging_config(debug_mode=False, sentry_dsn=None, sentry_environment='development'):
    """
    Returns a base logging configuration dictionary.
    debug_mode: If True, sets console handler level to DEBUG.
    sentry_dsn: If provided, adds Sentry handler to appropriate loggers.
    sentry_environment: Passed to Sentry as the environment tag.
    """
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(pathname)s %(lineno)d %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO', # Default, will be overridden by debug_mode
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'formatter': 'verbose',
            },
            # 'file': { # Uncomment and configure if you need file logging
            #     'level': 'INFO',
            #     'class': 'logging.handlers.RotatingFileHandler',
            #     'filename': '/var/log/django/app.log', # Ensure this path is writable in your container
            #     'maxBytes': 1024*1024*5, # 5 MB
            #     'backupCount': 5,
            #     'formatter': 'json',
            # },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
                'propagate': False, # Important to prevent duplicate logs if root also logs to console
            },
            'django.request': {
                'handlers': ['console', 'mail_admins'],
                'level': 'WARNING', # WARNING for 4xx, ERROR for 5xx
                'propagate': False,
            },
            'django.server': { # For runserver messages
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            '': { # Root logger for your custom application logs
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            'apps': { # For all loggers under the 'apps' namespace
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            # Add specific loggers for Gunicorn if you want them to go through Django's system
            'gunicorn.access': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'gunicorn.error': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

    if debug_mode:
        # Increase verbosity for development
        LOGGING['handlers']['console']['level'] = 'DEBUG'
        LOGGING['loggers']['django']['level'] = 'DEBUG'
        LOGGING['loggers']['django.request']['level'] = 'DEBUG'
        LOGGING['loggers']['']['level'] = 'DEBUG'
        LOGGING['loggers']['apps']['level'] = 'DEBUG'
        LOGGING['loggers']['gunicorn.access']['level'] = 'DEBUG'
        LOGGING['loggers']['gunicorn.error']['level'] = 'DEBUG'
        # In development, you usually don't want emails for errors
        for logger_name in LOGGING['loggers']:
            if 'mail_admins' in LOGGING['loggers'][logger_name]['handlers']:
                LOGGING['loggers'][logger_name]['handlers'].remove('mail_admins')


    # Sentry handler is added here if DSN is provided, ensuring it's conditional
    if sentry_dsn:
        LOGGING['handlers']['sentry'] = {
            'level': 'ERROR', # Only send ERROR and CRITICAL to Sentry
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        }
        # Add Sentry handler to relevant loggers
        for logger_name in ['django', 'django.request', '', 'apps', 'gunicorn.error']:
            if 'sentry' not in LOGGING['loggers'][logger_name]['handlers']:
                LOGGING['loggers'][logger_name]['handlers'].append('sentry')

    return LOGGING