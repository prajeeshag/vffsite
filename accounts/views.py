from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import signupForm, loginForm

@login_required
def home(request):
    return render(request, 'registration/home.html')


def signin(request):
    if request.method == 'POST':
        if settings.DEBUG:
            print(request.POST)
        form = loginForm(None, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('accounts:home')

    else:
        loginform = loginForm()

    return render(request, 'registration/signin.html', {'form':form,})



def signup(request):
    if request.method == 'POST':
        if settings.DEBUG:
            print(request.POST)
        form = signupForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('accounts:home')
    else:
        form = signupForm()

    return render(request, 'registration/signup.html', {'form':form})


