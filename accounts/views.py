from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import pyotp

from .forms import SignupForm1, SignupForm2


@login_required
def home(request):
    return render(request, 'registration/home.html')


def signin(request):
    if settings.DEBUG:
        print(request.POST)
    form = SignupForm2(user_id=11)

    return render(request, 'registration/base.html', {'form': form, })


def signup(request):

    if settings.DEBUG:
        print(request.POST)

    if 'sendOTP' in request.POST:
        form = SignupForm1(request.POST)
        if form.is_valid():
            user = form.save()
            form = SignupForm2(user_id=user.pk)
    else:
        form = SignupForm1()

    return render(request, 'registration/base.html', {'form': form, })
