"""
Custom Dashboard HTML Renderer for Django REST Framework

This module provides a custom HTML renderer that creates a modern,
dashboard-style interface for API endpoints, replacing the default
DRF browsable API pages.
"""

from rest_framework.renderers import BaseRenderer, HTMLFormRenderer, TemplateHTMLRenderer
from rest_framework.relations import Hyperlink, PKOnlyObject
from rest_framework.utils import formatting
from django.template import loader, RequestContext
from django.utils.safestring import mark_safe
from collections import OrderedDict
import json


class DashboardHTMLRenderer(BaseRenderer):
    """
    Custom HTML renderer that creates a modern dashboard-style interface
    for API endpoints, replacing the default DRF browsable API pages.
    """
    media_type = 'text/html'
    format = 'html'
    template_name = 'api/dashboard.html'
    charset = 'utf-8'
    
    # Style constants
    BUTTON_PRIMARY = 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors'
    BUTTON_SECONDARY = 'bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg font-medium transition-colors'
    BUTTON_DANGER = 'bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors'
    BUTTON_SUCCESS = 'bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors'
    INPUT_CLASS = 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
    LABEL_CLASS = 'block text-sm font-medium text-gray-300 mb-2'
    TABLE_HEADER_CLASS = 'px-6 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider bg-gray-800'
    TABLE_CELL_CLASS = 'px-6 py-4 whitespace-nowrap text-sm text-gray-300'
    CARD_CLASS = 'bg-gray-900 border border-gray-800 rounded-xl p-6'
    SIDEBAR_LINK_CLASS = 'flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300 hover:bg-gray-800 hover:text-white transition-all'
    SIDEBAR_LINK_ACTIVE_CLASS = 'bg-blue-600/20 text-blue-400 border-l-2 border-blue-600'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render data as HTML.
        """
        if data is None:
            return b''
        
        request = renderer_context.get('request')
        response = renderer_context.get('response')
        
        # Get the view and determine what we're rendering
        view = renderer_context.get('view')
        
        # Build context for the template
        context = self.build_context(data, request, response, view)
        
        # Render the template
        template = loader.get_template('api/dashboard.html')
        
        return template.render(context, request).encode('utf-8')
    
    def build_context(self, data, request, response, view):
        """Build the template context from the response data."""
        
        # Determine the context based on what's in data
        context = {
            'request': request,
            'response': response,
            'view': view,
            'theme': self.get_theme(request),
        }
        
        # Add endpoint info
        context['endpoint'] = request.path
        context['method'] = request.method
        context['is_list'] = response.status_code in [200, 201] and isinstance(data, (list, dict))
        
        # Handle different response types
        if isinstance(data, dict):
            # Check if it's a list response with pagination
            if 'results' in data:
                context['results'] = data['results']
                context['count'] = data.get('count', len(data['results']))
                context['next_url'] = data.get('next')
                context['previous_url'] = data.get('previous')
            elif 'detail' in data:
                context['detail'] = data['detail']
                context['error'] = True
            else:
                # Single object or other dict
                context['object'] = data
                context['fields'] = self.extract_fields(data)
        elif isinstance(data, list):
            context['results'] = data
            context['count'] = len(data)
        
        # Add serializer info if available
        if hasattr(view, 'get_serializer'):
            try:
                serializer = view.get_serializer()
                context['serializer'] = serializer
                if hasattr(serializer, 'fields'):
                    context['serializer_fields'] = self.get_serializer_fields(serializer)
            except:
                pass
        
        # Add CRUD operations info
        context['allowed_methods'] = self.get_allowed_methods(view)
        context['has_create'] = 'POST' in context['allowed_methods']
        context['has_update'] = 'PUT' in context['allowed_methods'] or 'PATCH' in context['allowed_methods']
        context['has_delete'] = 'DELETE' in context['allowed_methods']
        
        # Add view info
        if hasattr(view, 'queryset'):
            context['model_name'] = view.queryset.model._meta.model_name
            context['app_label'] = view.queryset.model._meta.app_label
        
        return context
    
    def get_theme(self, request):
        """Get the current theme preference."""
        # Check cookie first, then session
        theme = request.COOKIES.get('theme', 'dark')
        return theme
    
    def extract_fields(self, data):
        """Extract field information from serialized data."""
        if not isinstance(data, dict):
            return []
        
        fields = []
        for key, value in data.items():
            field_info = {
                'name': key,
                'value': value,
                'type': self.get_field_type(value),
            }
            
            # Check if it's a nested object or list
            if isinstance(value, dict):
                field_info['is_object'] = True
                field_info['nested_fields'] = self.extract_fields(value)
            elif isinstance(value, list):
                field_info['is_list'] = True
                field_info['count'] = len(value)
            else:
                field_info['is_object'] = False
                field_info['is_list'] = False
            
            fields.append(field_info)
        
        return fields
    
    def get_field_type(self, value):
        """Determine the type of a field value."""
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'string'
    
    def get_serializer_fields(self, serializer):
        """Extract field information from a serializer."""
        if not hasattr(serializer, 'fields'):
            return []
        
        fields = []
        for name, field in serializer.fields.items():
            field_info = {
                'name': name,
                'required': getattr(field, 'required', False),
                'read_only': getattr(field, 'read_only', False),
                'label': getattr(field, 'label', name),
                'help_text': getattr(field, 'help_text', ''),
            }
            fields.append(field_info)
        
        return fields
    
    def get_allowed_methods(self, view):
        """Get the allowed HTTP methods for the view."""
        if hasattr(view, 'get_allowed_methods'):
            return [m.upper() for m in view.get_allowed_methods()]
        return []


class DashboardFormRenderer(DashboardHTMLRenderer):
    """
    Renderer for forms in the dashboard interface.
    """
    template_name = 'api/form.html'
    
    def build_context(self, data, request, response, view):
        context = super().build_context(data, request, response, view)
        
        # Add form-specific context
        if hasattr(view, 'get_serializer'):
            try:
                serializer = view.get_serializer()
                context['form_fields'] = self.build_form_fields(serializer)
            except Exception:
                pass
        
        return context
    
    def build_form_fields(self, serializer):
        """Build form field definitions from serializer."""
        fields = []
        
        if hasattr(serializer, 'fields'):
            for name, field in serializer.fields.items():
                if getattr(field, 'write_only', False):
                    continue
                
                field_def = {
                    'name': name,
                    'label': getattr(field, 'label', name).replace('_', ' ').title(),
                    'required': getattr(field, 'required', False),
                    'help_text': getattr(field, 'help_text', ''),
                    'error': serializer.errors.get(name, []),
                }
                
                # Determine field type
                field_class = field.__class__.__name__
                if 'ChoiceField' in field_class:
                    field_def['type'] = 'select'
                    field_def['choices'] = field.choices if hasattr(field, 'choices') else []
                elif 'BooleanField' in field_class:
                    field_def['type'] = 'checkbox'
                elif 'TextField' in field_class or 'CharField' in field_class:
                    if getattr(field, 'max_length', 0) > 100:
                        field_def['type'] = 'textarea'
                    else:
                        field_def['type'] = 'text'
                else:
                    field_def['type'] = 'text'
                
                fields.append(field_def)
        
        return fields


class APIBrowserRenderer(BaseRenderer):
    """
    A complete API browser renderer that provides a Postman-like interface
    for exploring and testing API endpoints.
    """
    media_type = 'text/html'
    format = 'api'
    template_name = 'api/browser.html'
    charset = 'utf-8'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        request = renderer_context.get('request')
        response = renderer_context.get('response')
        view = renderer_context.get('view')
        
        context = {
            'request': request,
            'response': response,
            'view': view,
            'data': data,
            'theme': request.COOKIES.get('theme', 'dark'),
            'endpoint': request.path,
            'method': request.method,
            'status_code': response.status_code,
        }
        
        # Add response data
        if hasattr(response, 'data'):
            context['response_data'] = response.data
        
        # Add view info
        if view:
            context['allowed_methods'] = self.get_allowed_methods(view)
            context['view_name'] = getattr(view, 'action', 'unknown')
            
            if hasattr(view, 'get_queryset'):
                try:
                    model = view.get_queryset().model
                    context['model_name'] = model._meta.model_name
                    context['app_label'] = model._meta.app_label
                except:
                    pass
        
        template = loader.get_template('api/browser.html')
        return template.render(context, request).encode('utf-8')
    
    def get_allowed_methods(self, view):
        if hasattr(view, 'get_allowed_methods'):
            return [m.upper() for m in view.get_allowed_methods()]
        return []
