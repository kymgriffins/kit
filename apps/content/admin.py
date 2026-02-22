from django.contrib import admin
from .models import Category, VideoContent, Playlist, BlogPost, NewsItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'content_type', 'is_featured', 'is_published', 'view_count', 'published_at']
    list_filter = ['platform', 'content_type', 'is_featured', 'is_published']
    search_fields = ['title', 'description', 'external_id']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author', 'playlist', 'sponsored_by']
    filter_horizontal = ['categories']
    readonly_fields = ['view_count', 'like_count', 'share_count', 'comment_count', 'created_at', 'updated_at']
    ordering = ['-is_featured', '-published_at', '-created_at']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'difficulty_level', 'is_featured', 'estimated_duration_minutes']
    list_filter = ['difficulty_level', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'status', 'author', 'view_count', 'published_at', 'created_at']
    list_filter = ['post_type', 'status']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author', 'sponsored_by']
    filter_horizontal = ['categories', 'co_authors', 'related_videos', 'related_posts']
    readonly_fields = ['view_count', 'search_vector', 'created_at', 'updated_at']
    ordering = ['-published_at', '-created_at']


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_breaking', 'published_at', 'expires_at']
    list_filter = ['is_breaking']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-is_breaking', '-published_at']
