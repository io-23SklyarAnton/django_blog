from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('user_profile/', views.ProfileView.as_view(), name='user_profile'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('change_password/', views.PasswordChange.as_view(), name='change_password'),
    path('change_password_done/', views.PasswordChangeDone.as_view(), name='change_password_done'),
    path('reset_password/', views.PasswordReset.as_view(), name='reset_password'),
    path('password_reset_done/', views.PasswordResetDone.as_view(), name='reset_password_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),
         name='reset_password_confirm'),
    path('reset_password_complete/', views.PasswordResetComplete.as_view(), name='reset_password_complete'),
    path('', include('django.contrib.auth.urls')),
]
