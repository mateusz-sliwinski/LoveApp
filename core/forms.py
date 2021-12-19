"""Forms.py files."""
# Django
from django import forms


class ThreadForm(forms.Form):  # noqa D101
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.Form):  # noqa D101
    message = forms.CharField(label='', max_length=1000)
