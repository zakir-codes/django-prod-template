# config/middleware.py

import logging
import time
import json # For JSON logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        response = self.get_response(request)
        end_time = time.monotonic()
        duration_ms = round((end_time - start_time) * 1000, 2)

        # Build log data for context
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': duration_ms,
            'remote_ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'http_referer': request.META.get('HTTP_REFERER', ''),
            'user_id': request.user.id if request.user.is_authenticated else None,
        }

        # Log at different levels based on status code
        if response.status_code >= 500:
            logger.error("Server error for %s %s", request.method, request.path, extra=log_data)
        elif response.status_code >= 400:
            # Avoid logging 404s as errors unless specifically desired
            if response.status_code != 404:
                logger.warning("Client error for %s %s", request.method, request.path, extra=log_data)
            else:
                logger.info("Not Found: %s %s", request.method, request.path, extra=log_data) # Log 404s as INFO
        else:
            logger.info("Request successful for %s %s", request.method, request.path, extra=log_data)

        return response