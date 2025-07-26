import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from collections import defaultdict
from datetime import datetime, timedelta

# Configure logger
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

# Add file handler if not already present
if not logger.handlers:
    file_handler = logging.FileHandler("requests.log")
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server hour (24-hour format)
        current_hour = datetime.now().hour

        # Define restricted hours: only allow between 18 (6PM) and 21 (9PM)
        if not (18 <= current_hour <= 21):
            if request.path.startswith('/conversations/'):
                return HttpResponseForbidden("Access to conversations is only allowed between 6PM and 9PM.")

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of requests per IP
        self.request_log = defaultdict(list)

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only track POST requests to message endpoints
        if request.method == 'POST' and '/conversations/' in request.path and '/messages' in request.path:
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)

            # Filter requests in the last minute
            recent_requests = [ts for ts in self.request_log[ip] if ts > one_minute_ago]
            self.request_log[ip] = recent_requests

            if len(recent_requests) >= 5:
                return JsonResponse({
                    "error": "Rate limit exceeded. Only 5 messages allowed per minute."
                }, status=429)

            # Log this request
            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address of client, accounting for proxy headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce for authenticated users
        if request.user.is_authenticated:
            # Check for role: admin or moderator
            role = getattr(request.user, 'role', None)

            # You can also use is_superuser or is_staff if role field doesn't exist
            if role not in ['admin', 'moderator']:
                protected_paths = ['/conversations/', '/messages/']
                if any(request.path.startswith(p) for p in protected_paths):
                    return HttpResponseForbidden("403 Forbidden: Admin or moderator role required.")
        else:
            # Block unauthenticated access to protected paths
            protected_paths = ['/conversations/', '/messages/']
            if any(request.path.startswith(p) for p in protected_paths):
                return HttpResponseForbidden("403 Forbidden: Login required.")

        return self.get_response(request)
