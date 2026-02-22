from rest_framework import serializers
from .models import PageView, VideoEngagement, DonorFunnel


class PageViewSerializer(serializers.ModelSerializer):
    """Serializer for page view analytics"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    device_type_display = serializers.CharField(source='get_device_type_display', read_only=True)
    
    class Meta:
        model = PageView
        fields = [
            'id', 'url', 'path', 'content_type', 'content_id',
            'user', 'user_email', 'user_name', 'session_id',
            'ip_address', 'user_agent', 'referrer',
            'device_type', 'device_type_display', 'browser', 'os',
            'country', 'city', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return None


class PageViewListSerializer(serializers.ModelSerializer):
    """Lightweight page view serializer for list views"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = PageView
        fields = ['id', 'path', 'content_type', 'user_email', 'country', 'device_type', 'created_at']


class VideoEngagementSerializer(serializers.ModelSerializer):
    """Serializer for video engagement tracking"""
    video_title = serializers.CharField(source='video.title', read_only=True)
    video_slug = serializers.SlugField(source='video.slug', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = VideoEngagement
        fields = [
            'id', 'video', 'video_title', 'video_slug',
            'user', 'user_email', 'user_name', 'session_id',
            'event_type', 'event_type_display', 'timestamp_seconds',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return None


class VideoEngagementSummarySerializer(serializers.ModelSerializer):
    """Summary serializer for video engagement"""
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = VideoEngagement
        fields = ['id', 'event_type', 'event_type_display', 'timestamp_seconds', 'created_at']


class DonorFunnelSerializer(serializers.ModelSerializer):
    """Serializer for donor funnel tracking"""
    donor_email = serializers.EmailField(source='donor.user.email', read_only=True)
    donor_name = serializers.SerializerMethodField()
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    
    class Meta:
        model = DonorFunnel
        fields = [
            'id', 'donor', 'donor_email', 'donor_name',
            'stage', 'stage_display', 'source', 'value', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_donor_name(self, obj):
        return obj.donor.user.get_full_name()


class DonorFunnelListSerializer(serializers.ModelSerializer):
    """Lightweight donor funnel serializer"""
    donor_email = serializers.EmailField(source='donor.user.email', read_only=True)
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    
    class Meta:
        model = DonorFunnel
        fields = ['id', 'donor_email', 'stage', 'stage_display', 'value', 'created_at']


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary data"""
    total_page_views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    total_video_plays = serializers.IntegerField()
    total_video_completions = serializers.IntegerField()
    average_watch_time = serializers.FloatField()
    top_pages = serializers.ListField()
    top_videos = serializers.ListField()
    top_countries = serializers.ListField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
