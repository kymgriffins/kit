from django.contrib import admin
from .models import Donation, SponsorshipDeliverable, SponsorAsset


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'amount', 'currency', 'payment_method', 'status', 'is_recurring', 'transaction_id', 'created_at']
    list_filter = ['status', 'payment_method', 'currency', 'is_recurring']
    search_fields = ['donor__user__email', 'transaction_id', 'receipt_number']
    raw_id_fields = ['donor', 'parent_donation']
    readonly_fields = ['receipt_number', 'created_at', 'completed_at']
    ordering = ['-created_at']


@admin.register(SponsorshipDeliverable)
class SponsorshipDeliverableAdmin(admin.ModelAdmin):
    list_display = ['sponsor', 'deliverable_type', 'quantity_required', 'quantity_delivered', 'status', 'due_date']
    list_filter = ['deliverable_type', 'status']
    search_fields = ['sponsor__company_name', 'description']
    raw_id_fields = ['sponsor']
    filter_horizontal = ['linked_content', 'linked_videos', 'linked_newsletters']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['due_date']


@admin.register(SponsorAsset)
class SponsorAssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'sponsor', 'asset_type', 'is_primary', 'uploaded_at']
    list_filter = ['asset_type', 'is_primary']
    search_fields = ['name', 'sponsor__company_name']
    raw_id_fields = ['sponsor']
    readonly_fields = ['uploaded_at']
