from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
import uuid


class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')
    
    class PaymentMethod(models.TextChoices):
        MPESA = 'mpesa', _('M-Pesa')
        BANK = 'bank', _('Bank Transfer')
        CARD = 'card', _('Credit/Debit Card')
        PAYPAL = 'paypal', _('PayPal')
        CRYPTO = 'crypto', _('Cryptocurrency')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey(
        'accounts.DonorProfile',
        on_delete=models.CASCADE,
        related_name='donations'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Payment details
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_provider = models.CharField(max_length=50, blank=True)
    payment_metadata = models.JSONField(default=dict, blank=True)
    
    # Recurring
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=20,
        choices=[
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        blank=True
    )
    parent_donation = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='recurring_instances'
    )
    
    # Receipt
    receipt_number = models.CharField(max_length=50, blank=True, unique=True)
    receipt_sent = models.BooleanField(default=False)
    
    # Attribution
    campaign_source = models.CharField(max_length=100, blank=True)
    landing_page = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'sponsors_donation'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.donor.user.email} - {self.amount} {self.currency}"


class SponsorshipDeliverable(models.Model):
    """Track sponsor benefit fulfillment"""
    class Type(models.TextChoices):
        LOGO_DISPLAY = 'logo_display', _('Logo Display')
        DEDICATED_CONTENT = 'dedicated_content', _('Dedicated Content')
        EVENT_PRESENCE = 'event_presence', _('Event Presence')
        NEWSLETTER_MENTION = 'newsletter_mention', _('Newsletter Mention')
        SOCIAL_SHOUTOUT = 'social_shoutout', _('Social Media Shoutout')
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        OVERDUE = 'overdue', _('Overdue')
    
    sponsor = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.CASCADE,
        related_name='deliverables'
    )
    deliverable_type = models.CharField(max_length=20, choices=Type.choices)
    description = models.TextField()
    quantity_required = models.PositiveIntegerField(default=1)
    quantity_delivered = models.PositiveIntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Linked content
    linked_content = models.ManyToManyField(
        'content.BlogPost',
        blank=True,
        related_name='sponsor_deliverables'
    )
    linked_videos = models.ManyToManyField(
        'content.VideoContent',
        blank=True,
        related_name='sponsor_deliverables'
    )
    linked_newsletters = models.ManyToManyField(
        'newsletter.NewsletterCampaign',
        blank=True,
        related_name='sponsor_deliverables'
    )
    
    notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sponsors_deliverable'
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.sponsor.company_name} - {self.get_deliverable_type_display()}"


class SponsorAsset(models.Model):
    """Logos, brand guidelines, etc. provided by sponsors"""
    sponsor = models.ForeignKey(
        'accounts.SponsorProfile',
        on_delete=models.CASCADE,
        related_name='assets'
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='sponsors/assets/')
    asset_type = models.CharField(
        max_length=50,
        choices=[
            ('logo', 'Logo'),
            ('guidelines', 'Brand Guidelines'),
            ('ad_creative', 'Ad Creative'),
            ('photo', 'Photo'),
            ('other', 'Other'),
        ]
    )
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sponsors_asset'
    
    def __str__(self):
        return f"{self.sponsor.company_name} - {self.name}"
