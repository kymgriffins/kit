from django import forms
from .models import Subscriber, NewsletterCampaign, EmailLog


class SubscriberForm(forms.ModelForm):
    """Form for creating/editing newsletter subscribers"""
    class Meta:
        model = Subscriber
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'content_preference': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'website, api, etc.'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'unsubscribe_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class SubscriberPublicForm(forms.ModelForm):
    """Public-facing form for subscribing to newsletter"""
    class Meta:
        model = Subscriber
        fields = ('email', 'first_name', 'last_name', 'content_preference')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name (optional)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name (optional)'}),
            'content_preference': forms.Select(attrs={'class': 'form-control'}),
        }


class NewsletterCampaignForm(forms.ModelForm):
    """Form for creating/editing newsletter campaigns"""
    class Meta:
        model = NewsletterCampaign
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'preheader': forms.TextInput(attrs={'class': 'form-control'}),
            'campaign_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'html_content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'target_preferences': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': '["weekly_digest", "all"]'}),
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class EmailLogForm(forms.ModelForm):
    """Form for viewing email log details (mostly read-only)"""
    class Meta:
        model = EmailLog
        fields = '__all__'
        widgets = {
            'message_id': forms.TextInput(attrs={'class': 'form-control'}),
            'clicked_links': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
