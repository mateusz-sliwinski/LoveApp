"""Views.py files."""
# Django
import stripe
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

# Project
from accounts.forms import PhotoForm
from accounts.forms import PreferencesForm
from accounts.models import CustomUser
from accounts.models import PhotoUser
from accounts.models import Preferences
from accounts.utils import take_id_from_path
from accounts.utils import time_today
from accounts.utils import validate_tags
from project import settings


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
        current_user = self.request.user
        photo2 = form.cleaned_data.get('photo')

        photo = PhotoUser.objects.create(
            date_add=time_today(),
            photo=photo2,
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
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['photo'] = PhotoUser.objects.filter(custom_user=current_user).all()
        context['users'] = CustomUser.objects.filter(id=current_user.id).all()
        return context


class test(TemplateView):  # noqa D101
    template_name = 'payments.html'


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'premium',
                        'quantity': 1,
                        'currency': 'pln',
                        'amount': '5',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
