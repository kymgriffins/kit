"""
Custom template filters for API dashboard templates.
"""

import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def json_dumps(value):
    """Convert a Python object to JSON string."""
    if value is None:
        return 'null'
    try:
        return json.dumps(value, indent=2)
    except (TypeError, ValueError):
        return str(value)


@register.filter
def is_string(value):
    """Check if value is a string."""
    return isinstance(value, str)


@register.filter
def is_number(value):
    """Check if value is a number."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


@register.filter
def is_bool(value):
    """Check if value is a boolean."""
    return isinstance(value, bool)


@register.filter
def is_list(value):
    """Check if value is a list."""
    return isinstance(value, list)


@register.filter
def is_dict(value):
    """Check if value is a dict."""
    return isinstance(value, dict)


@register.filter
def replace(value, arg):
    """Replace all occurrences of arg with replacement."""
    if not value:
        return ''
    args = arg.split(',')
    if len(args) == 1:
        return value.replace('_', args[0])
    return value.replace(args[0], args[1] if len(args) > 1 else '')


@register.filter
def truncatechars(value, arg):
    """Truncate string to specified length."""
    if not value:
        return ''
    try:
        length = int(arg)
        if len(value) > length:
            return value[:length] + '...'
        return value
    except (ValueError, TypeError):
        return value


@register.filter
def default(value, arg):
    """Return default value if value is empty."""
    if value:
        return value
    return arg


@register.simple_tag
def method_badge(method):
    """Generate a method badge HTML."""
    method_lower = method.lower()
    colors = {
        'get': 'bg-green-500/20 text-green-400',
        'post': 'bg-blue-500/20 text-blue-400',
        'put': 'bg-yellow-500/20 text-yellow-400',
        'patch': 'bg-orange-500/20 text-orange-400',
        'delete': 'bg-red-500/20 text-red-400',
    }
    color_class = colors.get(method_lower, 'bg-gray-500/20 text-gray-400')
    return mark_safe(f'<span class="px-2 py-1 rounded text-xs font-semibold {color_class}">{method.upper()}</span>')


@register.simple_tag
def status_badge(status_code):
    """Generate a status code badge HTML."""
    if 200 <= status_code < 300:
        color_class = 'bg-green-500/20 text-green-400'
    elif 300 <= status_code < 400:
        color_class = 'bg-blue-500/20 text-blue-400'
    elif 400 <= status_code < 500:
        color_class = 'bg-orange-500/20 text-orange-400'
    elif 500 <= status_code:
        color_class = 'bg-red-500/20 text-red-400'
    else:
        color_class = 'bg-gray-500/20 text-gray-400'
    
    return mark_safe(f'<span class="px-2 py-1 rounded text-xs font-semibold {color_class}">{status_code}</span>')
