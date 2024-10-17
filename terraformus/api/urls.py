from django.urls import path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from terraformus.api import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from terraformus.api.views import CustomTokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[permissions.AllowAny]), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=[permissions.AllowAny]), name='redoc-ui'),
    path('solutions/', views.SolutionList.as_view(), name='solution_list'),
    path('solutions/<uuid:uuid>', views.SolutionItem.as_view(), name='solution_item'),
    path('strategies/', views.StrategyList.as_view(), name='strategy_list'),
    path('strategies/<uuid:uuid>', views.StrategyItem.as_view(), name='strategy_item'),
]
