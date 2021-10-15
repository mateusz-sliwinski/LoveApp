"""Views.py files."""
# Django
from django.views.generic import FormView

# Project
from accounts.forms import PreferencesForm
from accounts.models import Preferences
from accounts.utils import validate_tags


class PreferencesView(FormView): # noqa  D101
    template_name = 'preferences.html'
    form_class = PreferencesForm
    success_url = '/'

    def form_valid(self, form): # noqa D102
        self.form = form
        tags = form.cleaned_data.get('tags')
        age = form.cleaned_data.get('age')
        current_user = self.request.user
        validate_tags(tags)
        preferences = Preferences.objects.create(
            tags=tags,
            age=age,
            custom_user=current_user,
        )
        preferences.save()

        return super().form_valid(form)
