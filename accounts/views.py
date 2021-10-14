"""Views.py files."""
from django.shortcuts import render


from accounts.forms import PreferencesForm
from accounts.models import Preferences
from django.template.defaultfilters import slugify

# class MySignupView(FormView):  # noqa D101
#     template_name = 'account/signup.html'


def home_view(request):
    posts = Preferences.objects.all()
    common_tags = Preferences.tags.most_common()[:4]
    form = PreferencesForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.age)
        newpost.save()
        form.save_m2m()
    context = {
        'posts': posts,
        'common_tags': common_tags,
        'form': form,
    }
    return render(request, 'preferences.html', context)
