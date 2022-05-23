from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.http import request
from accounts.models import User


class LoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


def validate_length(password):
    return len(password) >= 7


def validate_upper(password):
    return any(x for x in password if x.isupper())


def validate_lower(password):
    return any(x for x in password if x.islower())


def validate_special(password):
    special = """!@#$%^&*()_+=-~{}[]:"|;'\<>?,./\|"""
    return any(x for x in password if x in special)


def validate_digit(password):
    return any(x for x in password if x.isdigit())


def validate_password(password):
    validators = [
        validate_digit,
        validate_special,
        validate_lower,
        validate_upper,
        validate_length
    ]
    for validator in validators:
        if not validator(password):
            return False
        return True


class CreateUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    password2 = forms.CharField(max_length=64)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean(self):
        data = super().clean()
        if data['password'] != data['password2']:
            self.add_error('password','Podaj dwukrotnie takie samo hasło!')
        if not 'password' in data:
            return data
        if not validate_password(self.cleaned_data['password']):
            self.add_error('password','Nowe hasło musi zawierać cyfrę, liczbę, dużą i małą literę.')
        else:
            return data


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(label='  Imię', widget=forms.TextInput())
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput())
    password = forms.CharField(label='  Aktualne hasło', widget=forms.PasswordInput())


class ChangePassword(forms.Form):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    new_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        data = super().clean()
        if data['new_password'] != data['new_password2']:
            self.add_error('new_password','Podaj dwukrotnie takie samo hasło!')
        if not 'new_password' in data:
            return data
        if not validate_password(self.cleaned_data['new_password']):
            self.add_error('new_password','Nowe hasło musi zawierać cyfrę, liczbę, dużą i małą literę.')
        else:
            return data


