from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import LoginUserForm


class Login(LoginView):
    template_name = 'users/auth.html'
    form_class = LoginUserForm


class Logout(LogoutView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_default_redirect_url(self):
        return reverse_lazy('blog:all_posts')
