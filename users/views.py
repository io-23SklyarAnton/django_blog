from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from .forms import RegistrationForm, UserForm


class Logout(LogoutView):

    def get_default_redirect_url(self):
        return reverse_lazy('blog:all_posts')


class Registration(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')


# class ProfileView(FormView):
#     template_name = 'user/profile.html'
#     form_class = UserForm
#     success_url = '#'
#
#     def get_form_kwargs(self):
#         """adds User instance arg to form"""
#         kwargs = super().get_form_kwargs()
#         kwargs['instance'] = self.request.user
#         return kwargs

class ProfileView(UpdateView):
    template_name = 'user/profile.html'
    model = User
    fields = ['username', 'first_name', 'last_name']

    def get_object(self, **kwargs):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return render(self.request, self.template_name, {'success': True, 'form': form})
