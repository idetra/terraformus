from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from terraformus.core import views

urlpatterns = [
    # all auth
    path('accounts/', include('allauth.urls')),
    path('account/delete_account/', views.delete_account, name='delete_account'),
    # solutions
    path('solutions/', views.solutions, name='solutions'),
    path('solution/<uuid:uuid>/<str:slug>', views.solution, name='solution'),
    path('create_solution/', views.create_solution, name='create_solution'),
    path('edit_solution/<str:slug>', views.edit_solution, name='edit_solution'),
    path('delete_solution/<str:slug>', views.delete_solution, name='delete_solution'),
    path('create_life_cycle/<str:pk>', views.create_life_cycle, name='create_life_cycle'),
    path('edit_life_cycle/<str:pk>', views.edit_life_cycle, name='edit_life_cycle'),
    path('delete_life_cycle/<str:pk>', views.delete_life_cycle, name='delete_life_cycle'),
    # strategies
    path('strategies/', views.strategies, name='strategies'),
    path('strategy/<uuid:uuid>/<str:slug>', views.strategy, name='strategy'),
    path('create_strategy/', views.create_strategy, name='create_strategy'),
    path('edit_strategy/<str:slug>', views.edit_strategy, name='edit_strategy'),
    path('delete_strategy/<str:slug>', views.delete_strategy, name='delete_strategy'),
    # solutions & strategies
    path('create_external_asset/<str:model_name>/<str:pk>', views.create_external_asset, name='create_external_asset'),
    path('edit_external_asset/<str:model_name>/<str:pk>', views.edit_external_asset, name='edit_external_asset'),
    path('delete_external_asset/<str:model_name>/<str:pk>', views.delete_external_asset, name='delete_external_asset'),
    # extras
    path('rate/<str:slug>', views.rate, name='rate'),
    path('report/<str:slug>', views.report, name='report'),
    path('rating_reply/<int:pk>', views.rating_reply, name='rating_reply'),
    # users
    path('profile/', views.profile, name='profile'),
    path('author/<str:name>', views.author, name='author'),
    path('my_proposals', views.my_proposals, name='my_proposals'),
    # system
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)