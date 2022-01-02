"""Views.py files."""
# Standard Library
import random

# Django
from django.utils import timezone

from django.db import models
from django.db.models import Func, Count
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

# 3rd-party
from core.utils import person_and_tags_for_like

# Project
from accounts.models import CustomUser, Preferences
from accounts.utils import time_today

# Local
from .forms import MessageForm
from .forms import ThreadForm
from .models import DashboardLike, Likes
from .models import DashboardMatched
from .models import DashboardMessage
from .models import Message
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

            crated_mess = DashboardMessage.objects.create(
                count_message_send=0,
                count_message_take=1,
                create_date=str(time_today()),
                custom_user=receiver,

            )
            crated_mess.save()

        else:
            receiver = thread.receiver
        message = Message(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            text_body=request.POST.get('message'),
        )

        message.save()

        crated_mess = DashboardMessage.objects.create(
            count_message_send=1,
            count_message_take=0,
            create_date=str(time_today()),
            custom_user=request.user,

        )
        crated_mess.save()
        return redirect('core:thread', pk=pk)


class DashboardView(TemplateView):  # noqa D101
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        context['like'] = DashboardLike.objects.all().filter(custom_user=current_user).annotate(
            month_data=Month('create_date')).values('month_data').annotate(
            total=Sum('count_like')).order_by('month_data')

        dict_data = {i: 0 for i in range(1, 13)}
        for data in context['like']:
            month_value_pair = list(data.values())
            dict_data[month_value_pair[0]] = month_value_pair[1]
        context['like_list'] = list(dict_data.values())

        context['dislike'] = DashboardLike.objects.all().filter(custom_user=current_user).annotate(
            month_data=Month('create_date')).values('month_data').annotate(
            total=Sum('count_dislike')).order_by('month_data')

        dict_data = {i: 0 for i in range(1, 13)}
        for data in context['dislike']:
            month_value_pair = list(data.values())
            dict_data[month_value_pair[0]] = month_value_pair[1]
        context['dislike_list'] = list(dict_data.values())

        # for pie chart data

        context['data_send'] = DashboardMessage.objects.all().filter(
            custom_user=current_user).aggregate(
            total=Sum('count_message_send'),
        )

        context['data_received'] = DashboardMessage.objects.all().filter(
            custom_user=current_user).aggregate(
            total=Sum('count_message_take'),
        )

        pie_dict = {'message_send': [list(context['data_send'].values())[0],
                                     '%06x' % random.randint(0, 0xFFFFFF)],  # S001
                    'message_received': [list(context['data_received'].values())[0],
                                         '%06x' % random.randint(0, 0xFFFFFF)]}  # S001

        context['dates'] = pie_dict

        # for single bar chart

        context['list_matched'] = DashboardMatched.objects.all().filter(
            Q(custom_user=current_user) | Q(custom_user2=current_user),
        ).annotate(
            month_data=Month('create_date')).values('month_data').annotate(
            total=Sum('count_matched')).order_by('month_data')

        dict_data = {i: 0 for i in range(1, 13)}
        for data in context['list_matched']:
            month_value_pair = list(data.values())
            dict_data[month_value_pair[0]] = month_value_pair[1]
        context['matched_list'] = list(dict_data.values())

        return context


class DashboardAdminView(TemplateView):  # noqa D101
    template_name = 'Dashboard_admin.html'

    def get_context_data(self, **kwargs):  # noqa D102
        context = super().get_context_data(**kwargs)

        # Gender of the users - summary
        context['count_all_gender'] = CustomUser.objects.all().values('sex').annotate(
            count=Count('id')
        )
        print(context['count_all_gender'])

        # most popular tags for user
        context['preferences_users'] = Preferences.objects.all().values(
            'custom_user__preferences__tags', 'age_max', 'age_min', 'sex'
        ).annotate(
            count=Count('id')
        )
        print(context['preferences_users'])

        # how many messages were sent in a current month
        context['all_message'] = Message.objects.all().annotate(
            month_data=Month('date')).values('month_data').annotate(
            total=Count('text_body')).order_by('month_data')

        dict_data = {i: 0 for i in range(1, 13)}
        for data in context['all_message']:
            month_value_pair = list(data.values())
            dict_data[month_value_pair[0]] = month_value_pair[1]
        context['all_message_list'] = list(dict_data.values())

        # test all like
        context['all_Like'] = Likes.objects.all().annotate(
            month_data=Month('date')).values('month_data').annotate(
            total=Count('status').filter(Likes.objects.filter(status='matched'))).order_by('month_data')

        for data in context['all_message']:
            month_value_pair = list(data.values())
            dict_data[month_value_pair[0]] = month_value_pair[1]
        context['all_message_list'] = list(dict_data.values())

        return context




class Month(Func):
    """This function extracts the month from the current date."""

    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
