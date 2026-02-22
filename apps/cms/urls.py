from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PageViewSet, MenuViewSet, SiteSettingViewSet, 
    WidgetViewSet, MediaLibraryViewSet
)

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='cms-pages')
router.register(r'menus', MenuViewSet, basename='cms-menus')
router.register(r'settings', SiteSettingViewSet, basename='cms-settings')
router.register(r'widgets', WidgetViewSet, basename='cms-widgets')
router.register(r'media', MediaLibraryViewSet, basename='cms-media')

urlpatterns = [
    path('', include(router.urls)),
]
