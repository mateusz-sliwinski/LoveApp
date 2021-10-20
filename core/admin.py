"""Admin.py files."""

# Django
from django.contrib import admin

# 3rd-party
from core.models import Likes


@admin.register(Likes)
class CustomUserAdmin(admin.ModelAdmin):  # noqa D101
    pass
