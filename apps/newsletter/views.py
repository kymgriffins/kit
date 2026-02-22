from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
import uuid
from .models import Subscriber, NewsletterCampaign, EmailLog
from .serializers import (
    SubscriberSerializer, SubscriberCreateSerializer,
    NewsletterCampaignSerializer, NewsletterCampaignListSerializer,
    EmailLogSerializer
)


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriberCreateSerializer
        return SubscriberSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'confirm', 'unsubscribe']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        # Check if subscriber already exists
        existing = Subscriber.objects.filter(email=email).first()
        if existing:
            if existing.status == Subscriber.Status.ACTIVE:
                return Response({'message': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)
            elif existing.status == Subscriber.Status.PENDING:
                return Response({'message': 'Confirmation email resent'}, status=status.HTTP_200_OK)
        
        # Generate confirmation token
        token = str(uuid.uuid4())
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        subscriber = serializer.save()
        subscriber.confirmation_token = token
        subscriber.status = Subscriber.Status.PENDING
        subscriber.save()
        
        # TODO: Send confirmation email
        
        return Response({'message': 'Please check your email to confirm subscription'}, 
                        status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def confirm(self, request):
        token = request.data.get('token')
        subscriber = Subscriber.objects.filter(confirmation_token=token).first()
        
        if not subscriber:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        subscriber.status = Subscriber.Status.ACTIVE
        subscriber.confirmed_at = timezone.now()
        subscriber.subscribed_at = timezone.now()
        subscriber.confirmation_token = ''
        subscriber.save()
        
        return Response({'message': 'Subscription confirmed!'})
    
    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        token = request.data.get('token')
        subscriber = Subscriber.objects.filter(confirmation_token=token).first()
        
        if not subscriber:
            # Also allow unsubscribing by email
            email = request.data.get('email')
            subscriber = Subscriber.objects.filter(email=email).first()
        
        if not subscriber:
            return Response({'error': 'Subscriber not found'}, status=status.HTTP_404_NOT_FOUND)
        
        subscriber.status = Subscriber.Status.UNSUBSCRIBED
        subscriber.unsubscribed_at = timezone.now()
        subscriber.unsubscribe_reason = request.data.get('reason', '')
        subscriber.save()
        
        return Response({'message': 'Unsubscribed successfully'})


class NewsletterCampaignViewSet(viewsets.ModelViewSet):
    queryset = NewsletterCampaign.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NewsletterCampaignListSerializer
        return NewsletterCampaignSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        campaign_status = self.request.query_params.get('status', None)
        if campaign_status:
            queryset = queryset.filter(status=campaign_status)
        
        # Filter by type
        campaign_type = self.request.query_params.get('type', None)
        if campaign_type:
            queryset = queryset.filter(campaign_type=campaign_type)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        campaign = self.get_object()
        
        if campaign.status != NewsletterCampaign.Status.DRAFT:
            return Response({'error': 'Campaign cannot be sent in current status'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        campaign.status = NewsletterCampaign.Status.SCHEDULED
        campaign.scheduled_at = timezone.now()
        campaign.save()
        
        # TODO: Queue Celery task to send campaign
        
        return Response({'message': 'Campaign queued for sending'})


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        return queryset
