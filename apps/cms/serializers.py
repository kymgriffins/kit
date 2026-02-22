from rest_framework import serializers
from .models import Page, Menu, MenuItem, SiteSetting, Widget, MediaLibrary


class PageSerializer(serializers.ModelSerializer):
    """Full page serializer with all fields"""
    template_display = serializers.CharField(source='get_template_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    author_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'subtitle', 'content', 'content_html',
            'template', 'template_display',
            'meta_title', 'meta_description', 'og_image',
            'featured_image', 'video_url',
            'status', 'status_display', 'is_featured', 'show_in_nav', 'nav_order',
            'show_sidebar', 'show_comments', 'full_width',
            'background_color', 'background_image',
            'author', 'author_name',
            'published_at', 'created_at', 'updated_at', 'url'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return None
    
    def get_url(self, obj):
        return f"/page/{obj.slug}/"


class PageListSerializer(serializers.ModelSerializer):
    """Lightweight page serializer for list views"""
    template_display = serializers.CharField(source='get_template_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'subtitle', 'template', 'template_display',
            'status', 'status_display', 'is_featured', 'show_in_nav',
            'featured_image', 'author_name', 'published_at', 'created_at'
        ]
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return None


class PageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating pages"""
    
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'subtitle', 'content', 'template',
            'meta_title', 'meta_description', 'og_image',
            'featured_image', 'video_url',
            'status', 'is_featured', 'show_in_nav', 'nav_order',
            'show_sidebar', 'show_comments', 'full_width',
            'background_color', 'background_image', 'author'
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    """Menu item serializer with nested children"""
    link_type_display = serializers.CharField(source='get_link_type_display', read_only=True)
    url = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'menu', 'parent', 'title', 'link_type', 'link_type_display',
            'page', 'url', 'category',
            'icon', 'css_class', 'target_new_tab',
            'order', 'is_active', 'children'
        ]
        read_only_fields = ['id']
    
    def get_url(self, obj):
        return obj.get_url()
    
    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('order')
        return MenuItemSerializer(children, many=True).data


class MenuSerializer(serializers.ModelSerializer):
    """Full menu serializer with items"""
    location_display = serializers.CharField(source='get_location_display', read_only=True)
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'slug', 'description', 'location', 'location_display',
            'is_active', 'items'
        ]
        read_only_fields = ['id']
    
    def get_items(self, obj):
        items = obj.items.filter(parent__isnull=True, is_active=True).order_by('order')
        return MenuItemSerializer(items, many=True).data


class MenuListSerializer(serializers.ModelSerializer):
    """Lightweight menu serializer"""
    location_display = serializers.CharField(source='get_location_display', read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'slug', 'location', 'location_display', 'is_active', 'item_count']
    
    def get_item_count(self, obj):
        return obj.items.filter(is_active=True).count()


class SiteSettingSerializer(serializers.ModelSerializer):
    """Site setting serializer"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    value_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteSetting
        fields = [
            'id', 'key', 'value', 'value_display', 'value_type',
            'category', 'category_display', 'description', 'is_public'
        ]
        read_only_fields = ['id']
    
    def get_value_display(self, obj):
        if obj.value_type == 'boolean':
            return obj.value.lower() == 'true'
        elif obj.value_type == 'json':
            import json
            try:
                return json.loads(obj.value)
            except:
                return obj.value
        return obj.value


class SiteSettingListSerializer(serializers.ModelSerializer):
    """Lightweight site setting serializer"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = SiteSetting
        fields = ['id', 'key', 'value_type', 'category', 'category_display', 'description', 'is_public']


class SiteSettingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating site settings"""
    
    class Meta:
        model = SiteSetting
        fields = ['key', 'value', 'value_type', 'category', 'description', 'is_public']


class WidgetSerializer(serializers.ModelSerializer):
    """Full widget serializer with all fields"""
    widget_type_display = serializers.CharField(source='get_widget_type_display', read_only=True)
    
    class Meta:
        model = Widget
        fields = [
            'id', 'name', 'widget_type', 'widget_type_display',
            'title', 'content', 'settings',
            'css_class', 'is_active', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WidgetListSerializer(serializers.ModelSerializer):
    """Lightweight widget serializer"""
    widget_type_display = serializers.CharField(source='get_widget_type_display', read_only=True)
    
    class Meta:
        model = Widget
        fields = ['id', 'name', 'widget_type', 'widget_type_display', 'is_active', 'order']


class WidgetCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating widgets"""
    
    class Meta:
        model = Widget
        fields = ['name', 'widget_type', 'title', 'content', 'settings', 'css_class', 'is_active', 'order']


class MediaLibrarySerializer(serializers.ModelSerializer):
    """Full media library serializer"""
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaLibrary
        fields = [
            'id', 'file', 'file_url', 'filename', 'media_type', 'media_type_display',
            'title', 'alt_text', 'caption', 'file_size', 'file_size_formatted',
            'width', 'height', 'folder', 'tags',
            'uploaded_by', 'uploaded_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'file_size', 'width', 'height', 'created_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name()
        return None
    
    def get_file_size_formatted(self, obj):
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


class MediaLibraryListSerializer(serializers.ModelSerializer):
    """Lightweight media library serializer"""
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaLibrary
        fields = ['id', 'file_url', 'filename', 'media_type', 'media_type_display', 'file_size_formatted', 'created_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_file_size_formatted(self, obj):
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


class MediaLibraryCreateSerializer(serializers.ModelSerializer):
    """Serializer for uploading media"""
    
    class Meta:
        model = MediaLibrary
        fields = ['file', 'title', 'alt_text', 'caption', 'folder', 'tags', 'uploaded_by']
