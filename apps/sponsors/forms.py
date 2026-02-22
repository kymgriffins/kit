from django import forms
from .models import Donation, SponsorshipDeliverable, SponsorAsset


class DonationForm(forms.ModelForm):
    """Form for creating/editing donations"""
    class Meta:
        model = Donation
        fields = '__all__'
        widgets = {
            'donor': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_metadata': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'recurring_frequency': forms.Select(attrs={'class': 'form-control'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
            'campaign_source': forms.TextInput(attrs={'class': 'form-control'}),
            'landing_page': forms.URLInput(attrs={'class': 'form-control'}),
            'completed_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class DonationPublicForm(forms.ModelForm):
    """Public-facing form for making donations"""
    class Meta:
        model = Donation
        fields = ('amount', 'currency', 'payment_method')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


class SponsorshipDeliverableForm(forms.ModelForm):
    """Form for creating/editing sponsorship deliverables"""
    class Meta:
        model = SponsorshipDeliverable
        fields = '__all__'
        widgets = {
            'sponsor': forms.Select(attrs={'class': 'form-control'}),
            'deliverable_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'quantity_required': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_delivered': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'completed_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'internal_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class SponsorAssetForm(forms.ModelForm):
    """Form for uploading sponsor assets"""
    class Meta:
        model = SponsorAsset
        fields = '__all__'
        widgets = {
            'sponsor': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
