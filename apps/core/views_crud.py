from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Accounts models
from apps.accounts.models import User, DonorProfile, SponsorProfile, ConsortiumPartner, OrganizationProfile
from apps.accounts.forms import (
    UserCreationForm, UserChangeForm, DonorProfileForm, 
    SponsorProfileForm, ConsortiumPartnerForm, OrganizationProfileForm
)

# Content models
from apps.content.models import Category, VideoContent, Playlist, BlogPost, NewsItem
from apps.content.forms import (
    CategoryForm, VideoContentForm, PlaylistForm, 
    BlogPostForm, NewsItemForm
)

# Newsletter models
from apps.newsletter.models import Subscriber, NewsletterCampaign, EmailLog
from apps.newsletter.forms import (
    SubscriberForm, SubscriberPublicForm, 
    NewsletterCampaignForm, EmailLogForm
)

# Sponsors models
from apps.sponsors.models import Donation, SponsorshipDeliverable, SponsorAsset
from apps.sponsors.forms import (
    DonationForm, DonationPublicForm,
    SponsorshipDeliverableForm, SponsorAssetForm
)


# ==================== ACCOUNTS VIEWS ====================

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin user"""
    def test_func(self):
        return self.request.user.is_staff


class AccountsListView(AdminRequiredMixin, ListView):
    """List view for all account-related models"""
    template_name = 'dashboard/accounts/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_type = self.kwargs.get('model', 'users')
        
        if model_type == 'users':
            context['title'] = 'Users'
            context['items'] = User.objects.all()
            context['columns'] = ['Email', 'Role', 'Verified', 'Created']
        elif model_type == 'donors':
            context['title'] = 'Donors'
            context['items'] = DonorProfile.objects.all().select_related('user')
            context['columns'] = ['User', 'Type', 'Total Donated', 'Donations']
        elif model_type == 'sponsors':
            context['title'] = 'Sponsors'
            context['items'] = SponsorProfile.objects.all().select_related('user')
            context['columns'] = ['Company', 'Level', 'Contract Value', 'Status']
        elif model_type == 'partners':
            context['title'] = 'Partners'
            context['items'] = ConsortiumPartner.objects.all()
            context['columns'] = ['Name', 'Website', 'Active', 'Joined']
        
        context['model'] = model_type
        return context


# ==================== CONTENT VIEWS ====================

class CategoryListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/content/category_list.html'
    context_object_name = 'categories'
    ordering = ['order', 'name']


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/content/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/content/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/content/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category deleted successfully!')
        return super().form_valid(form)


class VideoListView(AdminRequiredMixin, ListView):
    model = VideoContent
    template_name = 'dashboard/content/video_list.html'
    context_object_name = 'videos'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return VideoContent.objects.all().select_related('author', 'playlist')


class VideoCreateView(AdminRequiredMixin, CreateView):
    model = VideoContent
    form_class = VideoContentForm
    template_name = 'dashboard/content/video_form.html'
    success_url = reverse_lazy('video-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Video created successfully!')
        return super().form_valid(form)


class VideoUpdateView(AdminRequiredMixin, UpdateView):
    model = VideoContent
    form_class = VideoContentForm
    template_name = 'dashboard/content/video_form.html'
    success_url = reverse_lazy('video-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Video updated successfully!')
        return super().form_valid(form)


class VideoDeleteView(AdminRequiredMixin, DeleteView):
    model = VideoContent
    template_name = 'dashboard/content/video_confirm_delete.html'
    success_url = reverse_lazy('video-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Video deleted successfully!')
        return super().form_valid(form)


class PlaylistListView(AdminRequiredMixin, ListView):
    model = Playlist
    template_name = 'dashboard/content/playlist_list.html'
    context_object_name = 'playlists'
    ordering = ['-created_at']


class PlaylistCreateView(AdminRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'dashboard/content/playlist_form.html'
    success_url = reverse_lazy('playlist-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Playlist created successfully!')
        return super().form_valid(form)


class PlaylistUpdateView(AdminRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'dashboard/content/playlist_form.html'
    success_url = reverse_lazy('playlist-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Playlist updated successfully!')
        return super().form_valid(form)


class PlaylistDeleteView(AdminRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'dashboard/content/playlist_confirm_delete.html'
    success_url = reverse_lazy('playlist-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Playlist deleted successfully!')
        return super().form_valid(form)


class BlogPostListView(AdminRequiredMixin, ListView):
    model = BlogPost
    template_name = 'dashboard/content/blogpost_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return BlogPost.objects.all().select_related('author')


class BlogPostCreateView(AdminRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/content/blogpost_form.html'
    success_url = reverse_lazy('blogpost-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)


class BlogPostUpdateView(AdminRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/content/blogpost_form.html'
    success_url = reverse_lazy('blogpost-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)


class BlogPostDeleteView(AdminRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'dashboard/content/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogpost-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post deleted successfully!')
        return super().form_valid(form)


class NewsItemListView(AdminRequiredMixin, ListView):
    model = NewsItem
    template_name = 'dashboard/content/newsitem_list.html'
    context_object_name = 'news_items'
    ordering = ['-published_at']


class NewsItemCreateView(AdminRequiredMixin, CreateView):
    model = NewsItem
    form_class = NewsItemForm
    template_name = 'dashboard/content/newsitem_form.html'
    success_url = reverse_lazy('newsitem-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'News item created successfully!')
        return super().form_valid(form)


class NewsItemUpdateView(AdminRequiredMixin, UpdateView):
    model = NewsItem
    form_class = NewsItemForm
    template_name = 'dashboard/content/newsitem_form.html'
    success_url = reverse_lazy('newsitem-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'News item updated successfully!')
        return super().form_valid(form)


class NewsItemDeleteView(AdminRequiredMixin, DeleteView):
    model = NewsItem
    template_name = 'dashboard/content/newsitem_confirm_delete.html'
    success_url = reverse_lazy('newsitem-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'News item deleted successfully!')
        return super().form_valid(form)


# ==================== NEWSLETTER VIEWS ====================

class SubscriberListView(AdminRequiredMixin, ListView):
    model = Subscriber
    template_name = 'dashboard/newsletter/subscriber_list.html'
    context_object_name = 'subscribers'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Subscriber.objects.all()


class SubscriberCreateView(AdminRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'dashboard/newsletter/subscriber_form.html'
    success_url = reverse_lazy('subscriber-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subscriber created successfully!')
        return super().form_valid(form)


class SubscriberUpdateView(AdminRequiredMixin, UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'dashboard/newsletter/subscriber_form.html'
    success_url = reverse_lazy('subscriber-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subscriber updated successfully!')
        return super().form_valid(form)


class SubscriberDeleteView(AdminRequiredMixin, DeleteView):
    model = Subscriber
    template_name = 'dashboard/newsletter/subscriber_confirm_delete.html'
    success_url = reverse_lazy('subscriber-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subscriber deleted successfully!')
        return super().form_valid(form)


class NewsletterCampaignListView(AdminRequiredMixin, ListView):
    model = NewsletterCampaign
    template_name = 'dashboard/newsletter/campaign_list.html'
    context_object_name = 'campaigns'
    ordering = ['-created_at']


class NewsletterCampaignCreateView(AdminRequiredMixin, CreateView):
    model = NewsletterCampaign
    form_class = NewsletterCampaignForm
    template_name = 'dashboard/newsletter/campaign_form.html'
    success_url = reverse_lazy('campaign-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Campaign created successfully!')
        return super().form_valid(form)


class NewsletterCampaignUpdateView(AdminRequiredMixin, UpdateView):
    model = NewsletterCampaign
    form_class = NewsletterCampaignForm
    template_name = 'dashboard/newsletter/campaign_form.html'
    success_url = reverse_lazy('campaign-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Campaign updated successfully!')
        return super().form_valid(form)


class NewsletterCampaignDeleteView(AdminRequiredMixin, DeleteView):
    model = NewsletterCampaign
    template_name = 'dashboard/newsletter/campaign_confirm_delete.html'
    success_url = reverse_lazy('campaign-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Campaign deleted successfully!')
        return super().form_valid(form)


# ==================== SPONSORS VIEWS ====================

class DonationListView(AdminRequiredMixin, ListView):
    model = Donation
    template_name = 'dashboard/sponsors/donation_list.html'
    context_object_name = 'donations'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Donation.objects.all().select_related('donor__user')


class DonationCreateView(AdminRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'dashboard/sponsors/donation_form.html'
    success_url = reverse_lazy('donation-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Donation created successfully!')
        return super().form_valid(form)


class DonationUpdateView(AdminRequiredMixin, UpdateView):
    model = Donation
    form_class = DonationForm
    template_name = 'dashboard/sponsors/donation_form.html'
    success_url = reverse_lazy('donation-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Donation updated successfully!')
        return super().form_valid(form)


class DonationDeleteView(AdminRequiredMixin, DeleteView):
    model = Donation
    template_name = 'dashboard/sponsors/donation_confirm_delete.html'
    success_url = reverse_lazy('donation-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Donation deleted successfully!')
        return super().form_valid(form)


class DeliverableListView(AdminRequiredMixin, ListView):
    model = SponsorshipDeliverable
    template_name = 'dashboard/sponsors/deliverable_list.html'
    context_object_name = 'deliverables'
    ordering = ['due_date']
    
    def get_queryset(self):
        return SponsorshipDeliverable.objects.all().select_related('sponsor')


class DeliverableCreateView(AdminRequiredMixin, CreateView):
    model = SponsorshipDeliverable
    form_class = SponsorshipDeliverableForm
    template_name = 'dashboard/sponsors/deliverable_form.html'
    success_url = reverse_lazy('deliverable-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Deliverable created successfully!')
        return super().form_valid(form)


class DeliverableUpdateView(AdminRequiredMixin, UpdateView):
    model = SponsorshipDeliverable
    form_class = SponsorshipDeliverableForm
    template_name = 'dashboard/sponsors/deliverable_form.html'
    success_url = reverse_lazy('deliverable-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Deliverable updated successfully!')
        return super().form_valid(form)


class DeliverableDeleteView(AdminRequiredMixin, DeleteView):
    model = SponsorshipDeliverable
    template_name = 'dashboard/sponsors/deliverable_confirm_delete.html'
    success_url = reverse_lazy('deliverable-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Deliverable deleted successfully!')
        return super().form_valid(form)


class SponsorAssetListView(AdminRequiredMixin, ListView):
    model = SponsorAsset
    template_name = 'dashboard/sponsors/asset_list.html'
    context_object_name = 'assets'
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        return SponsorAsset.objects.all().select_related('sponsor')


class SponsorAssetCreateView(AdminRequiredMixin, CreateView):
    model = SponsorAsset
    form_class = SponsorAssetForm
    template_name = 'dashboard/sponsors/asset_form.html'
    success_url = reverse_lazy('asset-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Asset uploaded successfully!')
        return super().form_valid(form)


class SponsorAssetDeleteView(AdminRequiredMixin, DeleteView):
    model = SponsorAsset
    template_name = 'dashboard/sponsors/asset_confirm_delete.html'
    success_url = reverse_lazy('asset-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Asset deleted successfully!')
        return super().form_valid(form)


# ==================== PUBLIC VIEWS ====================

def dashboard(request):
    """Main dashboard view"""
    if not request.user.is_staff:
        raise PermissionDenied
    
    context = {
        'user_count': User.objects.count(),
        'subscriber_count': Subscriber.objects.filter(status='active').count(),
        'video_count': VideoContent.objects.count(),
        'post_count': BlogPost.objects.count(),
        'donation_total': sum(d.amount for d in Donation.objects.filter(status='completed')),
        # Additional context for new dashboard
        'recent_videos': VideoContent.objects.all().order_by('-created_at')[:5],
        'recent_posts': BlogPost.objects.all().order_by('-created_at')[:5],
        'sponsor_count': SponsorProfile.objects.count(),
        'partner_count': ConsortiumPartner.objects.count(),
        'donation_count': Donation.objects.count(),
        'total_donations': sum(d.amount for d in Donation.objects.filter(status='completed')),
    }
    return render(request, 'dashboard/index.html', context)


def public_videos(request):
    """Public video listing"""
    videos = VideoContent.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'public/videos.html', {'videos': videos})


def public_video_detail(request, slug):
    """Public video detail"""
    video = get_object_or_404(VideoContent, slug=slug, is_published=True)
    return render(request, 'public/video_detail.html', {'video': video})


def public_blog(request):
    """Public blog listing"""
    posts = BlogPost.objects.filter(status='published').order_by('-published_at')
    return render(request, 'public/blog.html', {'posts': posts})


def public_blog_detail(request, slug):
    """Public blog post detail"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    return render(request, 'public/blog_detail.html', {'post': post})


def public_donate(request):
    """Public donation page"""
    if request.method == 'POST':
        form = DonationPublicForm(request.POST)
        if form.is_valid():
            # In production, this would create a pending donation
            messages.success(request, 'Thank you for your interest in donating! We will contact you shortly.')
            return redirect('donate')
    else:
        form = DonationPublicForm()
    
    return render(request, 'public/donate.html', {'form': form})


def public_newsletter(request):
    """Public newsletter subscription"""
    if request.method == 'POST':
        form = SubscriberPublicForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.status = 'pending'
            subscriber.source = 'website'
            subscriber.ip_address = request.META.get('REMOTE_ADDR')
            subscriber.user_agent = request.META.get('HTTP_USER_AGENT', '')
            subscriber.save()
            messages.success(request, 'Thank you for subscribing! Please check your email to confirm.')
            return redirect('newsletter')
    else:
        form = SubscriberPublicForm()
    
    return render(request, 'public/newsletter.html', {'form': form})


def public_about(request):
    """Public about page"""
    org = OrganizationProfile.objects.first()
    return render(request, 'public/about.html', {'organization': org})


def public_contact(request):
    """Public contact page"""
    return render(request, 'public/contact.html')
