from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

class UserCreateForm(UserCreationForm):

    class Meta:
        model = CustomUser
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
        model = CustomUser
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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        widgets = {
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
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
