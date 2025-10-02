import time
import logging
from django.utils.deprecation import MiddlewareMixin


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        content_type = response.get('Content-Type', '')
        if 'text/html' in content_type:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response


logger = logging.getLogger("django.request")

class RequestTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        if hasattr(request, "_start_time"):
            duration = (time.monotonic() - request._start_time) * 1000  # ms
            logger.warning(
                f"Request {request.method} {request.path} took {duration:.2f} ms"
            )
        return response
