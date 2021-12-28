"""Urls.py files."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

# Project
from accounts.views import DeletePhotoView
from accounts.views import DetailPhotoView
from accounts.views import HomeView
from accounts.views import ListPhotoView
from accounts.views import PhotoView
from accounts.views import PreferencesListView
from accounts.views import PreferencesUpdateView
from accounts.views import PreferencesView
from accounts.views import test

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('preferences/', login_required(PreferencesView.as_view()),
         name='preferences'),
    path('preferences/list', login_required(PreferencesListView.as_view()),
         name='preferences_list'),
    path('preferences/update/<int:pk>', login_required(PreferencesUpdateView.as_view()),
         name='preference_update'),

    path('photo/', login_required(PhotoView.as_view()), name='photo'),
    path('photo/list', login_required(ListPhotoView.as_view()), name='list_photo'),
    path('photo/detail/<int:pk>', login_required(DetailPhotoView.as_view()), name='detail_photo'),
    path('photo/delete/<int:pk>', login_required(DeletePhotoView.as_view()), name='delete_photo'),
    path('account/profile', login_required(HomeView.as_view()), name='home'),
    path('test', test.as_view(), name='test'),

]
