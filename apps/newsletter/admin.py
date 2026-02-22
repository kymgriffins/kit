from django.contrib import admin
from .models import Subscriber, NewsletterCampaign, EmailLog


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'content_preference', 'status', 'subscribed_at', 'created_at']
    list_filter = ['status', 'content_preference']
    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = ['preferred_categories']
    readonly_fields = ['confirmation_token', 'emails_sent', 'emails_opened', 'emails_clicked', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'campaign_type', 'status', 'scheduled_at', 'sent_at', 'total_recipients']
    list_filter = ['campaign_type', 'status']
    search_fields = ['name', 'subject', 'html_content']
    filter_horizontal = ['featured_posts', 'target_categories']
    raw_id_fields = ['featured_video', 'sponsored_by']
    readonly_fields = ['total_recipients', 'delivered_count', 'open_count', 'click_count', 'bounce_count', 'unsubscribe_count', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'subscriber', 'message_id', 'sent_at', 'delivered_at', 'opened_at', 'clicked_at']
    list_filter = []
    search_fields = ['campaign__subject', 'subscriber__email', 'message_id']
    raw_id_fields = ['campaign', 'subscriber']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
