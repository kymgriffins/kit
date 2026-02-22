from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def profile(request):
    """View for user profile page"""
    user = request.user
    return render(request, 'dashboard/profile.html', {
        'user': user,
        'profile': user
    })