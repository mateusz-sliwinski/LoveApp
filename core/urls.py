"""Urls.py files."""

# Django
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local
from .views import CreateMessage, DashboardView
from .views import CreateThread
from .views import ListThreads
from .views import RandomPartner
from .views import RandomPartnerList
from .views import ThreadView

app_name = 'core'

urlpatterns = [
    path('random/', login_required(RandomPartner.as_view()), name='random'),
    path('ajax/random/', login_required(RandomPartnerList.as_view()), name='ajax_random_person'),

    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),

    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),


]
