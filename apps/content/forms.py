from django import forms
from .models import Category, VideoContent, Playlist, BlogPost, NewsItem


class CategoryForm(forms.ModelForm):
    """Form for creating/editing categories"""
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., fa-video'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VideoContentForm(forms.ModelForm):
    """Form for creating/editing video content"""
    class Meta:
        model = VideoContent
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'external_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YouTube video ID'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control'}),
            'embed_url': forms.URLInput(attrs={'class': 'form-control'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'duration_seconds': forms.NumberInput(attrs={'class': 'form-control'}),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PlaylistForm(forms.ModelForm):
    """Form for creating/editing playlists"""
    class Meta:
        model = Playlist
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'estimated_duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class BlogPostForm(forms.ModelForm):
    """Form for creating/editing blog posts"""
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '["tag1", "tag2"]'}),
            'featured_image_caption': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'scheduled_publish_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'read_time_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


class NewsItemForm(forms.ModelForm):
    """Form for creating/editing news items"""
    class Meta:
        model = NewsItem
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'source_url': forms.URLInput(attrs={'class': 'form-control'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
