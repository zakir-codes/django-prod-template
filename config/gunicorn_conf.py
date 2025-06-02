# config/gunicorn_conf.py

import multiprocessing
import os

# Get number of CPU cores
cpu_count = multiprocessing.cpu_count()

# Gunicorn configuration
# Adjust these based on your server's resources and load
workers = os.environ.get('WEB_CONCURRENCY', cpu_count * 2 + 1) # Heroku style, or (2 * CPU_CORES) + 1
threads = os.environ.get('PYTHON_MAX_THREADS', 2) # Number of threads per worker
timeout = os.environ.get('WEB_TIMEOUT', 30) # seconds
bind = '0.0.0.0:8000'
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info') # 'debug', 'info', 'warning', 'error', 'critical'
accesslog = '-' # Output access logs to stdout
errorlog = '-' # Output error logs to stderr
# When running in a container, typically don't need pidfile or daemon
# pidfile = '/tmp/gunicorn.pid'
# daemon = False

# Preload app for faster worker startup (can save memory but requires careful code design)
# If set to True, all your Django code will be loaded into the master process,
# and workers will fork from it. This means any code changes will require a full Gunicorn restart.
# Set to False in development with mounted volumes for hot-reloading.
preload_app = os.environ.get('GUNICORN_PRELOAD_APP', 'False').lower() == 'true'

# Optional: Gunicorn's custom logger class to integrate with Django's logging
# This makes Gunicorn logs appear in your Django application logs
# See: https://docs.gunicorn.org/en/stable/settings.html#logger-class
# class CustomGunicornLogger(gunicorn.glogging.Logger):
#     def setup(self, cfg):
#         super().setup(cfg)
#         # Ensure Django's logging is configured when this runs
#         # This might be tricky if Django's settings aren't fully loaded yet.
#         # Often simpler to let Gunicorn log to stdout/stderr and let Docker/log aggregator handle it.
#         # logging.getLogger('gunicorn.access').addHandler(logging.StreamHandler())
#         # logging.getLogger('gunicorn.error').addHandler(logging.StreamHandler())

# logger_class = 'config.gunicorn_conf.CustomGunicornLogger' # Uncomment to use custom logger