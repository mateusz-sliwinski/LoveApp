"""Admin.py files."""

# Django
from django.contrib import admin

# Project
from accounts.models import CustomUser, Preferences
from accounts.models import PhotoUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(PhotoUser)
class PhotoUserAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):  # noqa D101
    pass
