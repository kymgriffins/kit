from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationViewSet, SponsorshipDeliverableViewSet, SponsorAssetViewSet

router = DefaultRouter()
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'deliverables', SponsorshipDeliverableViewSet, basename='deliverable')
router.register(r'assets', SponsorAssetViewSet, basename='asset')

urlpatterns = [
    path('', include(router.urls)),
]
