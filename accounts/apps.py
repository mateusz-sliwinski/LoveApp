"""Apps.py files."""

# Django
from django.apps import AppConfig


class AccountConfig(AppConfig):  # noqa D101
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
