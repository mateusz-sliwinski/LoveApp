"""Models.py files."""
# Django
from django.db import models

# Project
from accounts.models import CustomUser


class Likes(models.Model): # noqa D101
    user_one = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='user_one')
    user_two = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='user_two')
    status = models.CharField(max_length=45)

    class Meta: # noqa D106
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self): # noqa D105
        return f'{self.user_one} {self.user_two} {self.status}'
