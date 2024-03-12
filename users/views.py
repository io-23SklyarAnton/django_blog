from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm, RegistrationForm


class Login(LoginView):
    template_name = 'users/auth.html'
    form_class = LoginUserForm


class Logout(LogoutView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_default_redirect_url(self):
        return reverse_lazy('blog:all_posts')


class Registration(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
