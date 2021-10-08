"""Forms.py file."""
# Django
from django import forms

# 3rd-party
from allauth.account.forms import SignupForm

from accounts.models import CustomUser, PhotoUser
from .utils import time_today

class MySignUpForm(SignupForm):  # noqa D101
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    city = forms.CharField(label='City', max_length=150)
    photo = forms.ImageField(label='Photo')
    descriptions = forms.Textarea()
    class Meta:  # noqa D106
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'city',
        ]

    def save(self, request):  # noqa D102
        city = self.cleaned_data['city']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        photo = self.cleaned_data['photo']
        descriptions = self.cleaned_data['descriptions']

        user = CustomUser(
            first_name=first_name,
            city=city,
            last_name=last_name,
            premium=False,
        )
        user.save()

        photo_user = PhotoUser(
            date_add=time_today(),
            photo=photo,
            descriptions=descriptions
        )
        photo_user.save()
