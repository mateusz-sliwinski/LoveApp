"""Urls.py files."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

# Project

from accounts.views import PreferencesView, PhotoView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('preferences/', login_required(PreferencesView.as_view()), name='tags'),
    path('photo/', login_required(PhotoView.as_view()), name='photo'),
]
