from django.contrib import admin
from .models import Page, Menu, MenuItem, SiteSetting, Widget, MediaLibrary


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'template', 'status', 'is_featured', 'show_in_nav', 'published_at']
    list_filter = ['status', 'template', 'is_featured', 'show_in_nav']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'location', 'is_active']
    list_filter = ['location', 'is_active']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'link_type', 'parent', 'order', 'is_active']
    list_filter = ['menu', 'link_type', 'is_active']
    search_fields = ['title']


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_type', 'category', 'is_public']
    list_filter = ['category', 'value_type', 'is_public']
    search_fields = ['key', 'description']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'order', 'is_active']
    list_filter = ['widget_type', 'is_active']
    search_fields = ['name', 'title']


@admin.register(MediaLibrary)
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ['filename', 'media_type', 'file_size', 'uploaded_by', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['filename', 'title', 'tags']
    date_hierarchy = 'created_at'
