from django.shortcuts import (
    render,
    redirect
    )
from . import forms

from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
    )


def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request, *args, **kwargs):
    """Signs up a new user."""

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            if user:
                auth_user = authenticate(username=username, password=password)
                login(request, auth_user)
                return redirect('/')
    elif request.method == 'GET':
        form = forms.SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """The user can login either by username or password."""

    if request.method == 'POST':
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')

    elif request.method == 'GET':
        form = forms.SignInForm()
    return render(request, 'users/login.html', {
                'form': form,
            })
