from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import signupForm, signinForm

@login_required
def home(request):
    return render(request, 'registration/home.html')


def signin(request):
    if request.method == 'POST':
        if settings.DEBUG:
            print(request.POST)
        form = signinForm(None, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('accounts:home')

    else:
        form = signinForm()

    return render(request, 'registration/base.html', {'form':form,})



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

    return render(request, 'registration/base.html', {'form':form,})


