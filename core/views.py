"""Views.py files."""
# Django
from django.db.models import Q, Sum, Func
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.db import models
# 3rd-party
from core.utils import person_and_tags_for_like

# Project
from accounts.models import CustomUser

# Local
from .forms import MessageForm
from .forms import ThreadForm
from .models import Message, DashboardLike
from .models import Thread
from .utils import person_and_tags


class RandomPartnerList(TemplateView):  # noqa D101
    template_name = 'random_person_list.html'
    success_url = reverse_lazy('core:random')

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user_id = self.request.user.id
        current_user = self.request.user
        all_photo = CustomUser.objects.all().count()

        if 'Dislike' in self.request.GET:
            context = person_and_tags(all_photo, context, current_user_id)
            return context

        if 'Like' in self.request.GET:
            context = person_and_tags_for_like(all_photo, context, current_user_id, current_user)

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


class RandomPartner(TemplateView):  # noqa D101
    template_name = 'random_partner.html'


class ListThreads(View):  # noqa D101
    def get(self, request, *args, **kwargs):  # noqa D102
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads,
        }

        return render(request, 'social/inbox.html', context)


class CreateThread(View):  # noqa D101
    def get(self, request, *args, **kwargs):  # noqa D102
        form = ThreadForm()

        context = {
            'form': form,
        }

        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):  # noqa D102
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = CustomUser.objects.get(username=username)
            if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = Thread(
                    user=request.user,
                    receiver=receiver,
                )
                thread.save()

                return redirect('core:thread', pk=thread.pk)
        except username.DoesNotExist:
            return redirect('core:create-thread')


class ThreadView(View):  # noqa D101
    def get(self, request, pk, *args, **kwargs):  # noqa D102
        form = MessageForm()
        thread = Thread.objects.get(pk=pk)
        message_list = Message.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list,
        }

        return render(request, 'social/thread.html', context)


class CreateMessage(View):  # noqa D101
    def post(self, request, pk, *args, **kwargs):  # noqa D102
        thread = Thread.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = Message(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            text_body=request.POST.get('message'),
        )

        message.save()
        return redirect('core:thread', pk=pk)


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)

        context['like'] = DashboardLike.objects.all().annotate(
            month_data=Month('create_date')).values('month_data').annotate(
            total=Sum('count_like')).order_by('month_data')

        context['dislike'] = DashboardLike.objects.all().annotate(
            month_data=Month('create_date')).values('month_data').annotate(
            total=Sum('count_dislike')).order_by('month_data')

        dict_data = {i: 0 for i in range(1, 13)}
        for data in context['date']:
            month_value_pair = list(data.values())
            dict_data[month_value_pair[0]] = month_value_pair[1]
        context['list'] = list(dict_data.values())

        return context


class Month(Func):
    """This function extracts the month from the current date."""

    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
