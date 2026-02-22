from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from .models import User, DonorProfile, SponsorProfile, ConsortiumPartner, OrganizationProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    DonorProfileSerializer, SponsorProfileSerializer,
    ConsortiumPartnerSerializer, OrganizationProfileSerializer,
    OrganizationProfilePublicSerializer, ImpactStatisticsSerializer,
    BrandIdentitySerializer, ContactInfoSerializer
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
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
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def record_donation(self, request, pk=None):
        profile = self.get_object()
        amount = request.data.get('amount')
        
        if amount:
            from django.utils import timezone
            from decimal import Decimal
            
            profile.total_donated += Decimal(str(amount))
            profile.donation_count += 1
            profile.last_donation_date = timezone.now().date()
            
            if not profile.first_donation_date:
                profile.first_donation_date = timezone.now().date()
            
            profile.save()
            
            return Response({
                'status': 'donation recorded',
                'total_donated': profile.total_donated,
                'donation_count': profile.donation_count
            })
        
        return Response({'error': 'Amount required'}, status=status.HTTP_400_BAD_REQUEST)


class SponsorProfileViewSet(viewsets.ModelViewSet):
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer
    filterset_fields = ['level', 'is_active']
    
    @action(detail=True, methods=['get'])
    def deliverables(self, request, pk=None):
        sponsor = self.get_object()
        return Response({
            'brand_mentions_this_month': 5,
            'content_pieces_remaining': sponsor.dedicated_content_pieces,
            'events_sponsored': sponsor.event_sponsorships,
            'brand_visibility_slots': sponsor.brand_visibility_slots
        })


class ConsortiumPartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConsortiumPartner.objects.filter(is_active=True)
    serializer_class = ConsortiumPartnerSerializer
    lookup_field = 'slug'


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for organization profile - Budget Ndio Story"""
    queryset = OrganizationProfile.objects.all()
    serializer_class = OrganizationProfileSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationProfilePublicSerializer
        return OrganizationProfileSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        """Get public organization profile"""
        profile = OrganizationProfile.objects.first()
        if profile:
            serializer = OrganizationProfilePublicSerializer(profile)
            return Response(serializer.data)
        return Response({'error': 'No profile found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def impact(self, request):
        """Get impact statistics"""
        profile = OrganizationProfile.objects.first()
        if profile:
            serializer = ImpactStatisticsSerializer(profile)
            return Response(serializer.data)
        return Response({'error': 'No profile found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def brand(self, request):
        """Get brand identity"""
        profile = OrganizationProfile.objects.first()
        if profile:
            serializer = BrandIdentitySerializer(profile)
            return Response(serializer.data)
        return Response({'error': 'No profile found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def contact(self, request):
        """Get contact information"""
        profile = OrganizationProfile.objects.first()
        if profile:
            serializer = ContactInfoSerializer(profile)
            return Response(serializer.data)
        return Response({'error': 'No profile found'}, status=status.HTTP_404_NOT_FOUND)
