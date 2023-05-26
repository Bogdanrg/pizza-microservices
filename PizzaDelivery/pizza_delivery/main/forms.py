from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Pizza, PizzaType
from django.forms import formset_factory


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


