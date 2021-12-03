"""Models.py files."""
# Django
from django.db import models
from django.utils import timezone

# Project
from accounts.models import CustomUser


class Likes(models.Model):  # noqa D101
    user_one = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='user_one')
    user_two = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='user_two')
    status = models.CharField(max_length=45)

    class Meta:  # noqa D106
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):  # noqa D105
        return f'{self.user_one} {self.user_two} {self.status}'


class Thread(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')


class Message(models.Model):
    thread = models.ForeignKey('Thread', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    text_body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='chat', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
