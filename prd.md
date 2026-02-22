 Here is the complete Django setup for your **Budget Ndio Story** platform with the full ecosystem.

---

# Budget Ndio Story - Django Backend Architecture

## Project Structure

```text
budget_ndio_backend/
├── apps/
│   ├── __init__.py
│   ├── accounts/                 # User management (donors, sponsors, admins)
│   ├── content/                  # Videos, blogs, news (the Learning Hub)
│   ├── newsletter/               # Email subscriptions & campaigns
│   ├── sponsors/                 # Donor/Sponsor ecosystem
│   └── analytics/                # Engagement tracking
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/
│   ├── base.txt
│   └── production.txt
├── templates/
├── static/
├── media/
├── celery_app.py
├── manage.py
└── Dockerfile
```

---

## 1. Requirements

```txt
# requirements/base.txt
Django>=5.0,<5.1
djangorestframework>=3.14.0
django-cors-headers>=4.3.0
django-filter>=23.5
django-extensions>=3.2.3
django-cleanup>=8.0.0
django-storages>=1.14.0

# Database
psycopg2-binary>=2.9.9

# Async & Tasks
celery[redis]>=5.3.0
redis>=5.0.0
django-celery-beat>=2.5.0
django-celery-results>=2.5.0

# API & Serialization
djangorestframework-simplejwt>=5.3.0
drf-spectacular>=0.27.0  # OpenAPI docs

# Social Media APIs
requests>=2.31.0
google-api-python-client>=2.108.0
tweepy>=4.14.0
facebook-sdk>=3.1.0

# Email
django-anymail[sendgrid]>=10.2

# Utilities
Pillow>=10.1.0
python-decouple>=3.8
pytz>=2023.3
gunicorn>=21.2.0
whitenoise>=6.6.0

# Development
pytest-django>=4.7.0
factory-boy>=3.3.0
faker>=20.1.0
```

---

## 2. Settings Configuration

```python
# config/settings/base.py
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',  # For full-text search
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'django_celery_beat',
    'django_celery_results',
    'anymail',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.content',
    'apps.newsletter',
    'apps.sponsors',
    'apps.analytics',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
    }
}

# Cache & Celery
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes max for newsletter sends

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'Budget Ndio Story API',
    'DESCRIPTION': 'Civic education platform API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# CORS
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Email Configuration
EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
ANYMAIL = {
    'SENDGRID_API_KEY': config('SENDGRID_API_KEY', default=''),
}
DEFAULT_FROM_EMAIL = 'Budget Ndio Story <newsletter@budgetndiostory.org>'
SERVER_EMAIL = 'server@budgetndiostory.org'

# Social Media API Keys
YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', default='')
TWITTER_BEARER_TOKEN = config('TWITTER_BEARER_TOKEN', default='')
FACEBOOK_ACCESS_TOKEN = config('FACEBOOK_ACCESS_TOKEN', default='')
TIKTOK_ACCESS_TOKEN = config('TIKTOK_ACCESS_TOKEN', default='')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## 3. Accounts App (Users, Donors, Sponsors)

```python
# apps/accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        EDITOR = 'editor', _('Content Editor')
        VIEWER = 'viewer', _('Viewer')
        DONOR = 'donor', _('Donor')
        SPONSOR = 'sponsor', _('Sponsor')
        PARTNER = 'partner', _('Consortium Partner')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Newsletter preferences
    newsletter_subscribed = models.BooleanField(default=False)
    newsletter_preferences = models.JSONField(default=dict, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'accounts_user'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class DonorProfile(models.Model):
    class DonorType(models.TextChoices):
        INDIVIDUAL = 'individual', _('Individual')
        CORPORATE = 'corporate', _('Corporate')
        FOUNDATION = 'foundation', _('Foundation')
        INSTITUTIONAL = 'institutional', _('Institutional')
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='donor_profile'
    )
    donor_type = models.CharField(max_length=20, choices=DonorType.choices)
    tax_id = models.CharField(max_length=50, blank=True)  # For receipts
    billing_address = models.TextField(blank=True)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    donation_count = models.PositiveIntegerField(default=0)
    first_donation_date = models.DateField(null=True, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_recurring_donor = models.BooleanField(default=False)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    communication_preferences = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)  # Internal notes
    
    class Meta:
        db_table = 'accounts_donor_profile'
    
    def __str__(self):
        return f"Donor: {self.user.email}"


class SponsorProfile(models.Model):
    class SponsorshipLevel(models.TextChoices):
        BRONZE = 'bronze', _('Bronze Partner')
        SILVER = 'silver', _('Silver Partner')
        GOLD = 'gold', _('Gold Partner')
        PLATINUM = 'platinum', _('Platinum Partner')
        STRATEGIC = 'strategic', _('Strategic Partner')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='sponsor_profile'
    )
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/logos/')
    website = models.URLField(blank=True)
    level = models.CharField(max_length=20, choices=SponsorshipLevel.choices)
    contract_value = models.DecimalField(max_digits=12, decimal_places=2)
    contract_start = models.DateField()
    contract_end = models.DateField()
    benefits_claimed = models.JSONField(default=list, blank=True)  # Track deliverables
    brand_visibility_slots = models.PositiveIntegerField(default=0)
    dedicated_content_pieces = models.PositiveIntegerField(default=0)
    event_sponsorships = models.PositiveIntegerField(default=0)
    account_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_sponsors'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'accounts_sponsor_profile'
        ordering = ['-contract_value']
    
    def __str__(self):
        return f"{self.company_name} ({self.get_level_display()})"


class ConsortiumPartner(models.Model):
    """The Continental Pot, Colour Twist Media, Sen Media"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='partners/')
    description = models.TextField()
    website = models.URLField(blank=True)
    contact_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_partners'
    )
    content_contribution_weight = models.PositiveSmallIntegerField(
        default=1,
        help_text="For revenue sharing calculations"
    )
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'accounts_consortium_partner'
    
    def __str__(self):
        return self.name
```

```python
# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, DonorProfile, SponsorProfile, ConsortiumPartner


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'phone', 'organization', 'bio', 'avatar',
            'is_verified', 'newsletter_subscribed', 'created_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DonorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DonorProfile
        fields = '__all__'
        read_only_fields = ['total_donated', 'donation_count', 'first_donation_date', 'last_donation_date']


class SponsorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    account_manager_name = serializers.CharField(source='account_manager.get_full_name', read_only=True)
    
    class Meta:
        model = SponsorProfile
        fields = '__all__'


class ConsortiumPartnerSerializer(serializers.ModelSerializer):
    contact_person_name = serializers.CharField(source='contact_person.get_full_name', read_only=True)
    
    class Meta:
        model = ConsortiumPartner
        fields = '__all__'
```

```python
# apps/accounts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from .models import User, DonorProfile, SponsorProfile, ConsortiumPartner
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    DonorProfileSerializer, SponsorProfileSerializer,
    ConsortiumPartnerSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def donors(self, request):
        donors = User.objects.filter(role=User.Role.DONOR)
        serializer = self.get_serializer(donors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sponsors(self, request):
        sponsors = User.objects.filter(role=User.Role.SPONSOR)
        serializer = self.get_serializer(sponsors, many=True)
        return Response(serializer.data)


class DonorProfileViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    
    @action(detail=True, methods=['post'])
    def record_donation(self, request, pk=None):
        profile = self.get_object()
        amount = request.data.get('amount')
        # Logic to record donation, update totals
        # Trigger thank you email, receipt generation
        return Response({'status': 'donation recorded'})


class SponsorProfileViewSet(viewsets.ModelViewSet):
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer
    filterset_fields = ['level', 'is_active']
    
    @action(detail=True, methods=['get'])
    def deliverables(self, request, pk=None):
        sponsor = self.get_object()
        # Return content calendar, brand mentions, etc.
        return Response({
            'brand_mentions_this_month': 5,
            'content_pieces_remaining': sponsor.dedicated_content_pieces,
            'events_sponsored': sponsor.event_sponsorships
        })


class ConsortiumPartnerViewSet(viewsets.ModelViewSet):
    queryset = ConsortiumPartner.objects.filter(is_active=True)
    serializer_class = ConsortiumPartnerSerializer
```

---

## 4. Content App (Videos, Blogs, News)

```python
# apps/content/models.py
import uuid
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#0066CC')  # Hex color
    icon = models.CharField(max_length=50, blank=True)  # Icon class/name
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
    external_id = models.CharField(
        max_length=255,
        help_text="Video ID from platform (e.g., YouTube video ID, TikTok video ID)"
    )
    external_url = models.URLField()
    embed_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    
    # Content metadata
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    categories = models.ManyToManyField(Category, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Engagement metrics (cached from APIs)
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
    description = models.TextField()
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
    content = models.TextField()  # Rich text/HTML
    content_html = models.TextField(blank=True)  # Processed HTML
    
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
    search_vector = SearchVectorField(null=True, blank=True)
    
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
            GinIndex(fields=['search_vector']),
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['post_type', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
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
```

```python
# apps/content/serializers.py
from rest_framework import serializers
from .models import VideoContent, BlogPost, Playlist, Category, NewsItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoListSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoContent
        fields = [
            'id', 'title', 'slug', 'platform', 'platform_display',
            'content_type', 'content_type_display', 'thumbnail_url',
            'duration_seconds', 'view_count', 'is_featured', 'published_at'
        ]
    
    def get_thumbnail_url(self, obj):
        # Return cached thumbnail or generate from platform
        if obj.thumbnail_url:
            return obj.thumbnail_url
        # Fallback logic per platform
        return self._generate_thumbnail(obj)
    
    def _generate_thumbnail(self, video):
        if video.platform == VideoContent.Platform.YOUTUBE:
            return f"https://img.youtube.com/vi/{video.external_id}/maxresdefault.jpg"
        return ""


class VideoDetailSerializer(VideoListSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    sponsor_name = serializers.CharField(source='sponsored_by.company_name', read_only=True)
    embed_code = serializers.SerializerMethodField()
    
    class Meta(VideoListSerializer.Meta):
        fields = VideoListSerializer.Meta.fields + [
            'description', 'external_url', 'embed_code',
            'categories', 'author_name', 'sponsor_name',
            'like_count', 'share_count', 'comment_count'
        ]
    
    def get_embed_code(self, obj):
        if obj.platform == VideoContent.Platform.YOUTUBE:
            return f'<iframe src="https://www.youtube.com/embed/{obj.external_id}" frameborder="0" allowfullscreen></iframe>'
        elif obj.platform == VideoContent.Platform.TIKTOK:
            return f'<blockquote class="tiktok-embed" cite="{obj.external_url}" data-video-id="{obj.external_id}"></blockquote>'
        return ""


class PlaylistSerializer(serializers.ModelSerializer):
    video_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = '__all__'
    
    def get_video_count(self, obj):
        return obj.videos.filter(is_published=True).count()
    
    def get_total_duration(self, obj):
        total = obj.videos.filter(is_published=True).aggregate(
            total=models.Sum('duration_seconds')
        )['total'] or 0
        return total // 60  # Return minutes


class BlogPostListSerializer(serializers.ModelSerializer):
    post_type_display = serializers.CharField(source='get_post_type_display', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'post_type', 'post_type_display', 'author_name',
            'categories', 'read_time_minutes', 'published_at', 'view_count'
        ]


class BlogPostDetailSerializer(BlogPostListSerializer):
    content_html = serializers.CharField(read_only=True)
    related_videos = VideoListSerializer(many=True, read_only=True)
    sponsor_name = serializers.CharField(source='sponsored_by.company_name', read_only=True)
    
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            'content_html', 'meta_title', 'meta_description',
            'related_videos', 'sponsor_name', 'allow_comments'
        ]


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = '__all__'
```

```python
# apps/content/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import VideoContent, BlogPost, Playlist, Category, NewsItem
from .serializers import (
    VideoListSerializer, VideoDetailSerializer,
    BlogPostListSerializer, BlogPostDetailSerializer,
    PlaylistSerializer, CategorySerializer, NewsItemSerializer
)
from .tasks import fetch_video_metrics


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class VideoContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VideoContent.objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'content_type', 'categories', 'is_featured']
    search_fields = ['title', 'description']
    ordering_fields = ['published_at', 'view_count', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VideoDetailSerializer
        return VideoListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by playlist
        playlist = self.request.query_params.get('playlist', None)
        if playlist:
            queryset = queryset.filter(playlist__slug=playlist)
        
        # Exclude expired or future content
        queryset = queryset.filter(
            models.Q(published_at__lte=timezone.now()) | models.Q(published_at__isnull=True)
        )
        
        return queryset.select_related('author', 'playlist', 'sponsored_by').prefetch_related('categories')
    
    @action(detail=True, methods=['post'])
    def refresh_metrics(self, request, pk=None):
        """Admin endpoint to refresh video metrics from APIs"""
        video = self.get_object()
        fetch_video_metrics.delay(video.id)
        return Response({'status': 'metrics refresh queued'})
    
    @action(detail=False, methods=['get'])
    def by_platform(self, request):
        """Group videos by platform for the media hub tabs"""
        platforms = VideoContent.Platform.values
        result = {}
        for platform in platforms:
            videos = self.get_queryset().filter(platform=platform)[:12]
            result[platform] = VideoListSerializer(videos, many=True).data
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = VideoListSerializer(featured, many=True)
        return Response(serializer.data)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['post_type', 'categories', 'author']
    search_fields = ['title', 'excerpt', 'content', 'search_vector']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count on retrieve"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.get_queryset().filter(is_featured=True).first()
        if featured:
            serializer = BlogPostDetailSerializer(featured)
            return Response(serializer.data)
        return Response({'detail': 'No featured post'}, status=404)
    
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        post = self.get_object()
        related = post.related_posts.filter(status=BlogPost.Status.PUBLISHED)[:3]
        serializer = BlogPostListSerializer(related, many=True)
        return Response(serializer.data)


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def videos(self, request, slug=None):
        playlist = self.get_object()
        videos = playlist.videos.filter(is_published=True)
        serializer = VideoListSerializer(videos, many=True)
        return Response(serializer.data)


class NewsItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsItem.objects.filter(
        models.Q(expires_at__gt=timezone.now()) | models.Q(expires_at__isnull=True)
    )
    serializer_class = NewsItemSerializer
    
    @action(detail=False, methods=['get'])
    def breaking(self, request):
        breaking = self.get_queryset().filter(is_breaking=True)[:3]
        serializer = self.get_serializer(breaking, many=True)
        return Response(serializer.data)
```

---

## 5. Newsletter App

```python
# apps/newsletter/models.py
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


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
    source = models.CharField(max_length=50, blank=True)  # 'footer', 'popup', 'blog_inline', etc.
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
    name = models.CharField(max_length=255)  # Internal name
    subject = models.CharField(max_length=255)
    preheader = models.CharField(max_length=255, blank=True)  # Preview text
    
    campaign_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    # Content
    html_content = models.TextField()
    text_content = models.TextField(blank=True)
    
    # Featured content (auto-populated or manual)
    featured_video = models.ForeignKey(
        'content.VideoContent',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    featured_posts = models.ManyToManyField('content.BlogPost', blank=True)
    
    # Targeting
    target_preferences = ArrayField(
        models.CharField(max_length=20),
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
```

```python
# apps/newsletter/tasks.py
from celery import shared_task, group, chord
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.utils import timezone
from anymail.message import AnymailMessage
from .models import Subscriber, NewsletterCampaign, EmailLog


@shared_task(bind=True, max_retries=3)
def send_newsletter_campaign(self, campaign_id):
    """Main task to send a newsletter campaign"""
    try:
        campaign = NewsletterCampaign.objects.get(id=campaign_id)
        
        if campaign.status != NewsletterCampaign.Status.SCHEDULED:
            return {'error': 'Campaign not in scheduled status'}
        
        campaign.status = NewsletterCampaign.Status.SENDING
        campaign.save()
        
        # Get target subscribers
        subscribers = Subscriber.objects.filter(
            status=Subscriber.Status.ACTIVE
        )
        
        if campaign.target_preferences:
            subscribers = subscribers.filter(
                content_preference__in=campaign.target_preferences
            )
        
        campaign.total_recipients = subscribers.count()
        campaign.save()
        
        # Create email logs and send in batches
        batch_size = 100
        subscriber_ids = list(subscribers.values_list('id', flat=True))
        
        for i in range(0, len(subscriber_ids), batch_size):
            batch = subscriber_ids[i:i + batch_size]
            send_newsletter_batch.delay(campaign_id, batch)
        
        return {
            'status': 'queued',
            'total_batches': (len(subscriber_ids) // batch_size) + 1,
            'total_recipients': len(subscriber_ids)
        }
        
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_newsletter_batch(self, campaign_id, subscriber_ids):
    """Send to a batch of subscribers"""
    try:
        campaign = NewsletterCampaign.objects.get(id=campaign_id)
        subscribers = Subscriber.objects.filter(id__in=subscriber_ids)
        
        connection = get_connection()
        messages = []
        
        for subscriber in subscribers:
            # Create email log
            log, created = EmailLog.objects.get_or_create(
                campaign=campaign,
                subscriber=subscriber
            )
            
            # Personalize content
            context = {
                'subscriber': subscriber,
                'campaign': campaign,
                'unsubscribe_url': f"/newsletter/unsubscribe?token={subscriber.confirmation_token}",
                'view_online_url': f"/newsletter/archive/{campaign.id}"
            }
            
            html_content = render_to_string('newsletter/email_base.html', context)
            text_content = render_to_string('newsletter/email_base.txt', context)
            
            message = AnymailMessage(
                subject=campaign.subject,
                body=text_content,
                from_email="Budget Ndio Story <newsletter@budgetndiostory.org>",
                to=[subscriber.email],
                connection=connection
            )
            message.attach_alternative(html_content, "text/html")
            message.metadata = {'campaign_id': str(campaign_id), 'subscriber_id': str(subscriber.id)}
            message.track_opens = True
            message.track_clicks = True
            
            messages.append(message)
            subscriber.emails_sent += 1
        
        # Send all messages in this batch
        connection.send_messages(messages)
        
        # Update logs
        EmailLog.objects.filter(
            campaign=campaign,
            subscriber_id__in=subscriber_ids
        ).update(sent_at=timezone.now())
        
        return {'sent': len(messages)}
        
    except Exception as exc:
        self.retry(exc=exc, countdown=120)


@shared_task
def send_welcome_series(subscriber_id):
    """Automated welcome email sequence"""
    subscriber = Subscriber.objects.get(id=subscriber_id)
    
    # Welcome email 1: Immediate
    send_single_email.delay(
        subscriber_id=subscriber_id,
        template='newsletter/welcome_1.html',
        subject='Welcome to Budget Ndio Story!'
    )
    
    # Welcome email 2: Day 2 - Best content
    send_single_email.apply_async(
        args=[subscriber_id, 'newsletter/welcome_2.html', 'Start Here: Budget Basics'],
        countdown=86400  # 24 hours
    )
    
    # Welcome email 3: Day 5 - Engagement
    send_single_email.apply_async(
        args=[subscriber_id, 'newsletter/welcome_3.html', 'Join the Conversation'],
        countdown=432000  # 5 days
    )


@shared_task
def send_single_email(subscriber_id, template, subject):
    """Send a single transactional email"""
    subscriber = Subscriber.objects.get(id=subscriber_id)
    
    context = {'subscriber': subscriber}
    html_content = render_to_string(template, context)
    text_content = render_to_string(template.replace('.html', '.txt'), context)
    
    send_mail(
        subject=subject,
        message=text_content,
        from_email='Budget Ndio Story <newsletter@budgetndiostory.org>',
        recipient_list=[subscriber.email],
        html_message=html_content,
        fail_silently=False
    )


@shared_task
def update_subscriber_metrics():
    """Daily aggregation of subscriber engagement"""
    from django.db.models import Avg, Count
    
    active_subscribers = Subscriber.objects.filter(status=Subscriber.Status.ACTIVE)
    
    metrics = {
        'total_active': active_subscribers.count(),
        'avg_open_rate': active_subscribers.filter(emails_sent__gt=0).aggregate(
            avg=Avg('emails_opened' * 100.0 / 'emails_sent')
        )['avg'] or 0,
        'new_this_week': active_subscribers.filter(
            subscribed_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).count(),
    }
    
    # Store metrics or send to dashboard
    return metrics


@shared_task
def cleanup_bounced_emails():
    """Mark long-term bounced emails as inactive"""
    threshold = timezone.now() - timezone.timedelta(days=30)
    
    bounced = Subscriber.objects.filter(
        status=Subscriber.Status.BOUNCED,
        updated_at__lt=threshold
    ).update(status=Subscriber.Status.UNSUBSCRIBED)
    
    return {'cleaned': bounced}
```

---

## 6. Sponsors App (Donor Management)

```python
# apps/sponsors/models.py
from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid


class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')
    
    class PaymentMethod(models.TextChoices):
        MPESA = 'mpesa', _('M-Pesa')
        BANK = 'bank', _('Bank Transfer')
        CARD = 'card', _('Credit/Debit Card')
        PAYPAL = 'paypal', _('PayPal')
        CRYPTO = 'crypto', _('Cryptocurrency')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey(
        'accounts.DonorProfile',
        on_delete=models.CASCADE,
        related_name='donations'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Payment details
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_provider = models.CharField(max_length=50, blank=True)  # 'mpesa', 'stripe', etc.
    payment_metadata = models.JSONField(default=dict, blank=True)
    
    # Recurring
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=20,
        choices=[
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        blank=True
    )
    parent_donation = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='recurring_instances'
    )
    
    # Receipt
    receipt_number = models.CharField(max_length=50, blank=True, unique=True)
    receipt_sent = models.BooleanField(default=False)
    
    # Attribution
    campaign_source = models.CharField(max_length=100, blank=True)  # 'newsletter', 'video', etc.
    landing_page = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'sponsors_donation'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.donor.user.email} - {self.amount} {self.currency}"


class SponsorshipDeliverable(models.Model):
    """Track sponsor benefit fulfillment"""
    class Type(models.TextChoices):
        LOGO_DISPLAY = 'logo_display', _('Logo Display')
        DEDICATED_CONTENT = 'dedicated_content', _('Dedicated Content')
        EVENT_PRESENCE = 'event_presence', _('Event Presence')
        NEWSLETTER_MENTION = 'newsletter_mention', _('Newsletter Mention')
        SOCIAL_SHOUTOUT = 'social_shoutout', _('Social Media Shoutout')
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        OVERDUE = 'overdue', _('Overdue')
    
    sponsor = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.CASCADE,
        related_name='deliverables'
    )
    deliverable_type = models.CharField(max_length=20, choices=Type.choices)
    description = models.TextField()
    quantity_required = models.PositiveIntegerField(default=1)
    quantity_delivered = models.PositiveIntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Linked content
    linked_content = models.ManyToManyField(
        'content.BlogPost',
        blank=True,
        related_name='sponsor_deliverables'
    )
    linked_videos = models.ManyToManyField(
        'content.VideoContent',
        blank=True,
        related_name='sponsor_deliverables'
    )
    linked_newsletters = models.ManyToManyField(
        'newsletter.NewsletterCampaign',
        blank=True,
        related_name='sponsor_deliverables'
    )
    
    notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)  # Not shown to sponsor
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sponsors_deliverable'
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.sponsor.company_name} - {self.get_deliverable_type_display()}"


class SponsorAsset(models.Model):
    """Logos, brand guidelines, etc. provided by sponsors"""
    sponsor = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.CASCADE,
        related_name='assets'
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='sponsors/assets/')
    asset_type = models.CharField(
        max_length=50,
        choices=[
            ('logo', 'Logo'),
            ('guidelines', 'Brand Guidelines'),
            ('ad_creative', 'Ad Creative'),
            ('photo', 'Photo'),
            ('other', 'Other'),
        ]
    )
    is_primary = models.BooleanField(default=False)  # Primary logo to use
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sponsors_asset'
    
    def __str__(self):
        return f"{self.sponsor.company_name} - {self.name}"
```

---

## 7. Analytics App

```python
# apps/analytics/models.py
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
import uuid


class PageView(models.Model):
    """Track page views for content analytics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    path = models.CharField(max_length=500)
    content_type = models.CharField(max_length=50, blank=True)  # 'video', 'blog', 'news'
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
    
    # Device info (parsed from UA)
    device_type = models.CharField(max_length=20, blank=True)  # mobile, desktop, tablet
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Location (from IP)
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
    timestamp_seconds = models.PositiveIntegerField(default=0)  # Video position
    metadata = models.JSONField(default=dict, blank=True)  # Additional context
    
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
    source = models.CharField(max_length=100, blank=True)  # 'video_hub', 'newsletter', etc.
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_donorfunnel'
```

---

## 8. URLs Configuration

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Endpoints
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/content/', include('apps.content.urls')),
    path('api/v1/newsletter/', include('apps.newsletter.urls')),
    path('api/v1/sponsors/', include('apps.sponsors.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 9. Environment Configuration

```bash
# .env.example
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,api.budgetndiostory.org

# Database
DB_NAME=budget_ndio_db
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis/Celery
REDIS_URL=redis://localhost:6379/0

# Email (SendGrid)
SENDGRID_API_KEY=SG.xxx

# Social Media APIs
YOUTUBE_API_KEY=AIza...
TWITTER_BEARER_TOKEN=AAAA...
FACEBOOK_ACCESS_TOKEN=EAAG...
TIKTOK_ACCESS_TOKEN=act...

# Payment (M-Pesa Daraja)
MPESA_CONSUMER_KEY=xxx
MPESA_CONSUMER_SECRET=xxx
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
```

---

## 10. Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/production.txt requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: budget_ndio_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A config worker -l info
    volumes:
      - .:/app
    environment:
      - DEBUG=True
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A config beat -l info
    volumes:
      - .:/app
    environment:
      - DEBUG=True
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

---

## 11. Admin Configuration

```python
# apps/content/admin.py
from django.contrib import admin
from .models import VideoContent, BlogPost, Playlist, Category


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'content_type', 'is_published', 'view_count', 'published_at']
    list_filter = ['platform', 'content_type', 'is_published', 'is_featured']
    search_fields = ['title', 'description', 'external_id']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    actions = ['make_featured', 'refresh_metrics']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'description', 'content_type', 'categories')
        }),
        ('Platform Data', {
            'fields': ('platform', 'external_id', 'external_url', 'embed_url', 'thumbnail_url', 'duration_seconds')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_at', 'display_order')
        }),
        ('Engagement', {
            'fields': ('view_count', 'like_count', 'share_count', 'comment_count', 'last_metrics_update'),
            'classes': ('collapse',)
        }),
        ('Relations', {
            'fields': ('author', 'playlist', 'sponsored_by'),
        }),
    )
    
    @admin.action(description='Mark selected videos as featured')
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    
    @admin.action(description='Refresh metrics from platforms')
    def refresh_metrics(self, request, queryset):
        from .tasks import fetch_video_metrics
        for video in queryset:
            fetch_video_metrics.delay(video.id)
        self.message_user(request, f"Queued metrics refresh for {queryset.count()} videos")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'author', 'status', 'published_at', 'view_count']
    list_filter = ['post_type', 'status', 'categories', 'allow_comments']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    filter_horizontal = ['categories', 'related_videos', 'co_authors']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'content_html')
        }),
        ('Metadata', {
            'fields': ('post_type', 'categories', 'tags', 'featured_image', 'featured_image_caption')
        }),
        ('Authoring', {
            'fields': ('author', 'co_authors')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at', 'scheduled_publish_at', 'allow_comments')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Sponsorship', {
            'fields': ('sponsored_by',),
        }),
    )


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
```

---

## 12. Next.js Integration Guide

Your frontend already exists. Here's how to connect:

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchVideos(params: Record<string, string> = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`${API_URL}/content/videos/?${query}`);
  if (!res.ok) throw new Error('Failed to fetch videos');
  return res.json();
}

export async function fetchBlogPosts(params: Record<string, string> = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`${API_URL}/content/posts/?${query}`);
  if (!res.ok) throw new Error('Failed to fetch posts');
  return res.json();
}

export async function subscribeToNewsletter(email: string, preferences: object) {
  const res = await fetch(`${API_URL}/newsletter/subscribers/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, ...preferences }),
  });
  return res.json();
}
```

---

## Deployment Checklist

- [ ] Set up PostgreSQL 15+ (managed or self-hosted)
- [ ] Configure Redis for caching + Celery
- [ ] Set up Celery worker + beat scheduler
- [ ] Configure SendGrid for email
- [ ] Set up social media API keys
- [ ] Configure M-Pesa for donations (if using)
- [ ] Set up S3 or similar for media storage
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL certificates
- [ ] Configure monitoring (Sentry, Prometheus)
- [ ] Set up database backups
- [ ] Configure log rotation

This architecture gives you the "old school" reliability of Django with modern scalability through Celery for your newsletter and video processing needs.