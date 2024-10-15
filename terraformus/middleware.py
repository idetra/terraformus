from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ExemptCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            # Resolve the requested URL
            resolver_match = resolve(request.path_info)

            # Check if the resolved view is a class-based view and compare
            if hasattr(resolver_match.func, 'view_class') and resolver_match.func.view_class in [TokenObtainPairView,
                                                                                                 TokenRefreshView]:
                setattr(request, '_dont_enforce_csrf_checks', True)
        except Exception as e:
            # Optionally log the exception or handle it as needed
            pass
