from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Page, Menu, MenuItem, SiteSetting, Widget, MediaLibrary
from .serializers import (
    PageSerializer, PageListSerializer, PageCreateSerializer,
    MenuSerializer, MenuListSerializer,
    SiteSettingSerializer, SiteSettingListSerializer, SiteSettingCreateSerializer,
    WidgetSerializer, WidgetListSerializer, WidgetCreateSerializer,
    MediaLibrarySerializer, MediaLibraryListSerializer, MediaLibraryCreateSerializer
)


class PageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing CMS pages"""
    queryset = Page.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PageListSerializer
        if self.action == 'create':
            return PageCreateSerializer
        return PageSerializer
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """Get all published pages"""
        pages = Page.objects.filter(status='published')
        serializer = PageListSerializer(pages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def navigation(self, request):
        """Get pages for navigation"""
        pages = Page.objects.filter(status='published', show_in_nav=True).order_by('nav_order')
        serializer = PageListSerializer(pages, many=True)
        return Response(serializer.data)


class MenuViewSet(viewsets.ModelViewSet):
    """ViewSet for managing menus"""
    queryset = Menu.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MenuListSerializer
        return MenuSerializer
    
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        """Get menus by location"""
        location = request.query_params.get('location', 'header')
        menus = Menu.objects.filter(location=location, is_active=True)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)


class SiteSettingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing site settings"""
    queryset = SiteSetting.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SiteSettingListSerializer
        if self.action == 'create':
            return SiteSettingCreateSerializer
        return SiteSettingSerializer
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get public settings"""
        settings = SiteSetting.objects.filter(is_public=True)
        serializer = SiteSettingListSerializer(settings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get settings by category"""
        category = request.query_params.get('category', 'general')
        settings = SiteSetting.objects.filter(category=category)
        serializer = SiteSettingListSerializer(settings, many=True)
        return Response(serializer.data)


class WidgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing widgets"""
    queryset = Widget.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return WidgetListSerializer
        if self.action == 'create':
            return WidgetCreateSerializer
        return WidgetSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active widgets"""
        widgets = Widget.objects.filter(is_active=True).order_by('order')
        serializer = WidgetListSerializer(widgets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get widgets by type"""
        widget_type = request.query_params.get('type')
        widgets = Widget.objects.filter(widget_type=widget_type, is_active=True)
        serializer = WidgetListSerializer(widgets, many=True)
        return Response(serializer.data)


class MediaLibraryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing media library"""
    queryset = MediaLibrary.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MediaLibraryListSerializer
        if self.action == 'create':
            return MediaLibraryCreateSerializer
        return MediaLibrarySerializer
    
    def perform_create(self, serializer):
        # Set file size and dimensions
        file = serializer.validated_data['file']
        instance = serializer.save()
        instance.file_size = file.size
        # Try to get image dimensions
        if instance.media_type == 'image':
            try:
                from PIL import Image
                img = Image.open(file)
                instance.width, instance.height = img.size
            except:
                pass
        instance.save()
    
    @action(detail=False, methods=['get'])
    def by_folder(self, request):
        """Get media by folder"""
        folder = request.query_params.get('folder', '')
        media = MediaLibrary.objects.filter(folder=folder)
        serializer = MediaLibraryListSerializer(media, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get media by type"""
        media_type = request.query_params.get('type')
        media = MediaLibrary.objects.filter(media_type=media_type)
        serializer = MediaLibraryListSerializer(media, many=True)
        return Response(serializer.data)
