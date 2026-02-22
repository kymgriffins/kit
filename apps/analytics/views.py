from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import PageView, VideoEngagement, DonorFunnel
from .serializers import (
    PageViewSerializer, VideoEngagementSerializer, DonorFunnelSerializer
)


class PageViewViewSet(viewsets.ModelViewSet):
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by content type
        content_type = self.request.query_params.get('content_type', None)
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        total_views = PageView.objects.count()
        views_this_week = PageView.objects.filter(created_at__gte=week_ago).count()
        
        # Top pages
        top_pages = PageView.objects.values('path').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        return Response({
            'total_views': total_views,
            'views_this_week': views_this_week,
            'top_pages': list(top_pages)
        })


class VideoEngagementViewSet(viewsets.ModelViewSet):
    queryset = VideoEngagement.objects.all()
    serializer_class = VideoEngagementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        video_id = self.request.query_params.get('video', None)
        if video_id:
            queryset = queryset.filter(video_id=video_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_video(self, request):
        video_id = request.query_params.get('video_id')
        if not video_id:
            return Response({'error': 'video_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        engagements = VideoEngagement.objects.filter(video_id=video_id)
        
        # Aggregate by event type
        by_event = engagements.values('event_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'total_events': engagements.count(),
            'by_event_type': list(by_event)
        })


class DonorFunnelViewSet(viewsets.ModelViewSet):
    queryset = DonorFunnel.objects.all()
    serializer_class = DonorFunnelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        donor_id = self.request.query_params.get('donor', None)
        if donor_id:
            queryset = queryset.filter(donor_id=donor_id)
        
        stage = self.request.query_params.get('stage', None)
        if stage:
            queryset = queryset.filter(stage=stage)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def funnel_summary(self, request):
        summary = DonorFunnel.objects.values('stage').annotate(
            count=Count('id'),
            total_value=Sum('value')
        ).order_by('stage')
        
        return Response({
            'funnel_stages': list(summary)
        })
