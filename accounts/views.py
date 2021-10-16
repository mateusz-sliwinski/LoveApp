"""Views.py files."""
# Django
from django.views.generic import FormView, DetailView, ListView

# Project
from accounts.forms import PreferencesForm, PhotoForm
from accounts.models import Preferences, PhotoUser
from accounts.utils import validate_tags, take_id_from_path


class PreferencesView(FormView): # noqa  D101
    template_name = 'preferences.html'
    form_class = PreferencesForm
    success_url = '/'

    def form_valid(self, form): # noqa D102
        self.form = form
        tags = form.cleaned_data.get('tags')
        age_min = form.cleaned_data.get('age_min')
        age_max = form.cleaned_data.get('age_max')
        sex = form.cleaned_data.get('sex')

        current_user = self.request.user
        validate_tags(tags)
        preferences = Preferences.objects.create(
            tags=tags,
            age_min=age_min,
            age_max=age_max,
            sex=sex,
            custom_user=current_user,
        )
        preferences.save()

        return super().form_valid(form)


class PhotoView(FormView):
    template_name = 'photo.html'
    form_class = PhotoForm
    success_url = '/'

    def form_valid(self, form): # noqa D102
        self.form = form
        photo = form.cleaned_data.get('photo')
        date = form.cleaned_data.get('date')
        descriptions = form.cleaned_data.get('descriptions')

        current_user = self.request.user
        photo = PhotoUser.objects.create(
            date_add=date,
            photo=photo,
            descriptions=descriptions,
            custom_user=current_user,
        )
        photo.save()

        return super().form_valid(form)


class ListPhoto(ListView):
    model = PhotoUser
    template_name = 'list_photo.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['data_photo'] = PhotoUser.objects.filter(custom_user=current_user).all()
        return context


class DetailPhoto(DetailView):
    model = PhotoUser
    template_name = 'detail_photo.html'
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        full_path = self.request.get_full_path()
        id_path = take_id_from_path(full_path)

        context['data_photo'] = PhotoUser.objects.filter(custom_user=current_user).get(id=id_path)
        print(context)
        return context
