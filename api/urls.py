"""api URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import api_docs, home, config_page, index
from apps.core import views_api

urlpatterns = [
    # Admin - must come first to avoid conflicts
    path('admin/', admin.site.urls),
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),  # Root serves home.html
    path('index/', index, name='index'),  # Main app page
    path('config/', config_page, name='config'),
    
    # API Documentation
    path('api/docs/', api_docs, name='api_docs'),
    
    # API Dashboard - Custom HTML Interface
    path('api/', views_api.APIDashboardView.as_view(), name='api_dashboard'),
    path('api/browser/', views_api.APIBrowserView.as_view(), name='api_browser'),
    path('api/v1/<str:app_name>/', views_api.APIEndpointProxyView.as_view(), name='api_endpoint'),
    
    # API endpoints (original DRF endpoints)
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/content/', include('apps.content.urls')),
    path('api/v1/newsletter/', include('apps.newsletter.urls')),
    path('api/v1/sponsors/', include('apps.sponsors.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/cms/', include('apps.cms.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
