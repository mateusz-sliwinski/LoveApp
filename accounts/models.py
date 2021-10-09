"""Models.py files."""
# Django
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):  # noqa D101
    email = models.EmailField(max_length=254)
    premium = models.BooleanField(
        blank=True,
        default=False,
    )
    city = models.CharField(max_length=100)

    class Meta:  # noqa: D106

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):  # noqa: D105
        return f'{self.email} {self.last_name}'


class PhotoUser(models.Model):  # noqa D101
    date_add = models.DateField()
    photo = models.ImageField(upload_to='media', null=True, blank=True)
    descriptions = models.TextField(blank=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:  # noqa: D106

        verbose_name = 'Photo User'
        verbose_name_plural = 'Photo Users'

    def __str__(self):  # noqa: D105
        return f'{self.custom_user.first_name} {self.custom_user.last_name} {self.photo}'
