from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PageViewViewSet, VideoEngagementViewSet, DonorFunnelViewSet

router = DefaultRouter()
router.register(r'pageviews', PageViewViewSet, basename='pageview')
router.register(r'engagement', VideoEngagementViewSet, basename='engagement')
router.register(r'funnel', DonorFunnelViewSet, basename='funnel')

urlpatterns = [
    path('', include(router.urls)),
]
