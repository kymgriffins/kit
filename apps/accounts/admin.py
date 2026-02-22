from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DonorProfile, SponsorProfile, ConsortiumPartner, OrganizationProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'organization']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('role', 'phone', 'organization', 'bio', 'avatar', 'is_verified')}),
        ('Newsletter', {'fields': ('newsletter_subscribed', 'newsletter_preferences')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile Info', {'fields': ('role', 'email')}),
    )


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'donor_type', 'total_donated', 'donation_count', 'is_recurring_donor', 'first_donation_date']
    list_filter = ['donor_type', 'is_recurring_donor']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'tax_id']
    raw_id_fields = ['user']


@admin.register(SponsorProfile)
class SponsorProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'level', 'contract_value', 'contract_start', 'contract_end', 'is_active']
    list_filter = ['level', 'is_active']
    search_fields = ['company_name', 'user__email', 'website']
    raw_id_fields = ['user', 'account_manager']
    readonly_fields = ['brand_visibility_slots', 'dedicated_content_pieces', 'event_sponsorships']


@admin.register(ConsortiumPartner)
class ConsortiumPartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'content_contribution_weight', 'joined_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['contact_person']


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'consortium_name', 'headquarters', 'year_established']
    search_fields = ['organization_name', 'consortium_name', 'tagline']
