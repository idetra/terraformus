from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from terraformus.core import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('account/delete_account/', views.delete_account, name='delete_account'),
    # solutions
    path('solutions/', views.solutions, name='solutions'),
    # users
    path('profile/', views.profile, name='profile'),
    path('author/<str:name>', views.author, name='author'),
    # system
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)