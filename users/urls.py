from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('user_profile/', views.ProfileView.as_view(), name='user_profile'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('', include('django.contrib.auth.urls')),
]
