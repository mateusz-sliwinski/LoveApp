"""Admin.py files."""

from django.contrib import admin

from accounts.models import CustomUser, PhotoUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(PhotoUser)
class PhotoUserAdmin(admin.ModelAdmin):  # noqa D101
    pass

