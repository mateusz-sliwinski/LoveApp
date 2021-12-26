"""Forms.py files."""
# Django
from django import forms

from core.models import Dashboard


class ThreadForm(forms.Form):  # noqa D101
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.Form):  # noqa D101
    message = forms.CharField(label='', max_length=1000)


class DashboardForm(forms.ModelForm):  # noqa D101

    class Meta:  # noqa D102
        model = Dashboard
        fields = [
            'count_like',
            'count_dislike',
            'count_message_send',
            'count_message_take',
            'message',
            'likes',

        ]
