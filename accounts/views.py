"""Views.py files."""
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from urllib3 import request

from accounts.forms import PreferencesForm
from accounts.models import Preferences
from django.template.defaultfilters import slugify


# class MySignupView(FormView):  # noqa D101
#     template_name = 'account/signup.html'
from accounts.utils import validate_tags


class PreferencesView(FormView):
    template_name = 'preferences.html'
    form_class = PreferencesForm
    success_url = '/'

    def form_valid(self, form):
        self.form = form
        tags = form.cleaned_data.get('tags')
        age = form.cleaned_data.get('age')
        current_user = self.request.user
        validate_tags(tags)
        preferences = Preferences.objects.create(
            tags=tags,
            age=age,
            custom_user=current_user
        )
        preferences.save()

        return super().form_valid(form)

