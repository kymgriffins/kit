from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, Count
from django.utils import timezone
import uuid
from django.shortcuts import render
from .models import Donation, SponsorshipDeliverable, SponsorAsset
from .serializers import (
    DonationSerializer, DonationCreateSerializer,
    SponsorshipDeliverableSerializer, SponsorAssetSerializer
)


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DonationCreateSerializer
        return DonationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        donation_status = self.request.query_params.get('status', None)
        if donation_status:
            queryset = queryset.filter(status=donation_status)
        
        # Filter by donor
        donor_id = self.request.query_params.get('donor', None)
        if donor_id:
            queryset = queryset.filter(donor_id=donor_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Donation.objects.filter(status=Donation.Status.COMPLETED).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        return Response({
            'total_raised': total['total'] or 0,
            'donation_count': total['count'] or 0,
            'currency': 'KES'
        })


class SponsorshipDeliverableViewSet(viewsets.ModelViewSet):
    queryset = SponsorshipDeliverable.objects.all()
    serializer_class = SponsorshipDeliverableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        deliverable_status = self.request.query_params.get('status', None)
        if deliverable_status:
            queryset = queryset.filter(status=deliverable_status)
        
        # Filter by sponsor
        sponsor_id = self.request.query_params.get('sponsor', None)
        if sponsor_id:
            queryset = queryset.filter(sponsor_id=sponsor_id)
        
        return queryset


class SponsorAssetViewSet(viewsets.ModelViewSet):
    queryset = SponsorAsset.objects.all()
    serializer_class = SponsorAssetSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_sponsor(self, request):
        sponsor_id = request.query_params.get('sponsor_id')
        if sponsor_id:
            assets = SponsorAsset.objects.filter(sponsor_id=sponsor_id)
            serializer = self.get_serializer(assets, many=True)
            return Response(serializer.data)
        return Response({'error': 'sponsor_id required'}, status=status.HTTP_400_BAD_REQUEST)


def donate_view(request):
    """Public donation form view"""
    return render(request, 'public/donate.html')
