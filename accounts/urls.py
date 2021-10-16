"""Urls.py files."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

# Project

from accounts.views import PreferencesView, PhotoView, ListPhoto, DetailPhoto

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('preferences/', login_required(PreferencesView.as_view()), name='tags'),
    path('photo/', login_required(PhotoView.as_view()), name='photo'),
    path('photo/list', login_required(ListPhoto.as_view()), name='list_photo'),
    path('photo/detail/<int:pk>', login_required(DetailPhoto.as_view()), name='detail_photo'),
]
