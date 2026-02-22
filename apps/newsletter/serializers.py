from rest_framework import serializers
from .models import Subscriber, NewsletterCampaign, EmailLog
from apps.content.serializers import VideoListSerializer, BlogPostListSerializer, CategoryListSerializer


class SubscriberSerializer(serializers.ModelSerializer):
    """Full subscriber serializer with all fields"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    content_preference_display = serializers.CharField(source='get_content_preference_display', read_only=True)
    preferred_categories = CategoryListSerializer(many=True, read_only=True)
    open_rate = serializers.SerializerMethodField()
    click_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscriber
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'content_preference', 'content_preference_display',
            'preferred_categories', 'status', 'status_display',
            'subscribed_at', 'unsubscribed_at', 'unsubscribe_reason',
            'source', 'ip_address', 'user_agent',
            'emails_sent', 'emails_opened', 'emails_clicked',
            'open_rate', 'click_rate', 'last_opened_at', 'last_clicked_at',
            'confirmed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'confirmation_token', 'created_at', 'updated_at']
    
    def get_open_rate(self, obj):
        if obj.emails_sent > 0:
            return round((obj.emails_opened / obj.emails_sent) * 100, 2)
        return 0
    
    def get_click_rate(self, obj):
        if obj.emails_sent > 0:
            return round((obj.emails_clicked / obj.emails_sent) * 100, 2)
        return 0


class SubscriberListSerializer(serializers.ModelSerializer):
    """Lightweight subscriber serializer for list views"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    content_preference_display = serializers.CharField(source='get_content_preference_display', read_only=True)
    
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'first_name', 'last_name', 'status', 'status_display', 'content_preference', 'content_preference_display', 'created_at']


class SubscriberCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new subscribers"""
    
    class Meta:
        model = Subscriber
        fields = ['email', 'first_name', 'last_name', 'content_preference', 'preferred_categories', 'source']


class SubscriberUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating subscriber preferences"""
    
    class Meta:
        model = Subscriber
        fields = ['first_name', 'last_name', 'content_preference', 'preferred_categories', 'status']


class NewsletterCampaignSerializer(serializers.ModelSerializer):
    """Full newsletter campaign serializer with all fields"""
    campaign_type_display = serializers.CharField(source='get_campaign_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    featured_video_data = VideoListSerializer(source='featured_video', read_only=True)
    featured_posts_data = BlogPostListSerializer(source='featured_posts', many=True, read_only=True)
    target_categories = CategoryListSerializer(many=True, read_only=True)
    open_rate = serializers.SerializerMethodField()
    click_rate = serializers.SerializerMethodField()
    click_to_open_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsletterCampaign
        fields = [
            'id', 'name', 'subject', 'preheader',
            'campaign_type', 'campaign_type_display',
            'status', 'status_display',
            'html_content', 'text_content',
            'featured_video', 'featured_video_data',
            'featured_posts', 'featured_posts_data',
            'target_preferences', 'target_categories', 'target_categories',
            'scheduled_at', 'sent_at',
            'total_recipients', 'delivered_count', 'open_count', 'click_count',
            'bounce_count', 'unsubscribe_count',
            'open_rate', 'click_rate', 'click_to_open_rate',
            'sponsored_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_recipients', 'delivered_count', 'open_count', 
                           'click_count', 'bounce_count', 'unsubscribe_count', 
                           'created_at', 'updated_at']
    
    def get_open_rate(self, obj):
        if obj.delivered_count > 0:
            return round((obj.open_count / obj.delivered_count) * 100, 2)
        return 0
    
    def get_click_rate(self, obj):
        if obj.delivered_count > 0:
            return round((obj.click_count / obj.delivered_count) * 100, 2)
        return 0
    
    def get_click_to_open_rate(self, obj):
        if obj.open_count > 0:
            return round((obj.click_count / obj.open_count) * 100, 2)
        return 0


class NewsletterCampaignListSerializer(serializers.ModelSerializer):
    """Lightweight newsletter campaign serializer for list views"""
    campaign_type_display = serializers.CharField(source='get_campaign_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    open_rate = serializers.SerializerMethodField()
    click_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsletterCampaign
        fields = [
            'id', 'name', 'subject', 'campaign_type', 'campaign_type_display',
            'status', 'status_display', 'scheduled_at', 'sent_at',
            'total_recipients', 'delivered_count', 'open_rate', 'click_rate'
        ]
    
    def get_open_rate(self, obj):
        if obj.delivered_count > 0:
            return round((obj.open_count / obj.delivered_count) * 100, 2)
        return 0
    
    def get_click_rate(self, obj):
        if obj.delivered_count > 0:
            return round((obj.click_count / obj.delivered_count) * 100, 2)
        return 0


class NewsletterCampaignCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating newsletter campaigns"""
    
    class Meta:
        model = NewsletterCampaign
        fields = ['name', 'subject', 'preheader', 'campaign_type', 'html_content', 'text_content',
                  'featured_video', 'featured_posts', 'target_preferences', 'target_categories',
                  'scheduled_at', 'sponsored_by']


class EmailLogSerializer(serializers.ModelSerializer):
    """Serializer for email log entries"""
    subscriber_email = serializers.EmailField(source='subscriber.email', read_only=True)
    subscriber_name = serializers.SerializerMethodField()
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    open_rate = serializers.SerializerMethodField()
    click_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EmailLog
        fields = [
            'id', 'campaign', 'campaign_name',
            'subscriber', 'subscriber_email', 'subscriber_name',
            'message_id', 'sent_at', 'delivered_at', 'opened_at', 'clicked_at',
            'bounced_at', 'complained_at', 'clicked_links',
            'open_rate', 'click_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_subscriber_name(self, obj):
        return f"{obj.subscriber.first_name} {obj.subscriber.last_name}".strip() or None
    
    def get_open_rate(self, obj):
        return obj.opened_at is not None
    
    def get_click_count(self, obj):
        return len(obj.clicked_links) if obj.clicked_links else 0


class EmailLogListSerializer(serializers.ModelSerializer):
    """Lightweight email log serializer"""
    subscriber_email = serializers.EmailField(source='subscriber.email', read_only=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = EmailLog
        fields = ['id', 'subscriber_email', 'sent_at', 'opened_at', 'clicked_at', 'status']
    
    def get_status(self, obj):
        if obj.complained_at:
            return 'complained'
        if obj.bounced_at:
            return 'bounced'
        if obj.clicked_at:
            return 'clicked'
        if obj.opened_at:
            return 'opened'
        if obj.delivered_at:
            return 'delivered'
        if obj.sent_at:
            return 'sent'
        return 'pending'
