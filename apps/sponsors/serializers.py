from rest_framework import serializers
from .models import Donation, SponsorshipDeliverable, SponsorAsset
from apps.accounts.serializers import UserSerializer, SponsorProfileListSerializer


class DonationSerializer(serializers.ModelSerializer):
    """Full donation serializer with all fields"""
    donor_email = serializers.EmailField(source='donor.user.email', read_only=True)
    donor_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    recurring_frequency_display = serializers.CharField(source='get_recurring_frequency_display', read_only=True)
    is_recurring_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Donation
        fields = [
            'id', 'donor', 'donor_email', 'donor_name',
            'amount', 'currency', 'payment_method', 'payment_method_display',
            'status', 'status_display',
            'transaction_id', 'payment_provider', 'payment_metadata',
            'is_recurring', 'is_recurring_display', 'recurring_frequency', 'recurring_frequency_display',
            'parent_donation', 'recurring_instances',
            'receipt_number', 'receipt_sent',
            'campaign_source', 'landing_page',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'receipt_number', 'created_at', 'completed_at']
    
    def get_donor_name(self, obj):
        return obj.donor.user.get_full_name()
    
    def get_is_recurring_display(self, obj):
        return 'Recurring' if obj.is_recurring else 'One-time'


class DonationListSerializer(serializers.ModelSerializer):
    """Lightweight donation serializer for list views"""
    donor_email = serializers.EmailField(source='donor.user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Donation
        fields = [
            'id', 'donor_email', 'amount', 'currency',
            'payment_method', 'payment_method_display',
            'status', 'status_display', 'is_recurring',
            'receipt_number', 'created_at'
        ]


class DonationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating donations"""
    
    class Meta:
        model = Donation
        fields = [
            'donor', 'amount', 'currency', 'payment_method',
            'is_recurring', 'recurring_frequency', 'campaign_source', 'landing_page'
        ]


class DonationAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for donation analytics"""
    donor_email = serializers.EmailField(source='donor.user.email', read_only=True)
    donor_type = serializers.CharField(source='donor.donor_type', read_only=True)
    
    class Meta:
        model = Donation
        fields = [
            'id', 'donor_email', 'donor_type', 'amount', 'currency',
            'payment_method', 'status', 'is_recurring', 'campaign_source', 'created_at'
        ]


class SponsorshipDeliverableSerializer(serializers.ModelSerializer):
    """Full sponsorship deliverable serializer with all fields"""
    deliverable_type_display = serializers.CharField(source='get_deliverable_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    sponsor_name = serializers.CharField(source='sponsor.company_name', read_only=True)
    sponsor_level = serializers.CharField(source='sponsor.level', read_only=True)
    linked_content_titles = serializers.SerializerMethodField()
    linked_videos_titles = serializers.SerializerMethodField()
    linked_newsletters_titles = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = SponsorshipDeliverable
        fields = [
            'id', 'sponsor', 'sponsor_name', 'sponsor_level',
            'deliverable_type', 'deliverable_type_display',
            'description', 'quantity_required', 'quantity_delivered',
            'status', 'status_display', 'due_date', 'completed_date',
            'linked_content', 'linked_content_titles',
            'linked_videos', 'linked_videos_titles',
            'linked_newsletters', 'linked_newsletters_titles',
            'notes', 'internal_notes',
            'is_completed', 'completion_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_linked_content_titles(self, obj):
        return [{'id': str(p.id), 'title': p.title, 'slug': p.slug} for p in obj.linked_content.all()]
    
    def get_linked_videos_titles(self, obj):
        return [{'id': str(v.id), 'title': v.title, 'slug': v.slug} for v in obj.linked_videos.all()]
    
    def get_linked_newsletters_titles(self, obj):
        return [{'id': str(n.id), 'subject': n.subject} for n in obj.linked_newsletters.all()]
    
    def get_is_completed(self, obj):
        return obj.status == SponsorshipDeliverable.Status.COMPLETED
    
    def get_completion_percentage(self, obj):
        if obj.quantity_required > 0:
            return round((obj.quantity_delivered / obj.quantity_required) * 100, 2)
        return 0


class SponsorshipDeliverableListSerializer(serializers.ModelSerializer):
    """Lightweight sponsorship deliverable serializer"""
    deliverable_type_display = serializers.CharField(source='get_deliverable_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    sponsor_name = serializers.CharField(source='sponsor.company_name', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = SponsorshipDeliverable
        fields = [
            'id', 'sponsor_name', 'deliverable_type', 'deliverable_type_display',
            'quantity_required', 'quantity_delivered', 'status', 'status_display',
            'due_date', 'is_overdue'
        ]
    
    def get_is_overdue(self, obj):
        from django.utils import timezone
        if obj.status != SponsorshipDeliverable.Status.COMPLETED and obj.due_date < timezone.now().date():
            return True
        return False


class SponsorshipDeliverableCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating sponsorship deliverables"""
    
    class Meta:
        model = SponsorshipDeliverable
        fields = [
            'sponsor', 'deliverable_type', 'description',
            'quantity_required', 'due_date', 'linked_content',
            'linked_videos', 'linked_newsletters', 'notes'
        ]


class SponsorAssetSerializer(serializers.ModelSerializer):
    """Full sponsor asset serializer with all fields"""
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)
    sponsor_name = serializers.CharField(source='sponsor.company_name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SponsorAsset
        fields = [
            'id', 'sponsor', 'sponsor_name', 'name', 'file', 'file_url',
            'asset_type', 'asset_type_display', 'is_primary', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class SponsorAssetListSerializer(serializers.ModelSerializer):
    """Lightweight sponsor asset serializer"""
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)
    
    class Meta:
        model = SponsorAsset
        fields = ['id', 'name', 'asset_type', 'asset_type_display', 'is_primary', 'uploaded_at']


class SponsorAssetCreateSerializer(serializers.ModelSerializer):
    """Serializer for uploading sponsor assets"""
    
    class Meta:
        model = SponsorAsset
        fields = ['sponsor', 'name', 'file', 'asset_type', 'is_primary']


class SponsorDashboardSerializer(serializers.Serializer):
    """Serializer for sponsor dashboard statistics"""
    total_sponsors = serializers.IntegerField()
    active_sponsors = serializers.IntegerField()
    total_contract_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    deliverables_pending = serializers.IntegerField()
    deliverables_completed = serializers.IntegerField()
    deliverables_overdue = serializers.IntegerField()
    top_sponsors = serializers.ListField()
    sponsors_by_level = serializers.DictField()
