from django.db import models
from django.utils import timezone
import uuid


class PageView(models.Model):
    """Track page views for content analytics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    path = models.CharField(max_length=500)
    content_type = models.CharField(max_length=50, blank=True)
    content_id = models.UUIDField(null=True, blank=True)
    
    # User info
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # Device info
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Location
    country = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_pageview'
        indexes = [
            models.Index(fields=['content_type', 'content_id']),
            models.Index(fields=['created_at']),
            models.Index(fields=['path']),
        ]
    
    def __str__(self):
        return f"{self.path} - {self.created_at}"


class VideoEngagement(models.Model):
    """Detailed video interaction tracking"""
    video = models.ForeignKey(
        'content.VideoContent',
        on_delete=models.CASCADE,
        related_name='engagement_events'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    session_id = models.CharField(max_length=100)
    
    event_type = models.CharField(
        max_length=20,
        choices=[
            ('play', 'Play'),
            ('pause', 'Pause'),
            ('complete', 'Complete'),
            ('seek', 'Seek'),
            ('mute', 'Mute'),
            ('unmute', 'Unmute'),
        ]
    )
    timestamp_seconds = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_videoengagement'


class DonorFunnel(models.Model):
    """Track donor journey"""
    donor = models.ForeignKey(
        'accounts.DonorProfile',
        on_delete=models.CASCADE,
        related_name='funnel_events'
    )
    stage = models.CharField(
        max_length=50,
        choices=[
            ('awareness', 'Awareness'),
            ('interest', 'Interest'),
            ('consideration', 'Consideration'),
            ('donation', 'Donation'),
            ('retention', 'Retention'),
            ('advocacy', 'Advocacy'),
        ]
    )
    source = models.CharField(max_length=100, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_donorfunnel'
