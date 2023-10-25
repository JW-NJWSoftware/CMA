from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'username',
            }),
            'email': forms.fields.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'email',
            }),
            'first_name': forms.fields.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'first_name',
            }),
            'last_name': forms.fields.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'last_name',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'password1',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'password2',
            }),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class AuthenticateForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
            }),
        }
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        if commit:
            user.save()
        return user
