import uuid
from django.db import models

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#0066CC')
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
        db_table = 'content_category'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VideoContent(models.Model):
    class Platform(models.TextChoices):
        TIKTOK = 'tiktok', _('TikTok')
        YOUTUBE = 'youtube', _('YouTube')
        X = 'x', _('X (Twitter)')
        FACEBOOK = 'facebook', _('Facebook')
        INSTAGRAM = 'instagram', _('Instagram')
    
    class ContentType(models.TextChoices):
        BUDGET_BASICS = 'budget_basics', _('Budget Basics')
        FINANCE_BILL = 'finance_bill', _('Finance Bill')
        NATIONAL_BUDGET = 'national_budget', _('National Budget')
        COUNTY_BUDGET = 'county_budget', _('County Budget')
        SECTOR_DEEP_DIVE = 'sector_deep_dive', _('Sector Deep Dive')
        TRACKER_STORY = 'tracker_story', _('Tracker Story')
        YOUTH_VOICE = 'youth_voice', _('Youth Voice')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Platform integration
    platform = models.CharField(max_length=20, choices=Platform.choices)
    external_id = models.CharField(max_length=255)
    external_url = models.URLField()
    embed_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    
    # Content metadata
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    categories = models.ManyToManyField(Category, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Engagement metrics
    view_count = models.PositiveBigIntegerField(default=0)
    like_count = models.PositiveBigIntegerField(default=0)
    share_count = models.PositiveBigIntegerField(default=0)
    comment_count = models.PositiveBigIntegerField(default=0)
    last_metrics_update = models.DateTimeField(null=True, blank=True)
    
    # Curation
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    
    # Relations
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos'
    )
    playlist = models.ForeignKey(
        'Playlist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos'
    )
    
    # Sponsor integration
    sponsored_by = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sponsored_videos'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'content_video'
        ordering = ['-is_featured', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['platform', 'is_published']),
            models.Index(fields=['content_type', 'is_published']),
            models.Index(fields=['-published_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)


class Playlist(models.Model):
    """Curated collections for learning paths"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='playlists/', blank=True)
    is_featured = models.BooleanField(default=False)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    estimated_duration_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'content_playlist'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    class PostType(models.TextChoices):
        INVESTIGATION = 'investigation', _('Investigation')
        EXPLAINER = 'explainer', _('Explainer')
        UPDATE = 'update', _('Update')
        FIELD_REPORT = 'field_report', _('Field Report')
        OPINION = 'opinion', _('Opinion')
        SPONSORED = 'sponsored', _('Sponsored Content')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        REVIEW = 'review', _('Under Review')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=500, blank=True)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    
    # Categorization
    post_type = models.CharField(max_length=20, choices=PostType.choices)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Media
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True)
    featured_image_caption = models.CharField(max_length=255, blank=True)
    
    # Authoring
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts'
    )
    co_authors = models.ManyToManyField('accounts.User', blank=True, related_name='co_authored_posts')
    
    # Publishing workflow
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_publish_at = models.DateTimeField(null=True, blank=True)
    
    # Engagement
    view_count = models.PositiveBigIntegerField(default=0)
    read_time_minutes = models.PositiveSmallIntegerField(default=5)
    allow_comments = models.BooleanField(default=True)
    
    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='blog/og/', blank=True)
    
    # Search
    search_vector = models.TextField(null=True, blank=True, editable=False)
    
    # Sponsor integration
    sponsored_by = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sponsored_posts'
    )
    
    # Related content
    related_videos = models.ManyToManyField(VideoContent, blank=True)
    related_posts = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'content_blogpost'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['post_type', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/blog/{self.slug}/'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug[:50]
        
        # Auto-calculate read time
        if self.content:
            word_count = len(self.content.split())
            self.read_time_minutes = max(1, word_count // 200)
        
        super().save(*args, **kwargs)


class NewsItem(models.Model):
    """Quick updates, breaking news - shorter than blog posts"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    source_url = models.URLField(blank=True)
    is_breaking = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'content_newsitem'
        ordering = ['-is_breaking', '-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
