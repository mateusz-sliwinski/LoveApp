"""Urls.py files."""
# Django
from django.urls import include
from django.urls import path
#
from accounts.views import home_view

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('preferences/', home_view, name='tags')
]
