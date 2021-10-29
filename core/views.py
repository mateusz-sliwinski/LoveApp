"""Views.py files."""
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from accounts.models import CustomUser, PhotoUser
from core.utils import randomize


class RandomPartnerList(TemplateView):
    template_name = 'random_person_list.html'
    success_url = reverse_lazy('core:random')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_id = self.request.user.id
        all_photo = CustomUser.objects.all().count()

        if 'Dislike' in self.request.GET:
            random = randomize(all_photo, current_user_id)
            context['photo'] = PhotoUser.objects.filter(custom_user=random).all()
            return context

        if 'Like' in self.request.GET:
            print('jestem Like')

        return context

    def get(self, request, *args, **kwargs):  # noqa D102
        html = render_to_string(
            self.template_name,
            {'randomPerson': self.get_context_data()},
            request=self.request,
        )
        print(self.get_context_data())
        return HttpResponse(html)


class RandomPartner(TemplateView):
    template_name = 'random_partner.html'

    # test
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_id = self.request.user.id
        all_photo = CustomUser.objects.all().count()
        random = randomize(all_photo, current_user_id)
        context['list'] = PhotoUser.objects.filter(custom_user=random).all()
        return context

    # def dispatch(self, request, *args, **kwargs):
    #
    #     print(self.get_context_data())
    #     return super().dispatch(request, *args, **kwargs)