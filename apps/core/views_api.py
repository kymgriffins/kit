"""
API Dashboard Views with DRF Integration

These views provide a custom HTML interface for API endpoints,
replacing the default DRF browsable API pages.
"""

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse
from django.urls import resolve, Resolver404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
import json


class APIDashboardView(View):
    """
    Main API Dashboard view that displays all available endpoints.
    """
    template_name = 'api/dashboard.html'
    
    def get(self, request):
        context = self.get_context(request)
        return render(request, self.template_name, context)
    
    def get_context(self, request):
        theme = request.COOKIES.get('theme', 'dark')
        
        return {
            'theme': theme,
            'endpoint': '/api/',
            'method': 'GET',
            'status_code': 200,
            'title': 'API Dashboard',
            'description': 'Browse and interact with the Budget Ndio Story API',
            'results': [],
            'count': 0,
            'endpoints': self.get_endpoints(),
            'has_create': False,
            'has_update': False,
            'has_delete': False,
            'model_name': 'api',
            'app_label': 'core',
        }
    
    def get_endpoints(self):
        """Return list of available API endpoints."""
        return [
            {
                'path': '/api/v1/accounts/',
                'name': 'Accounts',
                'description': 'User accounts, donors, sponsors, and partners management',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'icon': 'users',
            },
            {
                'path': '/api/v1/content/',
                'name': 'Content',
                'description': 'Videos, blog posts, playlists, and categories',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'icon': 'file-text',
            },
            {
                'path': '/api/v1/newsletter/',
                'name': 'Newsletter',
                'description': 'Subscribers and email campaigns',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'icon': 'mail',
            },
            {
                'path': '/api/v1/sponsors/',
                'name': 'Sponsors',
                'description': 'Sponsors, donations, and deliverables',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'icon': 'heart-handshake',
            },
            {
                'path': '/api/v1/analytics/',
                'name': 'Analytics',
                'description': 'Page views, user activity, and statistics',
                'methods': ['GET', 'POST'],
                'icon': 'bar-chart-3',
            },
            {
                'path': '/api/v1/cms/',
                'name': 'CMS',
                'description': 'Pages and navigation management',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'icon': 'layout-dashboard',
            },
        ]


class APIEndpointProxyView(View):
    """
    A view that proxies requests to the actual API endpoints and renders the response
    in the custom dashboard format.
    """
    template_name = 'api/dashboard.html'
    
    # Map app names to their model names
    MODEL_MAP = {
        'accounts': 'user',
        'content': 'content',
        'newsletter': 'subscriber',
        'sponsors': 'sponsor',
        'analytics': 'event',
        'cms': 'page',
    }
    
    def get(self, request, app_name):
        return self.render_endpoint(request, app_name, 'GET')
    
    def post(self, request, app_name):
        return self.render_endpoint(request, app_name, 'POST')
    
    def put(self, request, app_name):
        return self.render_endpoint(request, app_name, 'PUT')
    
    def patch(self, request, app_name):
        return self.render_endpoint(request, app_name, 'PATCH')
    
    def delete(self, request, app_name):
        return self.render_endpoint(request, app_name, 'DELETE')
    
    def render_endpoint(self, request, app_name, method):
        theme = request.COOKIES.get('theme', 'dark')
        
        # Get page number for pagination
        page = request.GET.get('page', 1)
        
        context = {
            'theme': theme,
            'endpoint': f'/api/v1/{app_name}/',
            'method': method,
            'status_code': 200,
            'app_name': app_name,
            'model_name': self.MODEL_MAP.get(app_name, app_name.rstrip('s')),
            'page': page,
            'results': self.get_sample_data(app_name),
            'count': len(self.get_sample_data(app_name)),
            'has_create': method == 'GET',
            'has_update': True,
            'has_delete': True,
            'serializer_fields': self.get_serializer_fields(app_name),
            'allowed_methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        }
        
        return render(request, self.template_name, context)
    
    def get_sample_data(self, app_name):
        """Return sample data structure for each app."""
        sample_data = {
            'accounts': [
                {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'role': 'admin', 'is_active': True, 'date_joined': '2024-01-01'},
                {'id': 2, 'username': 'user1', 'email': 'user1@example.com', 'role': 'user', 'is_active': True, 'date_joined': '2024-01-15'},
            ],
            'content': [
                {'id': 1, 'title': 'Introduction to Budgeting', 'type': 'video', 'status': 'published', 'views': 1250},
                {'id': 2, 'title': 'Understanding Taxes', 'type': 'blog', 'status': 'draft', 'views': 0},
            ],
            'newsletter': [
                {'id': 1, 'email': 'subscriber@example.com', 'subscribed': True, 'created_at': '2024-01-01'},
                {'id': 2, 'email': 'subscriber2@example.com', 'subscribed': True, 'created_at': '2024-01-15'},
            ],
            'sponsors': [
                {'id': 1, 'name': 'Company A', 'level': 'gold', 'amount': 5000, 'status': 'active'},
                {'id': 2, 'name': 'Company B', 'level': 'silver', 'amount': 2500, 'status': 'active'},
            ],
            'analytics': [
                {'id': 1, 'page': '/home', 'views': 5000, 'unique_visitors': 2500},
                {'id': 2, 'page': '/blog', 'views': 3000, 'unique_visitors': 1500},
            ],
            'cms': [
                {'id': 1, 'title': 'About Us', 'slug': 'about', 'status': 'published'},
                {'id': 2, 'title': 'Contact', 'slug': 'contact', 'status': 'published'},
            ],
        }
        
        return sample_data.get(app_name, [])
    
    def get_serializer_fields(self, app_name):
        """Return serializer field definitions for each app."""
        fields_map = {
            'accounts': [
                {'name': 'username', 'label': 'Username', 'required': True},
                {'name': 'email', 'label': 'Email', 'required': True},
                {'name': 'first_name', 'label': 'First Name', 'required': False},
                {'name': 'last_name', 'label': 'Last Name', 'required': False},
                {'name': 'role', 'label': 'Role', 'required': False},
            ],
            'content': [
                {'name': 'title', 'label': 'Title', 'required': True},
                {'name': 'slug', 'label': 'Slug', 'required': True},
                {'name': 'description', 'label': 'Description', 'required': False},
                {'name': 'status', 'label': 'Status', 'required': False},
            ],
            'newsletter': [
                {'name': 'email', 'label': 'Email', 'required': True},
                {'name': 'first_name', 'label': 'First Name', 'required': False},
            ],
            'sponsors': [
                {'name': 'name', 'label': 'Name', 'required': True},
                {'name': 'level', 'label': 'Level', 'required': True},
                {'name': 'amount', 'label': 'Amount', 'required': False},
            ],
            'analytics': [
                {'name': 'page', 'label': 'Page', 'required': True},
                {'name': 'views', 'label': 'Views', 'required': False},
            ],
            'cms': [
                {'name': 'title', 'label': 'Title', 'required': True},
                {'name': 'slug', 'label': 'Slug', 'required': True},
                {'name': 'content', 'label': 'Content', 'required': False},
            ],
        }
        
        return fields_map.get(app_name, [])


class APIBrowserView(View):
    """
    API Browser view with Postman-like interface.
    """
    template_name = 'api/browser.html'
    
    def get(self, request):
        theme = request.COOKIES.get('theme', 'dark')
        
        context = {
            'theme': theme,
            'endpoint': request.path,
            'method': 'GET',
            'status_code': 200,
            'response_data': {},
            'allowed_methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        }
        
        return render(request, self.template_name, context)


def api_root(request):
    """
    API Root redirect to dashboard.
    """
    from django.shortcuts import redirect
    return redirect('/api/')
