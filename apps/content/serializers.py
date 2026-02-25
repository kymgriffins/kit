from rest_framework import serializers
from .models import VideoContent, BlogPost, Playlist, Category, NewsItem


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for content categories"""
    video_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 'icon', 'order', 'is_active', 'video_count', 'post_count']
    
    def get_video_count(self, obj):
        return obj.videocontent_set.filter(is_published=True).count()
    
    def get_post_count(self, obj):
        return obj.blogpost_set.filter(status='published').count()


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight category serializer"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'icon', 'is_active']


class VideoListSerializer(serializers.ModelSerializer):
    """Lightweight video serializer for list views"""
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoContent
        fields = [
            'id', 'title', 'slug', 'platform', 'platform_display',
            'content_type', 'content_type_display', 'thumbnail_url',
            'duration_seconds', 'view_count', 'like_count', 'is_featured', 
            'author_name', 'published_at'
        ]
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail_url:
            return obj.thumbnail_url
        if obj.platform == VideoContent.Platform.YOUTUBE:
            return f"https://img.youtube.com/vi/{obj.external_id}/maxresdefault.jpg"
        return ""
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return None


class VideoDetailSerializer(VideoListSerializer):
    """Detailed video serializer with all information"""
    categories = CategoryListSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    sponsor_name = serializers.SerializerMethodField()
    playlist_title = serializers.CharField(source='playlist.title', read_only=True)
    embed_code = serializers.SerializerMethodField()
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)
    
    class Meta(VideoListSerializer.Meta):
        fields = VideoListSerializer.Meta.fields + [
            'description', 'external_id', 'external_url', 'embed_code',
            'categories', 'author', 'author_name', 'sponsor_name', 'playlist_title',
            'like_count', 'share_count', 'comment_count', 'last_metrics_update',
            'is_published', 'display_order', 'created_at', 'updated_at'
        ]
    
    def get_author(self, obj):
        if obj.author:
            return {
                'id': str(obj.author.id),
                'name': obj.author.get_full_name(),
                'email': obj.author.email
            }
        return None
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return None
    
    def get_sponsor_name(self, obj):
        if obj.sponsored_by:
            return obj.sponsored_by.company_name
        return None
    
    def get_embed_code(self, obj):
        if obj.platform == VideoContent.Platform.YOUTUBE:
            return f'<iframe src="https://www.youtube.com/embed/{obj.external_id}" frameborder="0" allowfullscreen></iframe>'
        elif obj.platform == VideoContent.Platform.TIKTOK:
            return f'<blockquote class="tiktok-embed" cite="{obj.external_url}" data-video-id="{obj.external_id}"></blockquote>'
        return ""


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer for video playlists"""
    videos = VideoListSerializer(many=True, read_only=True)
    video_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail',
            'is_featured', 'difficulty_level', 'estimated_duration_minutes',
            'videos', 'video_count', 'total_duration', 'created_at'
        ]
    
    def get_video_count(self, obj):
        return obj.videos.filter(is_published=True).count()
    
    def get_total_duration(self, obj):
        total = obj.videos.filter(is_published=True).aggregate(
            total=models.Sum('duration_seconds')
        )['total'] or 0
        return total // 60


class PlaylistListSerializer(serializers.ModelSerializer):
    """Lightweight playlist serializer"""
    video_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'slug', 'thumbnail', 'is_featured', 'difficulty_level', 'video_count']
    
    def get_video_count(self, obj):
        return obj.videos.filter(is_published=True).count()


class BlogPostListSerializer(serializers.ModelSerializer):
    """Lightweight blog post serializer for list views"""
    post_type_display = serializers.CharField(source='get_post_type_display', read_only=True)
    author_name = serializers.SerializerMethodField()
    categories = CategoryListSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'post_type', 'post_type_display', 'status', 'status_display',
            'author_name', 'categories', 'read_time_minutes', 
            'published_at', 'view_count'
        ]
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return None


class BlogPostDetailSerializer(BlogPostListSerializer):
    """Detailed blog post serializer with full content"""
    author = serializers.SerializerMethodField()
    co_authors = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    related_videos = VideoListSerializer(many=True, read_only=True)
    related_posts = serializers.SerializerMethodField()
    sponsor = serializers.SerializerMethodField()
    post_type_display = serializers.CharField(source='get_post_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            'content_html', 'content', 'author', 'co_authors',
            'meta_title', 'meta_description', 'og_image',
            'related_videos', 'related_posts', 'sponsor',
            'allow_comments', 'status', 'status_display',
            'scheduled_publish_at', 'created_at', 'updated_at'
        ]
    
    def get_author(self, obj):
        if obj.author:
            return {
                'id': str(obj.author.id),
                'name': obj.author.get_full_name(),
                'email': obj.author.email,
                'avatar': obj.author.avatar.url if obj.author.avatar else None
            }
        return None
    
    def get_co_authors(self, obj):
        return [{'id': str(u.id), 'name': u.get_full_name()} for u in obj.co_authors.all()]
    
    def get_related_posts(self, obj):
        return [{'id': str(p.id), 'title': p.title, 'slug': p.slug} for p in obj.related_posts.all()]
    
    def get_sponsor(self, obj):
        if obj.sponsored_by:
            return {
                'id': str(obj.sponsored_by.id),
                'company_name': obj.sponsored_by.company_name,
                'logo': obj.sponsored_by.logo.url if obj.sponsored_by.logo else None
            }
        return None


class NewsItemSerializer(serializers.ModelSerializer):
    """Serializer for news items"""
    time_since_published = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsItem
        fields = [
            'id', 'title', 'slug', 'content', 'source_url',
            'is_breaking', 'published_at', 'expires_at', 'time_since_published'
        ]
    
    def get_time_since_published(self, obj):
        from django.utils import timezone
        from django.utils.timesince import timesince
        return timesince(obj.published_at, timezone.now())


class NewsItemListSerializer(serializers.ModelSerializer):
    """Lightweight news item serializer"""
    
    class Meta:
        model = NewsItem
        fields = ['id', 'title', 'slug', 'is_breaking', 'published_at']
