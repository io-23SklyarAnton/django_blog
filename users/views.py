from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordResetView, PasswordChangeDoneView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegistrationForm


class Logout(LogoutView):

    def get_default_redirect_url(self):
        return reverse_lazy('blog:all_posts')


class Registration(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    template_name = 'user/profile.html'
    model = User
    fields = ['username', 'first_name', 'last_name']

    def get_object(self, **kwargs):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return render(self.request, self.template_name, {'success': True, 'form': form})


class PasswordChange(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('users:change_password_done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'registration/change_password_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'registration/reset_password.html'
    email_template_name = 'registration/reset_password_email.html'
    success_url = reverse_lazy('users:reset_password_done')
    extra_email_context = {'domain': '127.0.0.1:8000', 'site_name': '127.0.0.1:8000'}


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/reset_password_confirm.html'
    success_url = reverse_lazy("users:reset_password_complete")


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/reset_password_done.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/reset_password_complete.html'
