"""Urls.py files."""
from django.urls import path, include

urlpatterns = [
    path('/accounts/', include('allauth.urls')),
]
