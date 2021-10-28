"""Urls.py files."""

from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import RandomPartner

app_name = 'core'

urlpatterns = [
    path('random/', login_required(RandomPartner.as_view()), name='random'),
]
