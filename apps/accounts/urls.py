from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, DonorProfileViewSet, SponsorProfileViewSet, 
    ConsortiumPartnerViewSet, OrganizationProfileViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'donors', DonorProfileViewSet, basename='donor')
router.register(r'sponsors', SponsorProfileViewSet, basename='sponsor')
router.register(r'partners', ConsortiumPartnerViewSet, basename='partner')
router.register(r'organization', OrganizationProfileViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
]
