"""Urls.py files."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

# Project
from accounts.views import DeletePhotoView
from accounts.views import DetailPhotoView
from accounts.views import ListPhotoView
from accounts.views import PhotoView
from accounts.views import PreferencesListView
from accounts.views import PreferencesView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('preferences/', login_required(PreferencesView.as_view()), name='preferences'),
    path('preferences/list', login_required(PreferencesListView.as_view()), name='preferences_list'),

    path('photo/', login_required(PhotoView.as_view()), name='photo'),
    path('photo/list', login_required(ListPhotoView.as_view()), name='list_photo'),
    path('photo/detail/<int:pk>', login_required(DetailPhotoView.as_view()), name='detail_photo'),
    path('photo/delete/<int:pk>', login_required(DeletePhotoView.as_view()), name='delete_photo'),

]
