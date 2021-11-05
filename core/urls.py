"""Urls.py files."""

# Django
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local
from .views import RandomPartner
from .views import RandomPartnerList

app_name = 'core'

urlpatterns = [
    path('random/', login_required(RandomPartner.as_view()), name='random'),
    path('ajax/random/', login_required(RandomPartnerList.as_view()), name='ajax_random_person'),

]
