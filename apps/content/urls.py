from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, VideoContentViewSet, BlogPostViewSet,
    PlaylistViewSet, NewsItemViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'videos', VideoContentViewSet, basename='video')
router.register(r'posts', BlogPostViewSet, basename='post')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'news', NewsItemViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
]
