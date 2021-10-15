"""Forms.py file."""
# Django
import datetime

from django import forms

# 3rd-party
from allauth.account.forms import SignupForm
# Project
from urllib3 import fields

from accounts.models import CustomUser, Preferences
from accounts.models import PhotoUser

# Local
from .utils import time_today, legitimate_age


class MySignUpForm(SignupForm):  # noqa D101
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    city = forms.CharField(label='City', max_length=150)
    photo = forms.ImageField(required=False)
    descriptions = forms.CharField(widget=forms.Textarea, label='descriptions photo', required=False)
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:  # noqa D106
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'city',
        ]

    def save(self, request):  # noqa D102
        photo = self.cleaned_data['photo']
        descriptions = self.cleaned_data['descriptions']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        city = self.cleaned_data['city']
        date = self.cleaned_data['date']

        user = super().save(request)
        user.first_name = first_name
        user.last_name = last_name
        user.city = city
        user.birth_date = date
        user.save()

        if photo is True:
            context = {
                'count_users': user.id,
            }

            user_photo = PhotoUser(
                date_add=time_today(),
                photo=photo,
                descriptions=descriptions,
                custom_user=CustomUser.objects.get(id=context['count_users']),
            )
            user_photo.save()
        else:
            pass

        return user


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = [
            'age',
            'tags',
        ]
