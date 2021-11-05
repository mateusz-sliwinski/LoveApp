"""Views.py files."""
import requests
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from accounts.models import CustomUser, PhotoUser, Preferences
from core.models import Likes
from core.utils import randomize, person_and_tags_for_like
from .utils import person_and_tags


class RandomPartnerList(TemplateView):
    template_name = 'random_person_list.html'
    success_url = reverse_lazy('core:random')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_id = self.request.user.id
        current_user = self.request.user
        all_photo = CustomUser.objects.all().count()

        if 'Dislike' in self.request.GET:
            context = person_and_tags(all_photo, context, current_user_id)
            return context

        if 'Like' in self.request.GET:
            context = person_and_tags_for_like(all_photo, context, current_user_id)
            print(current_user)
            # dodać id 2 usera napisac funkcje parującą  /update scalanie?
            # x = Likes.objects.create(
            #     user_one=current_user_id,
            #     user_two=PhotoUser.objects.filter.get(id=id),
            #     status='NUll',
            # )
            # x.save()
            return context

        context = person_and_tags(all_photo, context, current_user_id)
        return context

    def get(self, request, *args, **kwargs):  # noqa D102
        html = render_to_string(
            self.template_name,
            {'photo': self.get_context_data()},
            request=self.request,
        )
        return HttpResponse(html)


class RandomPartner(TemplateView):
    template_name = 'random_partner.html'

    # test
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     current_user_id = self.request.user.id
    #     all_photo = CustomUser.objects.all().count()
    #     random = randomize(all_photo, current_user_id)
    #     context['preferences'] = Preferences.objects.filter(custom_user=random).all()
    #     return context
    #
    # # def dispatch(self, request, *args, **kwargs):
    # #
    # #     print(self.get_context_data())
    # #     return super().dispatch(request, *args, **kwargs)
