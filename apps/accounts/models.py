import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        EDITOR = 'editor', _('Content Editor')
        VIEWER = 'viewer', _('Viewer')
        DONOR = 'donor', _('Donor')
        SPONSOR = 'sponsor', _('Sponsor')
        PARTNER = 'partner', _('Consortium Partner')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Newsletter preferences
    newsletter_subscribed = models.BooleanField(default=False)
    newsletter_preferences = models.JSONField(default=dict, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'accounts_user'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class DonorProfile(models.Model):
    class DonorType(models.TextChoices):
        INDIVIDUAL = 'individual', _('Individual')
        CORPORATE = 'corporate', _('Corporate')
        FOUNDATION = 'foundation', _('Foundation')
        INSTITUTIONAL = 'institutional', _('Institutional')
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='donor_profile'
    )
    donor_type = models.CharField(max_length=20, choices=DonorType.choices)
    tax_id = models.CharField(max_length=50, blank=True)
    billing_address = models.TextField(blank=True)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    donation_count = models.PositiveIntegerField(default=0)
    first_donation_date = models.DateField(null=True, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_recurring_donor = models.BooleanField(default=False)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    communication_preferences = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'accounts_donor_profile'
    
    def __str__(self):
        return f"Donor: {self.user.email}"


class SponsorProfile(models.Model):
    class SponsorshipLevel(models.TextChoices):
        BRONZE = 'bronze', _('Bronze Partner')
        SILVER = 'silver', _('Silver Partner')
        GOLD = 'gold', _('Gold Partner')
        PLATINUM = 'platinum', _('Platinum Partner')
        STRATEGIC = 'strategic', _('Strategic Partner')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='sponsor_profile'
    )
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/logos/', blank=True)
    website = models.URLField(blank=True)
    level = models.CharField(max_length=20, choices=SponsorshipLevel.choices)
    contract_value = models.DecimalField(max_digits=12, decimal_places=2)
    contract_start = models.DateField()
    contract_end = models.DateField()
    benefits_claimed = models.JSONField(default=list, blank=True)
    brand_visibility_slots = models.PositiveIntegerField(default=0)
    dedicated_content_pieces = models.PositiveIntegerField(default=0)
    event_sponsorships = models.PositiveIntegerField(default=0)
    account_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_sponsors'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'accounts_sponsor_profile'
        ordering = ['-contract_value']
    
    def __str__(self):
        return f"{self.company_name} ({self.get_level_display()})"


class ConsortiumPartner(models.Model):
    """The Continental Pot, Colour Twist Media, Sen Media"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='partners/', blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_partners'
    )
    content_contribution_weight = models.PositiveSmallIntegerField(
        default=1,
        help_text="For revenue sharing calculations"
    )
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'accounts_consortium_partner'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class OrganizationProfile(models.Model):
    """Organization profile for Budget Ndio Story"""
    
    # Basic Info
    organization_name = models.CharField(max_length=255, default='Budget Ndio Story')
    consortium_name = models.CharField(max_length=100, default='BNSCLIENT1')
    tagline = models.CharField(max_length=255, default='Follow the Budget. Find the Story.')
    brand_promise = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    # Vision & Mission
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    
    # Location & Registration
    headquarters = models.CharField(max_length=255, default='Nairobi, Kenya')
    registration_country = models.CharField(max_length=100, default='Kenya')
    year_established = models.PositiveSmallIntegerField(default=2024)
    
    # Contact Info
    email_general = models.EmailField(blank=True)
    email_partnerships = models.EmailField(blank=True)
    email_media = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    
    # Social Media
    tiktok = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    youtube = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    
    # Brand Identity
    primary_color = models.CharField(max_length=7, default='#0066CC')
    secondary_color = models.CharField(max_length=7, default='#00A6A6')
    alert_color = models.CharField(max_length=7, default='#FF6B35')
    success_color = models.CharField(max_length=7, default='#2ECC71')
    neutral_dark = models.CharField(max_length=7, default='#1A1A2E')
    neutral_light = models.CharField(max_length=7, default='#F8F9FA')
    
    # Impact Statistics
    countries_reached = models.PositiveIntegerField(default=47)
    budget_reports_analyzed = models.PositiveIntegerField(default=500)
    citizens_engaged = models.PositiveIntegerField(default=15000)
    youth_champion_trainings = models.PositiveIntegerField(default=120)
    partner_organizations = models.PositiveIntegerField(default=200)
    programs_delivered = models.PositiveIntegerField(default=120)
    
    # Governance
    is_independent = models.BooleanField(default=True)
    is_non_partisan = models.BooleanField(default=True)
    document_version = models.CharField(max_length=20, default='1.0')
    last_updated = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_organization_profile'
        verbose_name = 'Organization Profile'
        verbose_name_plural = 'Organization Profiles'
    
    def __str__(self):
        return self.organization_name
