"""Models.py files."""
# Django
from django.db import models

# Project
from accounts.models import CustomUser


class Likes(models.Model): # noqa D101
    who_i_like = models.CharField(max_length=45)
    who_like_me = models.CharField(max_length=45)
    who_matched_with_me = models.CharField(max_length=45)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    class Meta: # noqa D106
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self): # noqa D105
        return f'{self.who_i_like} {self.who_like_me} {self.who_matched_with_me}'
