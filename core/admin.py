"""Admin.py files."""

# Django
from django.contrib import admin

# 3rd-party
from core.models import DashboardLike, Message
from core.models import DashboardMatched
from core.models import DashboardMessage
from core.models import Likes
from core.models import Thread


@admin.register(Likes)
class CustomUserAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(DashboardLike)
class DashboardLikeAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(DashboardMessage)
class DashboardMessageAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(DashboardMatched)
class DashboardMatchedAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):  # noqa D101
    pass
