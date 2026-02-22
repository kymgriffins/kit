from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriberViewSet, NewsletterCampaignViewSet, EmailLogViewSet

router = DefaultRouter()
router.register(r'subscribers', SubscriberViewSet, basename='subscriber')
router.register(r'campaigns', NewsletterCampaignViewSet, basename='campaign')
router.register(r'logs', EmailLogViewSet, basename='emaillog')

urlpatterns = [
    path('', include(router.urls)),
]
