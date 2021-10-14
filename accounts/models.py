"""Models.py files."""
# Django
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from taggit.managers import TaggableManager

class CustomUser(AbstractUser):  # noqa D101
    email = models.EmailField(max_length=254)
    premium = models.BooleanField(
        blank=True,
        default=False,
    )
    city = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:  # noqa: D106
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):  # noqa: D105
        today = date.today()
        age = relativedelta(today, self.birth_date)

        return f'{self.email} {self.last_name} {age.years}'


class PhotoUser(models.Model):  # noqa D101
    date_add = models.DateField()
    photo = models.ImageField(upload_to='photo', null=True, blank=True)
    descriptions = models.TextField(blank=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:  # noqa: D106

        verbose_name = 'Photo User'
        verbose_name_plural = 'Photo Users'

    def __str__(self):  # noqa: D105
        return f'{self.custom_user.first_name} {self.custom_user.last_name} {self.photo}'


class Preferences(models.Model):
    categories = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    age = models.IntegerField(
        default=18,
        validators=[
            MaxValueValidator(200),
            MinValueValidator(18)
        ]
     )
    slug = models.SlugField(unique=True)
    tags = TaggableManager()
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.tags
