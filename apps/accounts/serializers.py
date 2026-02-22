from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, DonorProfile, SponsorProfile, ConsortiumPartner, OrganizationProfile


class UserSerializer(serializers.ModelSerializer):
    """Full user serializer with all fields"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'role', 'role_display', 'phone', 'organization', 'bio', 'avatar',
            'is_verified', 'newsletter_subscribed', 'newsletter_preferences',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight user serializer for list views"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'role_display', 'organization', 'avatar', 'is_verified']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'organization', 'bio', 'avatar', 'newsletter_subscribed', 'newsletter_preferences']


class DonorProfileSerializer(serializers.ModelSerializer):
    """Full donor profile serializer with nested user"""
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    donor_type_display = serializers.CharField(source='get_donor_type_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DonorProfile
        fields = [
            'id', 'user', 'email', 'full_name', 'donor_type', 'donor_type_display',
            'tax_id', 'billing_address', 'total_donated', 'donation_count',
            'first_donation_date', 'last_donation_date', 'is_recurring_donor',
            'preferred_payment_method', 'communication_preferences', 'notes'
        ]
        read_only_fields = ['total_donated', 'donation_count', 'first_donation_date', 'last_donation_date']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()


class DonorProfileListSerializer(serializers.ModelSerializer):
    """Lightweight donor profile serializer"""
    email = serializers.EmailField(source='user.email', read_only=True)
    donor_type_display = serializers.CharField(source='get_donor_type_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DonorProfile
        fields = ['id', 'email', 'full_name', 'donor_type', 'donor_type_display', 'total_donated', 'donation_count', 'is_recurring_donor']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()


class SponsorProfileSerializer(serializers.ModelSerializer):
    """Full sponsor profile serializer with nested user"""
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    account_manager_name = serializers.SerializerMethodField()
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SponsorProfile
        fields = [
            'id', 'user', 'email', 'full_name', 'company_name', 'logo', 'website',
            'level', 'level_display', 'contract_value', 'contract_start', 'contract_end',
            'benefits_claimed', 'brand_visibility_slots', 'dedicated_content_pieces',
            'event_sponsorships', 'account_manager', 'account_manager_name', 'is_active'
        ]
    
    def get_account_manager_name(self, obj):
        if obj.account_manager:
            return obj.account_manager.get_full_name()
        return None
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()


class SponsorProfileListSerializer(serializers.ModelSerializer):
    """Lightweight sponsor profile serializer"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = SponsorProfile
        fields = ['id', 'company_name', 'logo', 'level', 'level_display', 'contract_value', 'is_active']


class ConsortiumPartnerSerializer(serializers.ModelSerializer):
    """Serializer for consortium partners"""
    contact_person_name = serializers.SerializerMethodField()
    contact_person_email = serializers.EmailField(source='contact_person.email', read_only=True)
    
    class Meta:
        model = ConsortiumPartner
        fields = [
            'id', 'name', 'slug', 'logo', 'description', 'website',
            'contact_person', 'contact_person_name', 'contact_person_email',
            'content_contribution_weight', 'joined_date', 'is_active'
        ]
    
    def get_contact_person_name(self, obj):
        if obj.contact_person:
            return obj.contact_person.get_full_name()
        return None


class ConsortiumPartnerListSerializer(serializers.ModelSerializer):
    """Lightweight consortium partner serializer"""
    
    class Meta:
        model = ConsortiumPartner
        fields = ['id', 'name', 'slug', 'logo', 'is_active']


class OrganizationProfileSerializer(serializers.ModelSerializer):
    """Serializer for organization profile - Budget Ndio Story"""
    
    class Meta:
        model = OrganizationProfile
        fields = [
            # Basic Info
            'id', 'organization_name', 'consortium_name', 'tagline', 'brand_promise', 'description',
            
            # Vision & Mission
            'vision', 'mission',
            
            # Location & Registration
            'headquarters', 'registration_country', 'year_established',
            
            # Contact Info
            'email_general', 'email_partnerships', 'email_media', 'phone', 'website',
            
            # Social Media
            'tiktok', 'instagram', 'twitter', 'youtube', 'facebook',
            
            # Brand Identity
            'primary_color', 'secondary_color', 'alert_color', 'success_color', 'neutral_dark', 'neutral_light',
            
            # Impact Statistics
            'countries_reached', 'budget_reports_analyzed', 'citizens_engaged',
            'youth_champion_trainings', 'partner_organizations', 'programs_delivered',
            
            # Governance
            'is_independent', 'is_non_partisan', 'document_version', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class OrganizationProfilePublicSerializer(serializers.ModelSerializer):
    """Public serializer for organization profile - excludes sensitive fields"""
    
    class Meta:
        model = OrganizationProfile
        fields = [
            # Basic Info
            'organization_name', 'consortium_name', 'tagline', 'brand_promise', 'description',
            
            # Vision & Mission
            'vision', 'mission',
            
            # Location & Registration
            'headquarters', 'registration_country', 'year_established',
            
            # Contact Info
            'email_general', 'email_partnerships', 'email_media', 'website',
            
            # Social Media
            'tiktok', 'instagram', 'twitter', 'youtube', 'facebook',
            
            # Brand Identity
            'primary_color', 'secondary_color', 'alert_color', 'success_color', 'neutral_dark', 'neutral_light',
            
            # Impact Statistics
            'countries_reached', 'budget_reports_analyzed', 'citizens_engaged',
            'youth_champion_trainings', 'partner_organizations', 'programs_delivered',
        ]


class ImpactStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for impact statistics"""
    
    class Meta:
        model = OrganizationProfile
        fields = [
            'countries_reached', 'budget_reports_analyzed', 'citizens_engaged',
            'youth_champion_trainings', 'partner_organizations', 'programs_delivered'
        ]


class BrandIdentitySerializer(serializers.ModelSerializer):
    """Serializer for brand identity - colors and typography"""
    
    class Meta:
        model = OrganizationProfile
        fields = [
            'organization_name', 'tagline',
            'primary_color', 'secondary_color', 'alert_color', 'success_color', 'neutral_dark', 'neutral_light'
        ]


class ContactInfoSerializer(serializers.ModelSerializer):
    """Serializer for contact information"""
    
    class Meta:
        model = OrganizationProfile
        fields = [
            'organization_name', 'headquarters',
            'email_general', 'email_partnerships', 'email_media', 'phone', 'website',
            'tiktok', 'instagram', 'twitter', 'youtube', 'facebook'
        ]
