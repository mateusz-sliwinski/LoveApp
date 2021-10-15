"""Views.py files."""
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import PreferencesForm
from accounts.models import Preferences
from django.template.defaultfilters import slugify


# class MySignupView(FormView):  # noqa D101
#     template_name = 'account/signup.html'


class PreferencesView(FormView):
    template_name = 'preferences.html'
    form_class = PreferencesForm
    success_url = '/'

    def form_valid(self, form):
        self.form = form
        tags = self.form.cleaned_data.get('tags')
        types = self.form.cleaned_data.get('type')

        context = {
            'count_tags': Preferences.objects.count() + 1,
        }

        if form.is_valid():
            person = form.save(commit=False)
            person.slug = slugify(context['count_tags'])
            person.tags = tags

            person.save()
            form.save_m2m()

        return super().form_valid(form)

# def home_view(request):
#     posts = Preferences.objects.all()
#     common_tags = Preferences.tags.most_common()[:4]
#     form = PreferencesForm(request.POST)
#     if form.is_valid():
#         newpost = form.save(commit=False)
#         newpost.slug = slugify(newpost.id)
#         newpost.save()
#         form.save_m2m()
#     context = {
#         'posts': posts,
#         'common_tags': common_tags,
#         'form': form,
#     }
#     return render(request, 'preferences.html', context)
