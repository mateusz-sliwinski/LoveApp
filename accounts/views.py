"""Views.py files."""
from django.shortcuts import render

class MySignupView(FormView):  # noqa D101
    template_name = 'account/signup.html'

class MyLoginupView(LoginView):  # noqa D101
    template_name = 'account/login.html'

