from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import signupForm, loginForm

@login_required
def home(request):
    return render(request, 'registration/home.html')

def signup_or_login(request):
    if request.method == 'POST':
        if settings.DEBUG:
            print(request.POST)
        if 'login' in request.POST:
            loginform = loginForm(None, request.POST)
            signupform = signupForm(tabActive=False)
            if loginform.is_valid():
                username = loginform.cleaned_data.get('username')
                raw_password = loginform.cleaned_data.get('password')
                user = authenticate(username=username,password=raw_password)
                login(request,user)
                return redirect('accounts:home')

        if 'signup' in request.POST:
            signupform = signupForm(request.POST)
            loginform = loginForm(tabActive=False)
            if signupform.is_valid():
                user=signupform.save()
                # username = signupform.cleaned_data.get('username')
                # raw_password = signupform.cleaned_data.get('password1')
                # user = authenticate(username=username,password=raw_password)
                login(request,user)
                return redirect('accounts:home')
    else:
        signupform = signupForm(tabActive=False)
        loginform = loginForm()

    return render(request, 'registration/signup_or_login.html', {'signupForm':signupform, 
        'loginForm':loginform,})

