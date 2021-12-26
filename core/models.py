"""Models.py files."""
# Django
from django.db import models
from django.utils import timezone

# Project
from accounts.models import CustomUser


class Likes(models.Model):  # noqa D101
    user_one = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        related_name='user_one'
    )
    user_two = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        related_name='user_two'
    )
    status = models.CharField(max_length=45)

    class Meta:  # noqa D106
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):  # noqa D105
        return f'{self.user_one} {self.user_two} {self.status}'


class Thread(models.Model):  # noqa D101
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='+'
    )
    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='+'
    )

    class Meta:  # noqa D106
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'

    def __str__(self):  # noqa D105
        return f'{self.user} {self.receiver}'


class Message(models.Model):  # noqa D101
    thread = models.ForeignKey(
        'Thread',
        related_name='+',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    sender_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='+'
    )
    receiver_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='+'
    )
    image = models.ImageField(
        upload_to='chat',
        blank=True,
        null=True
    )
    text_body = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:  # noqa D106
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):  # noqa D105
        return f'{self.sender_user} {self.receiver_user}'


class DashboardMessage(models.Model):
    count_message_send = models.IntegerField()
    count_message_take = models.IntegerField()
    create_date = models.DateField()

    message = models.ForeignKey(
        Message,
        on_delete=models.DO_NOTHING,
    )

    class Meta:  # noqa D106
        verbose_name = 'DashboardMessage'
        verbose_name_plural = 'DashboardsMessages'

    def __str__(self):  # noqa D105
        return f'{self.count_message_send}-{self.count_message_take}'


class DashboardLike(models.Model):
    count_like = models.IntegerField()
    count_dislike = models.IntegerField()
    create_date = models.DateField()

    likes = models.ForeignKey(
        Likes,
        on_delete=models.DO_NOTHING,
    )

    class Meta:  # noqa D106
        verbose_name = 'DashboardLike'
        verbose_name_plural = 'DashboardsLikes'

    def __str__(self):  # noqa D105
        return f'{self.create_date}-{self.count_like}-{self.count_dislike}-'
