from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DonorProfile, SponsorProfile, ConsortiumPartner, OrganizationProfile


class UserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'phone', 'organization')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form for editing existing users"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'organization', 'bio', 'avatar', 'is_verified', 'newsletter_subscribed')


class DonorProfileForm(forms.ModelForm):
    """Form for creating/editing donor profiles"""
    class Meta:
        model = DonorProfile
        fields = ('user', 'donor_type', 'tax_id', 'billing_address', 'is_recurring_donor', 'preferred_payment_method', 'communication_preferences', 'notes')
        widgets = {
            'billing_address': forms.Textarea(attrs={'rows': 3}),
            'communication_preferences': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SponsorProfileForm(forms.ModelForm):
    """Form for creating/editing sponsor profiles"""
    class Meta:
        model = SponsorProfile
        fields = ('user', 'company_name', 'logo', 'website', 'level', 'contract_value', 'contract_start', 'contract_end', 'benefits_claimed', 'brand_visibility_slots', 'dedicated_content_pieces', 'event_sponsorships', 'account_manager', 'is_active')
        widgets = {
            'benefits_claimed': forms.Textarea(attrs={'rows': 2}),
            'contract_start': forms.DateInput(attrs={'type': 'date'}),
            'contract_end': forms.DateInput(attrs={'type': 'date'}),
        }


class ConsortiumPartnerForm(forms.ModelForm):
    """Form for creating/editing consortium partners"""
    class Meta:
        model = ConsortiumPartner
        fields = ('name', 'slug', 'logo', 'description', 'website', 'contact_person', 'content_contribution_weight', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class OrganizationProfileForm(forms.ModelForm):
    """Form for organization profile - Budget Ndio Story"""
    class Meta:
        model = OrganizationProfile
        fields = '__all__'
        widgets = {
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'consortium_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_promise': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'vision': forms.Textarea(attrs={'rows': 3}),
            'mission': forms.Textarea(attrs={'rows': 3}),
            'headquarters': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_country': forms.TextInput(attrs={'class': 'form-control'}),
            'year_established': forms.NumberInput(attrs={'class': 'form-control'}),
            'email_general': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_partnerships': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_media': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'tiktok': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
            'youtube': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'alert_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'success_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'neutral_dark': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'neutral_light': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }
