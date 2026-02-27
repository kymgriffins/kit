from django.urls import path
from . import views_crud
from . import views
from . import views_profile
from django.views.decorators.csrf import csrf_exempt

# CSRF token view
def csrf_token_view(request):
    from django.middleware.csrf import get_token
    from django.http import JsonResponse
    return JsonResponse({'csrfToken': get_token(request)})

# Login view (JSON API)
@csrf_exempt
def api_login_view(request):
    from django.contrib.auth import authenticate, login
    from django.http import JsonResponse
    from django.views.decorators.http import require_POST
    import json
    
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Logout view (JSON API)
def api_logout_view(request):
    from django.contrib.auth import logout
    from django.http import JsonResponse
    from django.views.decorators.http import require_POST
    
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Current user view
def current_user_view(request):
    from django.http import JsonResponse
    
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
    return JsonResponse({'error': 'Not authenticated'}, status=401)

urlpatterns = [
    # CSRF and Auth API
    path('api/csrf/', csrf_token_view, name='csrf_token'),
    path('api/auth/login/', api_login_view, name='api_login'),
    path('api/auth/logout/', api_logout_view, name='api_logout'),
    path('api/auth/user/', current_user_view, name='current_user'),
    
    # Dashboard
    path('dashboard/', views_crud.dashboard, name='dashboard'),
    
    # Accounts URLs
    path('dashboard/users/', views_crud.AccountsListView.as_view(), {'model': 'users'}, name='user-list'),
    path('dashboard/donors/', views_crud.AccountsListView.as_view(), {'model': 'donors'}, name='donor-list'),
    path('dashboard/sponsors/', views_crud.AccountsListView.as_view(), {'model': 'sponsors'}, name='sponsor-list'),
    path('dashboard/partners/', views_crud.AccountsListView.as_view(), {'model': 'partners'}, name='partner-list'),
    
    # Content - Categories
    path('dashboard/categories/', views_crud.CategoryListView.as_view(), name='category-list'),
    path('dashboard/categories/create/', views_crud.CategoryCreateView.as_view(), name='category-create'),
    path('dashboard/categories/<int:pk>/edit/', views_crud.CategoryUpdateView.as_view(), name='category-update'),
    path('dashboard/categories/<int:pk>/delete/', views_crud.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Content - Videos
    path('dashboard/videos/', views_crud.VideoListView.as_view(), name='video-list'),
    path('dashboard/videos/create/', views_crud.VideoCreateView.as_view(), name='video-create'),
    path('dashboard/videos/<int:pk>/edit/', views_crud.VideoUpdateView.as_view(), name='video-update'),
    path('dashboard/videos/<int:pk>/delete/', views_crud.VideoDeleteView.as_view(), name='video-delete'),
    
    # Content - Playlists
    path('dashboard/playlists/', views_crud.PlaylistListView.as_view(), name='playlist-list'),
    path('dashboard/playlists/create/', views_crud.PlaylistCreateView.as_view(), name='playlist-create'),
    path('dashboard/playlists/<int:pk>/edit/', views_crud.PlaylistUpdateView.as_view(), name='playlist-update'),
    path('dashboard/playlists/<int:pk>/delete/', views_crud.PlaylistDeleteView.as_view(), name='playlist-delete'),
    
    # Content - Blog Posts
    path('dashboard/posts/', views_crud.BlogPostListView.as_view(), name='blogpost-list'),
    path('dashboard/posts/create/', views_crud.BlogPostCreateView.as_view(), name='blogpost-create'),
    path('dashboard/posts/<int:pk>/edit/', views_crud.BlogPostUpdateView.as_view(), name='blogpost-update'),
    path('dashboard/posts/<int:pk>/delete/', views_crud.BlogPostDeleteView.as_view(), name='blogpost-delete'),
    
    # Content - News
    path('dashboard/news/', views_crud.NewsItemListView.as_view(), name='newsitem-list'),
    path('dashboard/news/create/', views_crud.NewsItemCreateView.as_view(), name='newsitem-create'),
    path('dashboard/news/<int:pk>/edit/', views_crud.NewsItemUpdateView.as_view(), name='newsitem-update'),
    path('dashboard/news/<int:pk>/delete/', views_crud.NewsItemDeleteView.as_view(), name='newsitem-delete'),
    
    # Newsletter - Subscribers
    path('dashboard/subscribers/', views_crud.SubscriberListView.as_view(), name='subscriber-list'),
    path('dashboard/subscribers/create/', views_crud.SubscriberCreateView.as_view(), name='subscriber-create'),
    path('dashboard/subscribers/<int:pk>/edit/', views_crud.SubscriberUpdateView.as_view(), name='subscriber-update'),
    path('dashboard/subscribers/<int:pk>/delete/', views_crud.SubscriberDeleteView.as_view(), name='subscriber-delete'),
    
    # Newsletter - Campaigns
    path('dashboard/campaigns/', views_crud.NewsletterCampaignListView.as_view(), name='campaign-list'),
    path('dashboard/campaigns/create/', views_crud.NewsletterCampaignCreateView.as_view(), name='campaign-create'),
    path('dashboard/campaigns/<int:pk>/edit/', views_crud.NewsletterCampaignUpdateView.as_view(), name='campaign-update'),
    path('dashboard/campaigns/<int:pk>/delete/', views_crud.NewsletterCampaignDeleteView.as_view(), name='campaign-delete'),
    
    # Sponsors - Donations
    path('dashboard/donations/', views_crud.DonationListView.as_view(), name='donation-list'),
    path('dashboard/donations/create/', views_crud.DonationCreateView.as_view(), name='donation-create'),
    path('dashboard/donations/<int:pk>/edit/', views_crud.DonationUpdateView.as_view(), name='donation-update'),
    path('dashboard/donations/<int:pk>/delete/', views_crud.DonationDeleteView.as_view(), name='donation-delete'),
    
    # Sponsors - Deliverables
    path('dashboard/deliverables/', views_crud.DeliverableListView.as_view(), name='deliverable-list'),
    path('dashboard/deliverables/create/', views_crud.DeliverableCreateView.as_view(), name='deliverable-create'),
    path('dashboard/deliverables/<int:pk>/edit/', views_crud.DeliverableUpdateView.as_view(), name='deliverable-update'),
    path('dashboard/deliverables/<int:pk>/delete/', views_crud.DeliverableDeleteView.as_view(), name='deliverable-delete'),
    
    # Sponsors - Assets
    path('dashboard/assets/', views_crud.SponsorAssetListView.as_view(), name='asset-list'),
    path('dashboard/assets/create/', views_crud.SponsorAssetCreateView.as_view(), name='asset-create'),
    path('dashboard/assets/<int:pk>/delete/', views_crud.SponsorAssetDeleteView.as_view(), name='asset-delete'),
    
    # Public Pages
    path('videos/', views_crud.public_videos, name='public-videos'),
    path('videos/<slug:slug>/', views_crud.public_video_detail, name='public-video-detail'),
    path('blog/', views_crud.public_blog, name='public-blog'),
    path('blog/<slug:slug>/', views_crud.public_blog_detail, name='public-blog-detail'),
    path('donate/', views_crud.public_donate, name='donate'),
    path('newsletter/', views_crud.public_newsletter, name='newsletter'),
    path('about/', views_crud.public_about, name='about'),
    path('contact/', views_crud.public_contact, name='contact'),

    # Profile
    path('dashboard/profile/', views_profile.profile, name='profile'),
    
    # Existing API documentation and main pages
    path('api/docs/', views.api_docs, name='api_docs'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('index/', views.index, name='index'),
    path('config/', views.config_page, name='config'),
    path('v2/', views.v2_page, name='v2'),
]
