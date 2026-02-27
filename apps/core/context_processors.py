"""
Context processors for the API dashboard.
"""

from django.conf import settings


def theme(request):
    """
    Add theme to all template contexts.
    """
    theme = request.COOKIES.get('theme', 'dark')
    return {
        'theme': theme,
    }


def api_info(request):
    """
    Add API info to template context.
    """
    return {
        'api_version': 'v1',
        'api_base_url': '/api/v1/',
    }
