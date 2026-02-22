from django.contrib import admin
from .models import PageView, VideoEngagement, DonorFunnel


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'content_type', 'user', 'session_id', 'country', 'created_at']
    list_filter = ['content_type', 'device_type', 'browser', 'country']
    search_fields = ['path', 'session_id', 'ip_address']
    raw_id_fields = ['user']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(VideoEngagement)
class VideoEngagementAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'session_id', 'event_type', 'timestamp_seconds', 'created_at']
    list_filter = ['event_type']
    search_fields = ['video__title', 'session_id']
    raw_id_fields = ['video', 'user']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(DonorFunnel)
class DonorFunnelAdmin(admin.ModelAdmin):
    list_display = ['donor', 'stage', 'source', 'value', 'created_at']
    list_filter = ['stage', 'source']
    search_fields = ['donor__user__email']
    raw_id_fields = ['donor']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
