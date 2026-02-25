from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models
from .models import VideoContent, BlogPost, Playlist, Category, NewsItem
from .serializers import (
    VideoListSerializer, VideoDetailSerializer,
    BlogPostListSerializer, BlogPostDetailSerializer,
    PlaylistSerializer, CategorySerializer, NewsItemSerializer
)


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
    
    @action(detail=False, methods=['get'])
    def by_platform(self, request):
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
    search_fields = ['title', 'excerpt', 'content']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        # Get the latest published post as featured
        featured = self.get_queryset().first()
        if featured:
            serializer = BlogPostDetailSerializer(featured)
            return Response(serializer.data)
        return Response({'detail': 'No posts available'}, status=404)
    
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
