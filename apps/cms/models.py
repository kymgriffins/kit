import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    """Custom pages for the CMS"""
    class Template(models.TextChoices):
        DEFAULT = 'default', _('Default')
        HOME = 'home', _('Home')
        ABOUT = 'about', _('About')
        CONTACT = 'contact', _('Contact')
        LANDING = 'landing', _('Landing Page')
        FULLWIDTH = 'fullwidth', _('Full Width')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    
    # Template & Layout
    template = models.CharField(max_length=20, choices=Template.choices, default=Template.DEFAULT)
    
    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='cms/og/', blank=True)
    
    # Featured Media
    featured_image = models.ImageField(upload_to='cms/pages/', blank=True)
    video_url = models.URLField(blank=True)
    
    # Visibility
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    show_in_nav = models.BooleanField(default=False)
    nav_order = models.PositiveSmallIntegerField(default=0)
    
    # Layout Options
    show_sidebar = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=False)
    full_width = models.BooleanField(default=False)
    
    # Background
    background_color = models.CharField(max_length=7, default='#ffffff')
    background_image = models.ImageField(upload_to='cms/backgrounds/', blank=True)
    
    # Author
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='cms_pages'
    )
    
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_page'
        ordering = ['nav_order', '-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)


class Menu(models.Model):
    """Navigation menus"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(
        max_length=50,
        choices=[
            ('header', 'Header'),
            ('footer', 'Footer'),
            ('sidebar', 'Sidebar'),
            ('mobile', 'Mobile'),
        ],
        default='header'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cms_menu'
        verbose_name_plural = 'Menus'
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Individual menu items"""
    class LinkType(models.TextChoices):
        PAGE = 'page', _('Page')
        URL = 'url', _('Custom URL')
        CATEGORY = 'category', _('Category')
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    title = models.CharField(max_length=100)
    link_type = models.CharField(max_length=20, choices=LinkType.choices, default=LinkType.PAGE)
    
    # Link targets
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey('content.Category', on_delete=models.CASCADE, null=True, blank=True)
    
    # Display
    icon = models.CharField(max_length=50, blank=True)
    css_class = models.CharField(max_length=100, blank=True)
    target_new_tab = models.BooleanField(default=False)
    
    # Order
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cms_menu_item'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.menu.name} - {self.title}"
    
    def get_url(self):
        if self.link_type == self.LinkType.PAGE and self.page:
            return f"/page/{self.page.slug}/"
        elif self.link_type == self.LinkType.URL:
            return self.url
        elif self.link_type == self.LinkType.CATEGORY and self.category:
            return f"/category/{self.category.slug}/"
        return "#"


class SiteSetting(models.Model):
    """Site-wide settings stored in database"""
    class Category(models.TextChoices):
        GENERAL = 'general', _('General')
        APPEARANCE = 'appearance', _('Appearance')
        SOCIAL = 'social', _('Social Media')
        INTEGRATIONS = 'integrations', _('Integrations')
        ANALYTICS = 'analytics', _('Analytics')
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    value_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('number', 'Number'),
            ('boolean', 'Boolean'),
            ('json', 'JSON'),
            ('image', 'Image'),
        ],
        default='text'
    )
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cms_site_setting'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return self.key


class Widget(models.Model):
    """Reusable widgets for pages"""
    class WidgetType(models.TextChoices):
        HERO = 'hero', _('Hero Section')
        FEATURED_VIDEOS = 'featured_videos', _('Featured Videos')
        LATEST_POSTS = 'latest_posts', _('Latest Posts')
        NEWSLETTER = 'newsletter', _('Newsletter Signup')
        SPONSORS = 'sponsors', _('Sponsors Carousel')
        STATS = 'stats', _('Statistics Counter')
        TESTIMONIALS = 'testimonials', _('Testimonials')
        CALL_TO_ACTION = 'call_to_action', _('Call to Action')
        VIDEO_GRID = 'video_grid', _('Video Grid')
        BLOG_GRID = 'blog_grid', _('Blog Grid')
        CUSTOM_HTML = 'custom_html', _('Custom HTML')
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=30, choices=WidgetType.choices)
    
    # Content
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    settings = models.JSONField(default=dict, blank=True)
    
    # Display
    css_class = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_widget'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"


class MediaLibrary(models.Model):
    """Media files management"""
    class MediaType(models.TextChoices):
        IMAGE = 'image', _('Image')
        VIDEO = 'video', _('Video')
        DOCUMENT = 'document', _('Document')
        AUDIO = 'audio', _('Audio')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='cms/media/')
    filename = models.CharField(max_length=255)
    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.IMAGE)
    
    # Metadata
    title = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    file_size = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    
    # Organization
    folder = models.CharField(max_length=255, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='uploaded_media'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cms_media_library'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.filename
