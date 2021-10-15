"""Urls.py files."""
# Django
from django.urls import include
from django.urls import path
#
from accounts.views import PreferencesView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('preferences/', PreferencesView.as_view(), name='tags')
]
