"""Models.py files."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254)
    premium = models.BooleanField(
        blank=True,
        default=False,
    )
    city = models.CharField(max_length=100)


class PhotoUser(models.Model):
    date_add = models.DateField()
    photo = models.ImageField(upload_to='media', null=True, blank=True)
    descriptions = models.TextField(blank=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


