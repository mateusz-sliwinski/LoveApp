"""Views.py files."""
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from accounts.models import CustomUser
from core.utils import randomize


class RandomPartner(TemplateView):
    template_name = 'random_partner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id
        all_photo = CustomUser.objects.all().count()

        if 'Dislike' in self.request.GET:
            randomize(all_photo, current_user)
            print(all_photo)
            print(current_user)
            print('jestem Dislike')

        if 'Like' in self.request.GET:
            print('jestem Like')


    def get(self, request, *args, **kwargs):  # noqa D102
        html = render_to_string(
            self.template_name,
            {'random_person': self.get_context_data()},
            request=self.request,
        )
        return HttpResponse(html)
