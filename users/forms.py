from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login or Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.TextInput(attrs={'class': 'form-input'}))

    email = forms.EmailField(label='E-Mail')
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth', 'avatar']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'avatar': forms.FileInput(),
        }

    def clean_email(self):
        cd = self.cleaned_data
        if get_user_model().objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('This email is already exists')
        return cd['email']


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'avatar', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'avatar': forms.FileInput(),
        }
