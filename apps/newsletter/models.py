import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Subscriber(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending Confirmation')
        ACTIVE = 'active', _('Active')
        UNSUBSCRIBED = 'unsubscribed', _('Unsubscribed')
        BOUNCED = 'bounced', _('Bounced')
        COMPLAINED = 'complained', _('Complained')
    
    class ContentPreference(models.TextChoices):
        ALL = 'all', _('All Content')
        VIDEOS_ONLY = 'videos_only', _('Videos Only')
        BLOGS_ONLY = 'blogs_only', _('Blogs Only')
        WEEKLY_DIGEST = 'weekly_digest', _('Weekly Digest Only')
        MONTHLY_ROUNDUP = 'monthly_roundup', _('Monthly Round-up')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    
    # Preferences
    content_preference = models.CharField(
        max_length=20,
        choices=ContentPreference.choices,
        default=ContentPreference.ALL
    )
    preferred_categories = models.ManyToManyField('content.Category', blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    subscribed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    unsubscribe_reason = models.TextField(blank=True)
    
    # Tracking
    source = models.CharField(max_length=50, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Engagement metrics
    emails_sent = models.PositiveIntegerField(default=0)
    emails_opened = models.PositiveIntegerField(default=0)
    emails_clicked = models.PositiveIntegerField(default=0)
    last_opened_at = models.DateTimeField(null=True, blank=True)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    
    # Double opt-in
    confirmation_token = models.CharField(max_length=100, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'newsletter_subscriber'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.status})"


class NewsletterCampaign(models.Model):
    class Type(models.TextChoices):
        WEEKLY_DIGEST = 'weekly_digest', _('Weekly Digest')
        DAILY_UPDATE = 'daily_update', _('Daily Update')
        BREAKING_NEWS = 'breaking_news', _('Breaking News')
        MONTHLY_ROUNDUP = 'monthly_roundup', _('Monthly Round-up')
        SPONSORED = 'sponsored', _('Sponsored Content')
        WELCOME_SERIES = 'welcome_series', _('Welcome Series')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        SCHEDULED = 'scheduled', _('Scheduled')
        SENDING = 'sending', _('Sending')
        SENT = 'sent', _('Sent')
        PAUSED = 'paused', _('Paused')
        CANCELLED = 'cancelled', _('Cancelled')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    preheader = models.CharField(max_length=255, blank=True)
    
    campaign_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    # Content
    html_content = models.TextField(blank=True)
    text_content = models.TextField(blank=True)
    
    # Featured content
    featured_video = models.ForeignKey(
        'content.VideoContent',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    featured_posts = models.ManyToManyField('content.BlogPost', blank=True)
    
    # Targeting
    target_preferences = models.JSONField(
        default=list,
        blank=True
    )
    target_categories = models.ManyToManyField('content.Category', blank=True)
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Metrics
    total_recipients = models.PositiveIntegerField(default=0)
    delivered_count = models.PositiveIntegerField(default=0)
    open_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    bounce_count = models.PositiveIntegerField(default=0)
    unsubscribe_count = models.PositiveIntegerField(default=0)
    
    # Sponsor integration
    sponsored_by = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'newsletter_campaign'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} ({self.get_status_display()})"


class EmailLog(models.Model):
    """Individual email tracking"""
    campaign = models.ForeignKey(
        NewsletterCampaign,
        on_delete=models.CASCADE,
        related_name='email_logs'
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name='email_logs'
    )
    message_id = models.CharField(max_length=255, blank=True)
    
    # Status tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    bounced_at = models.DateTimeField(null=True, blank=True)
    complained_at = models.DateTimeField(null=True, blank=True)
    
    # Click tracking
    clicked_links = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'newsletter_emaillog'
        unique_together = ['campaign', 'subscriber']
