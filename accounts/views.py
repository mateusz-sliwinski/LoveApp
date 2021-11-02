"""Views.py files."""
# Django
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

# Project
from accounts.forms import PhotoForm
from accounts.forms import PreferencesForm
from accounts.models import PhotoUser
from accounts.models import Preferences
from accounts.utils import take_id_from_path, time_today
from accounts.utils import validate_tags


class PreferencesView(FormView):  # noqa  D101
    template_name = 'preferences.html'
    form_class = PreferencesForm
    success_url = reverse_lazy('preferences_list')

    def form_valid(self, form):  # noqa D102
        self.form = form
        tags = form.cleaned_data.get('tags')
        age_min = form.cleaned_data.get('age_min')
        age_max = form.cleaned_data.get('age_max')
        sex = form.cleaned_data.get('sex')

        current_user = self.request.user
        validate_tags(tags)
        if Preferences.objects.filter(custom_user=current_user).exists():
            raise ValidationError('You have Already Preferences')
        else:
            preferences = Preferences.objects.create(
                tags=tags,
                age_min=age_min,
                age_max=age_max,
                sex=sex,
                custom_user=current_user,
            )
            preferences.save()

        return super().form_valid(form)


class PhotoView(FormView):  # noqa D101
    template_name = 'photo.html'
    form_class = PhotoForm
    success_url = reverse_lazy('list_photo')

    def form_valid(self, form):  # noqa D102
        self.form = form
        photo = form.cleaned_data.get('photo')
        descriptions = form.cleaned_data.get('descriptions')

        current_user = self.request.user
        photo = PhotoUser.objects.create(
            date_add=time_today,
            photo=photo,
            descriptions=descriptions,
            custom_user=current_user,
        )
        photo.save()

        return super().form_valid(form)


class ListPhotoView(ListView):  # noqa D101
    model = PhotoUser
    template_name = 'list_photo.html'
    success_url = '/'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['data_photo'] = PhotoUser.objects.filter(custom_user=current_user).all()
        return context


class DetailPhotoView(DetailView):  # noqa D101
    model = PhotoUser
    template_name = 'detail_photo.html'
    success_url = '/'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        full_path = self.request.get_full_path()
        id_path = take_id_from_path(full_path)
        context['data_photo'] = PhotoUser.objects.filter(custom_user=current_user).get(id=id_path)
        return context


class DeletePhotoView(DeleteView):  # noqa D101
    model = PhotoUser
    template_name = 'delete_photo.html'
    success_url = reverse_lazy('list_photo')

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        full_path = self.request.get_full_path()
        id_path = take_id_from_path(full_path)
        context['data_photo'] = PhotoUser.objects.filter(custom_user=current_user).get(id=id_path)

        return context


class PreferencesListView(ListView):  # noqa D101
    model = Preferences
    template_name = 'list_preferences.html'
    success_url = '/'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['data_preferences'] = Preferences.objects.filter(custom_user=current_user).all()

        return context


class PreferencesUpdateView(UpdateView):  # noqa D101
    model = Preferences
    template_name = 'preferences.html'
    success_url = reverse_lazy('preferences_list')

    fields = [
        'age_min',
        'age_max',
        'tags',
        'sex',
    ]


class HomeView(TemplateView):  # noqa D101
    template_name = 'home_page.html'

    def get(self, request, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        current_user = self.request.user
        context['photo'] = PhotoUser.objects.filter(custom_user=current_user).all()
        context['preferences'] = Preferences.objects.filter(custom_user=current_user).all()
        context = {
            'photo': context['photo'],
            'preferences': context['preferences'],
        }
        print(context)
        return super().get(context)
