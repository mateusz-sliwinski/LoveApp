"""Admin.py files."""

# Django
from django.contrib import admin

# 3rd-party
from core.models import Likes, DashboardLike, DashboardMessage, DashboardMatched
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
class DashboardMatchedeAdmin(admin.ModelAdmin):  # noqa D101
    pass



