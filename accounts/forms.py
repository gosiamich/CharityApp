from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.http import request
from accounts.models import User


class LoginForm(forms.Form):
    email = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email'}))
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


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(max_length=64)
    password2 = forms.CharField(max_length=64)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean_password(self):
        if not validate_password(self.cleaned_data['password']):
            raise ValidationError('Wrong password')
        return self.cleaned_data['password']

    def clean_password(self):
        # Check that the two password entries match
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            raise ValidationError('Podaj dwukrotnie takie samo hasło!')
        return self.cleaned_data['password']


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(label='Imię', widget=forms.TextInput())
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput())


class ChangePassword(forms.Form):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    new_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        data = super().clean()
        errors = []
        if data['new_password'] != data['new_password2']:
            errors.append('Podaj dwukrotnie takie samo hasło!')
            raise forms.ValidationError(errors)
        else:
            return data

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    new_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    class Meta:
        model = User






