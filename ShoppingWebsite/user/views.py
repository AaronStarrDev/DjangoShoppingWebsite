from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from user.forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        sign_up_form = SignUpForm()
    return render(request, 'user/signup.html', {'sign_up_form': sign_up_form, 'title': 'Sign Up'})

def log_in(request):
    if request.method == 'POST':
        log_in_form = AuthenticationForm(request=request, data=request.POST)
        if log_in_form.is_valid():
            username = log_in_form.cleaned_data.get('username')
            password = log_in_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "User doesn't exist.")
    log_in_form = AuthenticationForm()
    return render(request, 'user/login.html', {'log_in_form': log_in_form, 'title': 'log in'})

def log_out(request):
    logout(request)
    return redirect('home')

def settings(request):
    return