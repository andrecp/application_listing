from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class SignUpForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'control-group form-group controls form-control'}), max_length=100)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'control-group form-group controls form-control'}), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'control-group form-group controls form-control'}), max_length=100)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email


class SignInForm(forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'control-group form-group controls form-control'}), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'control-group form-group controls form-control'}), max_length=100)

    def clean(self, *args, **kwargs):
        username_or_email = self.cleaned_data['username_or_email']
        username = False
        email = False

        # First try by username then by email.
        if User.objects.filter(username=username_or_email).exists():
            username = True
        else:
            user = User.objects.filter(email=username_or_email).exists()
            if user:
                user = User.objects.filter(email=username_or_email).get()
                email = True

        if not (email or username):
            raise ValidationError('Username and/or email not registered')

        # Log in by whichever they have.
        if username:
            user = authenticate(username=self.cleaned_data['username_or_email'],
                                password=self.cleaned_data['password'])
        else:
            user = authenticate(username=user.username, password=self.cleaned_data['password'])

        # If can't login, raise.
        if not user:
            raise ValidationError('Email/Password mismatch')

        # If we didn't raise it's because we have user.username.
        self.cleaned_data['username_or_email'] = user.username
        return super(SignInForm, self).clean(*args, **kwargs)
